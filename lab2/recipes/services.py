import asyncio

import httpx
from fastapi import status
from fastapi.exceptions import HTTPException
from schemas import Recipe, RecipeInfo
from settings import settings
from logging import getLogger

from utils import is_user_error

NUMBER_OF_RECIPES_PER_QUERY = 7

logger = getLogger(__name__)


SERVICE_UNAVAILABLE = HTTPException(
    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    detail="External service is unavailable",
)
BAD_REQUEST = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="No recipes found",
)


async def translate_ingredients(ingredients: list[str]) -> list[str]:
    translations = await translate_texts(ingredients, target_language="en")
    return translations


async def translate_recipes(recipes: list[Recipe]) -> None:
    texts_to_translate = _get_texts_to_translate(recipes)
    translations = await translate_texts(
        texts_to_translate, target_language=settings.TARGET_LANGUAGE
    )
    translations_by_text = dict(list(zip(texts_to_translate, translations)))
    _merge_recipes_with_translations(recipes, translations_by_text)


def _get_texts_to_translate(recipes: list[Recipe]) -> list[str]:
    texts_to_translate = []

    for recipe in recipes:
        texts_to_translate.extend(recipe.get_texts_to_translate())

    return texts_to_translate


def _merge_recipes_with_translations(
    recipes: list[Recipe], translations_by_text: dict[str, str]
) -> None:
    for recipe in recipes:
        recipe.title = translations_by_text[recipe.title]
        recipe.missed_ingredients = [
            translations_by_text[ingredient] for ingredient in recipe.missed_ingredients
        ]
        recipe.used_ingredients = [
            translations_by_text[ingredient] for ingredient in recipe.used_ingredients
        ]
        recipe.summary = translations_by_text[recipe.summary]


async def translate_texts(text: list[str], target_language: str) -> list[str]:
    url = f"{settings.DEEPL_API_URL}/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {settings.DEEPL_API_KEY}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "text": text,
        "target_lang": target_language,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=url,
            headers=headers,
            data=data,
        )

    if response.status_code != 200:
        logger.info(f"Failed to translate texts: {text}")
        if is_user_error(response.status_code):
            raise BAD_REQUEST
        raise SERVICE_UNAVAILABLE

    return [t["text"] for t in response.json()["translations"]]


async def fetch_recipes(ingredients_en: list[str]) -> list[Recipe]:
    merged_ingredients = ",".join(ingredients_en)
    base_url = (
        f"{settings.FOOD_API_URL}/recipes/findByIngredients?"
        f"number={NUMBER_OF_RECIPES_PER_QUERY}&ignorePantry=true&ingredients={merged_ingredients}&"
        f"apiKey={settings.FOOD_API_KEY}"
    )
    min_missing_url = f"{base_url}&ranking=1"
    max_used_url = f"{base_url}&ranking=2"

    async with httpx.AsyncClient() as client:
        min_missing_result, max_used_result = await asyncio.gather(
            client.get(min_missing_url),
            client.get(max_used_url),
        )

        if min_missing_result.status_code != 200 or max_used_result.status_code != 200:
            logger.info(
                f"Failed to fetch recipes for ingredients: {ingredients_en}, "
                f"{min_missing_result.status_code=}, {max_used_result.status_code=}"
            )

            if is_user_error(min_missing_result.status_code) or is_user_error(max_used_result.status_code):
                raise BAD_REQUEST

            raise SERVICE_UNAVAILABLE

    recipes = [*min_missing_result.json(), *max_used_result.json()]
    recipes_by_ids = {recipe["id"]: recipe for recipe in recipes}
    recipes_ids = recipes_by_ids.keys()

    async with (httpx.AsyncClient() as client):
        recipes_info = await client.get(
            f"{settings.FOOD_API_URL}/recipes/informationBulk"
            f"?apiKey={settings.FOOD_API_KEY}&includeNutrition=true&ids={','.join([str(r) for r in recipes_ids])}"
        )

        if recipes_info.status_code != 200:
            logger.info(f"Failed to fetch recipes info or summaries")
            if is_user_error(recipes_info.status_code):
                raise BAD_REQUEST
            raise SERVICE_UNAVAILABLE

    for recipe_info in recipes_info.json():
        recipe = recipes_by_ids[recipe_info["id"]]
        recipe.update(recipe_info)

    return [Recipe.from_api_response(recipe) for recipe in recipes_by_ids.values()]


def divide_recipes(recipes: list[Recipe]) -> RecipeInfo:
    min_missing = min(recipes, key=lambda r: len(r.missed_ingredients))
    max_used = max(recipes, key=lambda r: len(r.used_ingredients))
    lowest_calories = min(recipes, key=lambda r: r.calories)
    fastest_to_prepare = min(recipes, key=lambda r: r.ready_in_minutes)
    cheapest = min(recipes, key=lambda r: r.price)
    healthiest = max(recipes, key=lambda r: r.health_score)

    return RecipeInfo(
        min_missing=min_missing,
        max_used=max_used,
        lowest_calories=lowest_calories,
        fastest_to_prepare=fastest_to_prepare,
        cheapest=cheapest,
        healthiest=healthiest,
        rest=[
            r for r in recipes
            if r not in (
                min_missing, max_used, lowest_calories, fastest_to_prepare, cheapest, healthiest
            )
        ]
    )

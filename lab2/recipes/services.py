import asyncio

import httpx
from fastapi import status
from fastapi.exceptions import HTTPException
from schemas import Recipe
from settings import settings


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
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="External service is unavailable",
        )

    return [t["text"] for t in response.json()["translations"]]


async def fetch_recipes(ingredients_en: list[str]) -> list[Recipe]:
    merged_ingredients = ",".join(ingredients_en)
    base_url = (
        f"{settings.FOOD_API_URL}/recipes/findByIngredients?"
        f"number=3&ignorePantry=true&ingredients={merged_ingredients}&"
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
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="External service is unavailable",
            )

    recipes = [*min_missing_result.json(), *max_used_result.json()]
    recipes_by_ids = {recipe["id"]: recipe for recipe in recipes}

    async with httpx.AsyncClient() as client:
        recipes_summaries = await asyncio.gather(
            *(
                client.get(
                    f"{settings.FOOD_API_URL}/recipes/{recipe_id}/summary?apiKey={settings.FOOD_API_KEY}"
                )
                for recipe_id in recipes_by_ids.keys()
            )
        )

        if any(response.status_code != 200 for response in recipes_summaries):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="External service is unavailable",
            )

    for summary_response in recipes_summaries:
        summary = summary_response.json()
        recipe = recipes_by_ids[summary["id"]]
        recipe["summary"] = summary["summary"]

    return [Recipe.from_api_response(recipe) for recipe in recipes_by_ids.values()]

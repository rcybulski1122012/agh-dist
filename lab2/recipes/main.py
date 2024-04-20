from typing import Annotated

from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from logging import getLogger

from dependencies import validate_ingredients, validate_api_key
from schemas import RecipeInfo
from services import fetch_recipes, translate_ingredients, translate_recipes, divide_recipes, BAD_REQUEST

logger = getLogger(__name__)
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def main(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="form.html")


@app.get("/recipes/")
async def get_recipes(
    request: Request,
    ingredients: Annotated[list[str], Depends(validate_ingredients)],
    _api_key: Annotated[str, Depends(validate_api_key)],
) -> RecipeInfo:
    translated_ingredients = await translate_ingredients(ingredients)
    try:
        recipes = await fetch_recipes(translated_ingredients)
    except ValidationError as e:
        logger.info(f"Validation error caused by external service response: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="External service is unavailable",
        )
    await translate_recipes(recipes)
    recipe_info = divide_recipes(recipes)

    return recipe_info

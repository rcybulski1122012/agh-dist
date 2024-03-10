from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services import fetch_recipes, translate_ingredients, translate_recipes

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def main(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="form.html")


@app.post("/recipes/")
async def get_recipes(
    request: Request, ingredients: Annotated[str, Form(...)]
) -> HTMLResponse:
    ingredients = [s.strip() for s in ingredients.strip().split(",")]
    translated_ingredients = await translate_ingredients(ingredients)
    recipes = await fetch_recipes(translated_ingredients)
    await translate_recipes(recipes)

    return templates.TemplateResponse(
        request=request, name="result.html", context={"recipes": recipes}
    )

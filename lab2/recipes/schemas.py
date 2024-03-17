from pydantic import BaseModel
from pydantic_core import Url


class Recipe(BaseModel):
    title: str
    image: Url
    missed_ingredients: list[str]
    used_ingredients: list[str]
    summary: str
    calories: float
    ready_in_minutes: int
    price: float
    health_score: int

    @classmethod
    def from_api_response(cls, response: dict) -> "Recipe":
        return cls(
            title=response["title"],
            image=response["image"],
            missed_ingredients=[
                ingredient["original"] for ingredient in response["missedIngredients"]
            ],
            used_ingredients=[
                ingredient["original"] for ingredient in response["usedIngredients"]
            ],
            summary=response["summary"],
            calories=cls._get_calories_from_nutrients(response["nutrition"]["nutrients"]),
            ready_in_minutes=response["readyInMinutes"],
            price=response["pricePerServing"],
            health_score=response["healthScore"],
        )

    @staticmethod
    def _get_calories_from_nutrients(nutrients: list[dict]) -> float:
        for nutrient in nutrients:
            if nutrient["name"] == "Calories":
                return nutrient["amount"]
        return 0.0

    def get_texts_to_translate(self) -> list[str]:
        return [
            self.title,
            *self.missed_ingredients,
            *self.used_ingredients,
            self.summary,
        ]


class RecipeInfo(BaseModel):
    min_missing: Recipe
    max_used: Recipe
    lowest_calories: Recipe
    fastest_to_prepare: Recipe
    cheapest: Recipe
    healthiest: Recipe
    rest: list[Recipe]


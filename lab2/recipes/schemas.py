from pydantic import BaseModel
from pydantic_core import Url


class Recipe(BaseModel):
    title: str
    image: Url
    missed_ingredients: list[str]
    used_ingredients: list[str]
    summary: str

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
        )

    def get_texts_to_translate(self) -> list[str]:
        return [
            self.title,
            *self.missed_ingredients,
            *self.used_ingredients,
            self.summary,
        ]

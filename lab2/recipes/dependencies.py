from fastapi import HTTPException, status


def validate_ingredients(ingredients: str) -> list[str]:
    ingredients = [s.strip() for s in ingredients.strip().split(",") if s.strip()]
    if not ingredients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No ingredients provided",
        )
    return ingredients

from fastapi import HTTPException, status

FAKE_API_KEYS = [
    "123",
    "abc",
]


def validate_ingredients(ingredients: str) -> list[str]:
    ingredients = [s.strip() for s in ingredients.strip().split(",") if s.strip()]
    if not ingredients:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No ingredients provided",
        )
    return ingredients


def validate_api_key(api_key: str) -> str:
    if api_key not in FAKE_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return api_key
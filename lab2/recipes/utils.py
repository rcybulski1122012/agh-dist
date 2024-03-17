def is_user_error(status_code: int) -> bool:
    return 400 <= status_code < 500

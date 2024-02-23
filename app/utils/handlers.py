from fastapi import HTTPException, status


def not_found_exception():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found: Invalid id")


def credentials_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

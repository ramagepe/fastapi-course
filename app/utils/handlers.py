from fastapi import HTTPException, status


def not_found_exception(msg: str = "Not found: Invalid id"):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=msg)


def unauthorized_exception(msg: str = "Could not validate credentials"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden_exception(msg: str = "Not authorized to do requested action"):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=msg)


def locked_exception(msg: str = "This action is locked"):
    raise HTTPException(
        status_code=status.HTTP_423_LOCKED,
        detail=msg)

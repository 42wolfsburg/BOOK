from typing import Annotated
from fastapi import Cookie, Depends, HTTPException
import jwt
from config import settings

async def get_current_user(session: Annotated[str | None, Cookie()] = None) -> dict:
    if session is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        return jwt.decode(session, key=settings.JWT_SECRET, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise HTTPException(status_code=401, detail=str(e))
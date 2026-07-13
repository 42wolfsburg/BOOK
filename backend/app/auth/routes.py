import secrets
import httpx
import jwt
from typing import Annotated
from urllib.parse import urlencode
from loguru import logger
from fastapi import APIRouter, status, HTTPException, Request, Response, Cookie, Depends
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta, timezone

from .auth import get_current_user
from config import settings

auth_router = APIRouter()

FT_AUTH_URL  = "https://api.intra.42.fr/oauth/authorize"
FT_TOKEN_URL = "https://api.intra.42.fr/oauth/token"
FT_USER_URL  = "https://api.intra.42.fr/v2/me"

@auth_router.get("/me", status_code=200) #check already authenticated user
async def me(user: Annotated[dict, Depends(get_current_user)]):
	return {
		"login": user["login"],
		"is_staff": user["is_staff"]
	}

@auth_router.get("/login", status_code=302) #redirect HTTP code
async def login():
	state = secrets.token_urlsafe(32)

	auth_url = FT_AUTH_URL + "?" + urlencode({
		"client_id":		settings.CLIENT_ID,
		"redirect_uri":		settings.REDIRECT_URI,
		"response_type":	"code",
		"scope":			"public",
		"state":			state
	})

	response = RedirectResponse(url=auth_url, status_code=302)
	response.set_cookie(
		key="oauth_state",
		value=state,
		httponly=True,
		secure=True,
		samesite="lax",
		max_age=500
	)

	return response

@auth_router.get("/logout", status_code=200)
async def logout(response: Response):
	response.delete_cookie(
		key="session",
		httponly=True,
		samesite="lax"
	)
	return {"message": "logged out"}

@auth_router.get("/callback", status_code=302) #redirect HTTP code
async def callback(request: Request, code: str, state: str):
	stored_state = request.cookies.get("oauth_state")
	if not stored_state or stored_state != state:
		raise HTTPException(status_code=400, detail="Invalid code")
	
	try:
		async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=30.0)) as client:
			token_res = await client.post(FT_TOKEN_URL, data={
				"grant_type":		"authorization_code",
				"client_id":		settings.CLIENT_ID,
				"client_secret":	settings.SECRET,
				"code":				code,
				"redirect_uri":		settings.REDIRECT_URI,
			})

		if token_res.status_code != 200:
			raise HTTPException(status_code=400, detail="Failed to exchange code")

		ft_access_token = token_res.json()["access_token"]

		async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=30.0)) as client:
			user_res = await client.get(
				FT_USER_URL,
				headers={"Authorization": f"Bearer {ft_access_token}"}
			)

		if user_res.status_code != 200:
			raise HTTPException(status_code=400, detail="Failed to fetch user")

		user = user_res.json()

		session_token = jwt.encode(
			payload={
				"sub":		str(user["id"]),
				"login":	user["login"],
				"is_staff":	user["staff?"],
				"exp":		datetime.now(timezone.utc) + timedelta(days=7)
			},
			key=settings.JWT_SECRET,
			algorithm="HS256"
		)
		response = RedirectResponse(url=settings.FRONTEND_URL, status_code=302)
		response.set_cookie(
			key="session",
			value=session_token,
			httponly=True,
			secure=False, # change in prod
			samesite="lax",
			max_age=60*60*24*7
		)
		response.delete_cookie("oauth_state")
		return response
	except httpx.TimeoutException:
		logger.error("Timeout during token exchange with 42")
		return RedirectResponse(
			url=f"{settings.FRONTEND_URL}/login?error=timeout",
			status_code=302
		)

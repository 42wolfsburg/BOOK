import secrets
import httpx
import jwt
from uuid import UUID
from typing import Annotated
from urllib.parse import urlencode
from loguru import logger
from fastapi import APIRouter, status, HTTPException, Request, Cookie
from fastapi.responses import RedirectResponse
from datetime import datetime, timedelta, timezone

from ..rooms import service
from config import settings
from ..models.schemas import BookingRequest, BookingCreation, RoomName

router = APIRouter()
response = {}

FT_AUTH_URL  = "https://api.intra.42.fr/oauth/authorize"
FT_TOKEN_URL = "https://api.intra.42.fr/oauth/token"
FT_USER_URL  = "https://api.intra.42.fr/v2/me"

@router.get("/", status_code=status.HTTP_200_OK)
async def root():
	logger.info("Received request from root")
	return ({
		"title": "BOOK",
		"version": "1.0.0",
		"Author": "42Wolfsburg",
		"status": "development"
	})


@router.get("/auth/me", status_code=200) #check already authenticated user
async def me(jwt_token: Annotated[str | None, Cookie()] = None):
	if jwt_token is None:
		raise HTTPException(status_code=401)
	parsed_token = jwt.decode(jwt_token)
	return parsed_token

@router.get("/auth/login", status_code=302) #redirect HTTP code
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
		secure=False, #Change in prod
		samesite="lax",
		max_age=500
	)

	return response

@router.get("/auth/callback", status_code=302) #redirect HTTP code
async def callback(request: Request, code: str, state: str):
	stored_state = request.cookies.get("oauth_state")
	if not stored_state or stored_state != state:
		raise HTTPException(status_code=400, detail="Invalid code")
	
	async with httpx.AsyncClient() as client:
		token_res = await client.post(FT_TOKEN_URL, data={
			"grant_type":		"authorization_code",
			"client_id":		settings.CLIENT_ID,
			"client_secret":	settings.SECRET,
			"code":				code,
			"redirect_uri":		settings.REDIRECT_URI,
		})
	
	if token_res.status_code != 200:
		print(token_res.status_code)
		print(token_res.text)
		raise HTTPException(status_code=400, detail="Failed to exchange code")
	
	ft_access_token = token_res.json()["access_token"]

	async with httpx.AsyncClient() as client:
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
		secure=False, # Change in prod
		samesite="lax",
		max_age=60*60*24*7
	)
	response.delete_cookie("oauth_state")

	return response

@router.get("/api/rooms")
async def rooms():
	return await service.get_all_bookings()

@router.get("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_200_OK)
async def booking(
	room_name: RoomName,
	id: UUID
	) -> dict:
	"""
	booking data request

	status: default 202, success 200, fail 400
	"""
	try:
		response["resource"] = await service.get_booking(
			room_name=room_name,
			id=id
			)
	except Exception as err:
		raise HTTPException(status_code=404, detail=str(err))
	return response

@router.get("/api/rooms/{room_name}/bookings", status_code=status.HTTP_200_OK)
async def booking(room_name: RoomName) -> dict:
	"""
	booking data request

	status: default 202, success 200, fail 400
	"""
	try:
		response["resource"] = await service.get_booking_per_room(room_name=room_name)
	except Exception as err:
		raise HTTPException(status_code=404, detail=str(err))
	return response

@router.post("/api/rooms/{room_name}/bookings", status_code=status.HTTP_201_CREATED)
async def booking(
	room_name: RoomName,
	pl: BookingCreation
	) -> dict:
	"""
	booking request

	status: default 202, success 201, slot used 502, other 400
	"""
	try:
		response["resource"] = await service.register_booking(
			intra=pl.intra,
			room_name=room_name,
			begin_at=pl.begin_at,
			end_at=pl.end_at
			)
		return response	
	except Exception as err:
		raise HTTPException(status_code=400, detail=str(err))


#TODO include payload in call
@router.patch("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_201_CREATED)
async def booking(
	room_name: RoomName, 
	pl: BookingRequest,
	# RFC 4122 states that UUIDs are a standard size/length of 36
	# id: str = Field(..., min_length=16, max_length=128)
	id: UUID #= Path(..., min_length=36, max_length=36)
	) -> dict:
	"""
	booking patch

	status: default 202, success 200, fail 400
	"""
	try:
		response["resource"] = await service.update_booking(
			room_name,
			begin_at=pl.begin_at,
			end_at=pl.end_at,
			id=id
			)
		return response
	except Exception as err:
		raise HTTPException(status_code=400, detail=str(err))

@router.delete("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def booking(
	room_name: RoomName,
	# RFC 4122 states that UUIDs are a standard size/length of 36
	# id: str = Field(..., min_length=16, max_length=128)
	id: UUID #= Path(..., min_length=36, max_length=36)
	) -> None:
	"""
	booking delete

	status: always 204
	"""
	try:
		response["resource"] = await service.delete_booking(
			room_name=room_name, 
			id=id
			)
	except Exception as err:
		response["error"] = err
	return response

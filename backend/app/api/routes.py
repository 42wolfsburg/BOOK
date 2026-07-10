from uuid import UUID
from typing import Annotated
from urllib.parse import urlencode
from loguru import logger
from fastapi import APIRouter, status, HTTPException, Request, Response, Cookie, Depends

from ..rooms import service
from ..auth.auth import get_current_user
from config import settings
from ..models.schemas import BookingRequest, BookingCreation, RoomName

api_router = APIRouter()

@api_router.get("/", status_code=status.HTTP_200_OK)
async def root():
	logger.info("Received request from root")
	return ({
		"title": "BOOK",
		"version": "1.0.0",
		"Author": "42Wolfsburg",
		"status": "development"
	})


# @api_router.get("/rooms")
# async def rooms():
# 	return await service.get_all_bookings()

@api_router.get("/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_200_OK)
async def booking(
	room_name: RoomName,
	id: UUID
	) -> dict:
	"""
	booking data request

	status: default 202, success 200, fail 400
	"""
	try:
		resource = await service.get_booking(
			room_name=room_name,
			id=id
			)
		return {"resource": resource}
	except Exception as err:
		raise HTTPException(status_code=404, detail=str(err))

@api_router.get("/rooms/{room_name}/bookings", status_code=status.HTTP_200_OK)
async def booking(room_name: RoomName) -> dict:
	"""
	booking data request

	status: default 202, success 200, fail 400
	"""
	try:
		resource = await service.get_booking_per_room(room_name=room_name)
		if resource is None:
			raise HTTPException(status_code=201, detail=str(err))
		return { "resource": resource }
	except Exception as err:
		raise HTTPException(status_code=404, detail=str(err))

@api_router.post("/rooms/{room_name}/bookings", status_code=status.HTTP_201_CREATED)
async def booking(
	room_name: RoomName,
	pl: BookingCreation,
	user: Annotated[dict, Depends(get_current_user)]
	) -> dict:
	"""
	booking request

	status: default 202, success 201, slot used 502, other 400
	"""
	try:
		resource = await service.register_booking(
			intra=user['login'],
			room_name=room_name,
			begin_at=pl.begin_at,
			end_at=pl.end_at,
			is_staff=user['is_staff']
			)
		return { "resource": resource }
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))

@api_router.patch("/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_201_CREATED)
async def booking(
	room_name: RoomName, 
	pl: BookingRequest,
	id: UUID
	) -> dict:
	"""
	booking patch

	status: default 202, success 200, fail 400
	"""
	try:
		resource = await service.update_booking(
			room_name,
			begin_at=pl.begin_at,
			end_at=pl.end_at,
			id=id
			)
		return { "resource": resource }
	except Exception as err:
		raise HTTPException(status_code=400, detail=str(err))

@api_router.delete("/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def booking(
	room_name: RoomName,
	id: UUID,
	user: Annotated[dict, Depends(get_current_user)]
	) -> None:
	"""
	booking delete

	status: always 204 (not really true)
	"""
	try:
		await service.delete_booking(
			room_name=room_name,
			id=id,
			login=user['login'],
			is_staff=user['is_staff']
			)
	except PermissionError as e:
		raise HTTPException(status_code=403, detail=str(e))
	except Exception as e:
		raise HTTPException(status_code=204, detail=str(e))

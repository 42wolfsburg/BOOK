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
		"status": "production"
	})

@api_router.get("/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def booking(
	room_name: RoomName,
	id: UUID
	) -> dict:
	"""
	Endpoint responsible for retrieving bookings by ID. This specific endpoint is useful
	when you need to retrieve just one booking.

	:Parameters:
	------------
	room_name: RoomName
		In content, this is just a string that should match our list of meeting room names.

	id: UUID
		General UUID provided by the frontend.

	:Returns:
	---------
	resource: dict
		All information regarding that specific booking.
	"""
	try:
		resource = await service.get_booking(
			room_name=room_name,
			id=id
			)
		return {"resource": resource}
	except PermissionError as e:
		logger.error(str(e))
		raise HTTPException(status_code=403, detail=str(e))
	except Exception as err:
		logger.error(str(e))
		raise HTTPException(status_code=404, detail=str(err))

@api_router.get("/rooms/{room_name}/bookings", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_user)])
async def booking(room_name: RoomName) -> dict:
	"""
	Endpoint responsible for retrieving bookings of specific meeting room. It retrieves
	everything that that specific meeting room has in the database for future bookings.
	Old bookings are not retrieved as they are dead data and are scheduled for deletion.

	:Parameters:
	------------
	room_name: RoomName
		In content, this is just a string that should match our list of meeting room names.

	:Returns:
	---------
	resource: dict
		All bookings from that specific meeting room.
	"""
	try:
		resource = await service.get_booking_per_room(room_name=room_name)
		if resource is None:
			raise HTTPException(status_code=201, detail=str(err))
		return { "resource": resource }
	except PermissionError as e:
		logger.error(str(e))
		raise HTTPException(status_code=403, detail=str(e))
	except Exception as e:
		logger.error(str(e))
		raise HTTPException(status_code=404, detail=str(e))

@api_router.post("/rooms/{room_name}/bookings", status_code=status.HTTP_201_CREATED)
async def booking(
	room_name: RoomName,
	pl: BookingCreation,
	user: Annotated[dict, Depends(get_current_user)]
	) -> dict:
	"""
	Endpoint responsible for saving one booking of specific meeting room. 

	:Parameters:
	------------
	room_name: RoomName
		In content, this is just a string that should match our list of meeting room names.

	:Returns:
	---------
	resource: dict
		Payload with data pertaining to the specific booking from that meeting room.
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
	except PermissionError as e:
		logger.error(str(e))
		raise HTTPException(status_code=403, detail=str(e))
	except Exception as e:
		logger.error(str(e))
		raise HTTPException(status_code=400, detail=str(e))

@api_router.patch("/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def booking(
	room_name: RoomName,
	pl: BookingRequest,
	id: UUID
	) -> dict:
	"""
	Endpoint responsible for patching specific bookings. It is not being currently used by
	frontend, but everything in this part of the stack is wired for it to work in case it
	would be used.

	:Parameters:
	------------
	room_name: RoomName
		In content, this is just a string that should match our list of meeting room names.

	id: UUID
		General UUID provided by the frontend.

	:Returns:
	---------
	resource: dict
		Updated information regarding booking
	"""
	try:
		resource = await service.update_booking(
			room_name,
			begin_at=pl.begin_at,
			end_at=pl.end_at,
			id=id
			)
		return { "resource": resource }
	except PermissionError as e:
		logger.error(str(e))
		raise HTTPException(status_code=403, detail=str(e))
	except Exception as err:
		logger.error(str(e))
		raise HTTPException(status_code=400, detail=str(err))

@api_router.delete("/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def booking(
	room_name: RoomName,
	id: UUID,
	user: Annotated[dict, Depends(get_current_user)]
	) -> None:
	"""
	Endpoint responsible for deletion of bookings. Nothing is returned as this is the industry
	standard and REST architecture compliance method.

	:Parameters:
	------------
	room_name: RoomName
		In content, this is just a string that should match our list of meeting room names.

	id: UUID
		General UUID provided by the frontend.
	"""
	try:
		await service.delete_booking(
			room_name=room_name,
			id=id,
			login=user['login'],
			is_staff=user['is_staff']
			)
	except PermissionError as e:
		logger.error(str(e))
		raise HTTPException(status_code=403, detail=str(e))
	except Exception as e:
		logger.error(str(e))
		raise HTTPException(status_code=204, detail=str(e))

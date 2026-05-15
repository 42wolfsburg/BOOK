from loguru import logger
from fastapi import APIRouter, status, Response
from pydantic import ValidationError

from ..rooms.service import crud
from ..rooms import service
from ..models.schemas import BookingRequest, BookingCreation, RoomName, Id

router = APIRouter()
response = {}

@router.get("/", status_code=status.HTTP_200_OK)
async def root():
	logger.info("Received request from root")
	return ({
		"title": "BOOK",
		"version": "1.0.0",
		"Author": "42Wolfsburg",
		"status": "development"
	})

@router.get("/rooms")
async def rooms():
	return crud.db_get_all_bookings()


@router.get("/api/rooms/{room_name}/bookings", status_code=status.HTTP_200_OK)
async def booking(
	room_name: RoomName,
	pl: BookingRequest
	) -> dict:
	"""
	booking data request

	status: default 202, success 200, fail 400
	"""
	try:
		response["resource"] = await service.get_booking(pl.id)
		response["status"] = status.HTTP_200_OK
		return 
	except Exception as err:
		response["status"] = status.HTTP_400_BAD_REQUEST
		response["error"] = err
	return response

#TODO include payload in call
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
		["resource"] = await service.register_booking(
			intra=pl.intra,
			room_name=room_name,
			begin_at=str(pl.begin_at),
			end_at=str(pl.end_at)
			)
		# response = status.HTTP_201_CREATED
	except ValidationError as err:
		response["status"] = status.HTTP_400_BAD_REQUEST
	except Exception as err:
		response["status"] = status.HTTP_502_BAD_GATEWAY
		response["error"] = err
	return response	

#TODO include payload in call
@router.patch("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_201_CREATED)
async def booking(
	room_name: RoomName, 
	id: Id, 
	pl: BookingRequest
	) -> dict:
	"""
	booking patch

	status: default 202, success 200, fail 400
	"""
	try:
		response["resource"] = await service.update_booking(
			begin_at=str(pl.begin_at),
			end_at=str(pl.end_at),
			id=id
			)
	except ValidationError as err:
		response["status"] = status.HTTP_400_BAD_REQUEST
		response["error"] = err
	return response

@router.delete("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def booking(
	room_name: RoomName, id: Id
	) -> dict:
	"""
	booking delete

	status: always 204
	"""
	try:
		response["resource"] = await service.delete_booking(id=id)
	except Exception as err:
		response["error"] = err
	return response

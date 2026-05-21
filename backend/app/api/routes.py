from loguru import logger
from fastapi import APIRouter, status, Path, HTTPException
from pydantic import ValidationError
from uuid import UUID
# from ..rooms.service import crud
from ..rooms import service
from ..models.schemas import BookingRequest, BookingCreation, RoomName

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
		response["resource"] = await service.get_booking(room_name, id)
		response["status"] = status.HTTP_200_OK
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
	# id: Id, 
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
	except ValidationError as err:
		response["status"] = status.HTTP_400_BAD_REQUEST
		response["error"] = err
	return response

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
		response["resource"] = await service.delete_booking(id=id)
	except Exception as err:
		response["error"] = err
	return response

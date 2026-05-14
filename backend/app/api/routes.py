from loguru import logger
from fastapi import APIRouter, status, Response
from pydantic import ValidationError

from ..rooms.service import crud
from ..rooms import service

from .base_payload import BookingRequest

router = APIRouter()
err = ""

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

#TODO id / room_name discreptancy
@router.get("/api/rooms/{room_name}/bookings", status_code=status.HTTP_202_ACCEPTED)
async def get_room(room_name: str, response: Response, pl: BookingRequest): 
	"""
	booking data request

	status: default 202, success 200, fail 400
	"""
	try:
		service.get_booking()
		response.status_code = status.HTTP_200_OK
	except Exception as err:
		response.status_code = status.HTTP_400_BAD_REQUEST
	finally:
		return err

#TODO include payload in call
@router.post("/api/rooms/{room_name}/bookings", status_code=status.HTTP_202_ACCEPTED)
async def post_room(room_name: str, response: Response, pl: BookingRequest):
	"""
	booking request

	status: default 202, success 201, slot used 502, other 400
	"""
	try:
		service.register_booking(intra=pl.intra ,room_name=room_name, begin_at=str(pl.begin_at), end_at=str(pl.end_at))
		response.status_code = status.HTTP_201_CREATED
	except ValidationError as err:
		response.status_code = status.HTTP_400_BAD_REQUEST
	except Exception as err:
		response.status_code = status.HTTP_502_BAD_GATEWAY
	finally:
		return err
		

#TODO include payload in call
@router.patch("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_202_ACCEPTED)
async def patch_room(room_name: str, id: str, response: Response, pl: BookingRequest):
	"""
	booking patch

	status: default 202, success 200, fail 400
	"""
	try:
		service.update_booking(begin_at=str(pl.begin_at), end_at=str(pl.end_at) ,id=id)
		response.status_code = status.HTTP_200_OK
	except ValidationError as err:
		response.status_code = status.HTTP_400_BAD_REQUEST
	finally:
		return err

@router.delete("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_name: str, id: str, response: Response):
	"""
	booking delete

	status: always 204
	"""
	try:
		service.delete_booking(id=id)
	except Exception as err:
		pass
	finally:
		return err
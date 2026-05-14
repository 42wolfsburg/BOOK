from loguru import logger
from fastapi import APIRouter, status, Response

from ..rooms.service import crud
from ..rooms import service

router = APIRouter()

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
async def get_room(room_name: str, response: Response):
	"""
	booking data request

	status: default 202, success 200, fail 400
	"""
	service.get_booking()

#TODO include payload in call
@router.post("/api/rooms/{room_name}/bookings", status_code=status.HTTP_202_ACCEPTED)
async def post_room(room_name: str, response: Response):
	"""
	booking request

	status: default 202, success 201, slot used 502, other 400
	"""
	try:
		service.register_booking(room_name=room_name)
	finally:
		response.status_code = status.HTTP_201_CREATED

#TODO include payload in call
@router.patch("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_202_ACCEPTED)
async def patch_room(room_name: str, id: str, response: Response):
	"""
	booking patch

	status: default 202, success 200, fail 400
	"""
	try:
		service.update_booking(id=id) 
	finally:
		response.status_code = status.HTTP_200_OK

@router.delete("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_name: str, id: str, response: Response):
	"""
	booking delete

	status: always 204
	"""
	service.delete_booking(id=id)
	return
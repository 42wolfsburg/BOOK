from loguru import logger
from fastapi import APIRouter, status, Response
from ..rooms.repository import crud

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

@router.get("/api/rooms/{room_name}/bookings", status_code=status.HTTP_202_ACCEPTED)
async def get_room(room_name: str, response: Response):
	return({
		"name": room_name
		 })

@router.post("/api/rooms/{room_name}/bookings", status_code=status.HTTP_202_ACCEPTED)
async def post_room(room_name: str, response: Response):
	return ({
		"result": "👍"
    })

@router.patch("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_202_ACCEPTED)
async def patch_room(room_name: str, id: str, response: Response):
	pass

@router.delete("/api/rooms/{room_name}/bookings/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_name: str, id: str, response: Response):
	pass
from loguru import logger
from fastapi import APIRouter, status
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
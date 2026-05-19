from typing import Any, Optional
from time import time

from pydantic import BaseModel, Field, model_validator, ValidationError

unix_hour: float = 3600
unix_month: float = 2629743
meeting_rooms = [
	"space",
	"swimming-pool",
	"space-invader",
	"gallery"
]

class RoomName(BaseModel):
	room_name: str = Field(..., min_length=4, max_length=15)

	@model_validator(mode="after")
	def validate(self):
		if (self.room_name.strip()).lower() not in meeting_rooms:
			raise ValidationError("room_name invalid name")


class Id(BaseModel):
	id: str = Field(..., min_length=16, max_length=128)

class BookingRequest(BaseModel):
	id: Id
	intra: str = Field(..., min_length=1, max_length=10)
	begin_at: float = Field(..., ge=time(), le=(time() + (unix_month * 3)))
	end_at: float = Field(..., ge=begin_at, le=(begin_at + (unix_hour * 3)))

class BookingCreation(BaseModel):
	intra: str = Field(..., min_length=1, max_length=10)
	begin_at: float = Field(..., ge=time(), le=(time() + (unix_month * 3)))
	end_at: float = Field(..., ge=begin_at, le=(begin_at + (unix_hour * 3)))

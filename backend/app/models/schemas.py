from typing import Any, Optional
from time import time
from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError

unix_hour: float = 3600
unix_month: float = 2629743

# meeting_rooms = [
# 	"space",
# 	"swimming-pool",
# 	"space-invader",
# 	"gallery"
# ]

# FastAPI path parameters have to be scalar: int, str, float, bool, or UUID. Our schema will never work.
# class RoomName(BaseModel):
# 	room_name: str = Field(..., min_length=4, max_length=15)

# 	@model_validator(mode="after")
# 	def validate(self):
# 		if (self.room_name.strip()).lower() not in meeting_rooms:
# 			raise ValidationError("room_name invalid name")

class RoomName(str, Enum):
	space = "space"
	piscine = "piscine"
	space_invader = "space-invader"
	gallery = "gallery"

# Same issue as RoomName. It has to be scalar and over here we are creating it's own type.
# class Id(BaseModel):
# 	id: str = Field(..., min_length=16, max_length=128)

class BookingRequest(BaseModel):
	intra: str = Field(..., min_length=1, max_length=10)
	# Field() only takes static values. We can't do arithmetic operations in it.
	# begin_at: float = Field(..., ge=time(), le=(time() + (unix_month * 3)))
	# end_at: float = Field(..., ge=begin_at, le=(begin_at + (unix_hour * 3)))
	begin_at: float = Field(...)
	end_at: float = Field(...)

	@model_validator(mode="after")
	def validate(self) -> 'BookingRequest':
		if self.end_at < self.begin_at:
			raise ValueError("end_at must be >= begin_at")
		if self.end_at > self.begin_at + (unix_hour * 3):
			raise ValueError("end_at must be within three hours of begin_at")
		return self


class BookingCreation(BaseModel):
	intra: str = Field(..., min_length=1, max_length=10)
	# begin_at: float = Field(..., ge=time(), le=(time() + (unix_month * 3)))
	# end_at: float = Field(..., ge=begin_at, le=(begin_at + (unix_hour * 3)))
	begin_at: float = Field(...)
	end_at: float = Field(...)

	@model_validator(mode="after")
	def validate(self) -> 'BookingRequest':
		if self.end_at < self.begin_at:
			raise ValueError("end_at must be >= begin_at")
		if self.end_at > self.begin_at + (unix_hour * 3):
			raise ValueError("end_at must be within three hours of begin_at")
		return self

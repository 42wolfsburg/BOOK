from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Any, Optional
from time import time
from enum import Enum

unix_hour: float = 3600
unix_month: float = 2629743

class RoomName(str, Enum):
	space = "space"
	piscine = "piscine"
	space_invader = "space-invader"
	gallery = "gallery"

class BookingRequest(BaseModel):
	intra: str
	begin_at: int
	end_at: int

	@field_validator("begin_at", "end_at")
	@classmethod
	def must_be_valid_timestamp(cls, v: int) -> int:
		if v < 0:
			raise ValueError("Timestamp cannot be negative")
		if v > 9_999_999_999:  # year ~2286, reasonable upper bound
			raise ValueError("Timestamp is unrealistically large")
		return v

	@field_validator("end_at")
	@classmethod
	def end_must_be_after_begin(cls, v: int, info) -> int:
		begin = info.data.get("begin_at")
		if begin is not None and v <= begin:
			raise ValueError("end_at must be after begin_at")
		return v

class BookingCreation(BaseModel):
	intra: str = Field(..., min_length=1, max_length=10)
	begin_at: float = Field(...)
	end_at: float = Field(...)

	@model_validator(mode="after")
	def validate(self) -> 'BookingRequest':
		if self.end_at < self.begin_at:
			raise ValueError("end_at must be >= begin_at")
		if self.end_at > self.begin_at + (unix_hour * 3):
			raise ValueError("end_at must be within three hours of begin_at")
		return self

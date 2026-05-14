from typing import Any, Optional
from time import time

from pydantic import BaseModel, Field, model_validator, ValidationError

unix_hour: float = 3600
unix_month: float = 2629743

class BookingRequest(BaseModel):
	intra: str = Field(..., min_length=1, max_length=10)
	begin_at: float = Field(..., ge=time(), le=(time() + (unix_month * 3)))
	end_at: float = Field(..., ge=begin_at, le=(begin_at + (unix_hour * 3)))

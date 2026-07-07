from ..rooms.repository import crud
from uuid import UUID

db = crud()

async def register_booking(
	intra: str,
	room_name: str,
	begin_at: int,
	end_at: int
	) -> dict:
	"""
	Function responsible for registration of booking. The same registration is
	responsible for informing the uuid that will be used for updating, getting,
	and deleting said booking.

	:Parameters:
	------------
	intra: str
		42 intra login that should be informed by 42API

	room_name: str
		Name of the meeting room

	begin_at: str
		UNIX timestamp regarding beginning of booking.
	
	end_at: str
		UNIX timestamp regarding end of booking.

	:Returns:
	---------
	resource: dict
		Resource following API REST architectural standards for GET.
		Contains all information about the booking: starting and end time,
		intra, name of the room in which booking is taking place, and 
		boolean value indicating if it's a staff member or not.
	
	"""
	resource: dict = db.db_insert_booking(intra, room_name, begin_at, end_at)

	return resource

async def delete_booking(
	room_name:str, 
	id: UUID
	) -> None:
	"""
	Function responsible for deletion of bookings. According to REST architecture
	we should not return anything, as the action itself is a result of deletion of
	the same resource. Additionally, for security purposes we should not confirm nor
	deny exclusion of resource to avoid usage of endpoint for malicious purposes.

	:Parameters:
	------------
	id: str
		UUID provideed during the registration of booking.
	"""
	db.db_delete_booking(room_name, id)

async def update_booking(
	room_name: str,
	id: UUID, 
	begin_at: int,
	end_at: int
	) -> dict:
	"""
	Function responsible for intermediating database call for in a service layer.

	:Parameters:
	------------
	id: UUID
		UUID provided during the registration of booking.
	
	begin_at: int
		UNIX timestamp regarding beginning of booking.
	
	end_at: int
		UNIX timestamp regarding end of booking.

	:Returns:
	---------
	resource: dict
		Dictionary containing updated booking following REST architecture.
	"""
	resource: dict = db.db_update_booking(room_name, id, begin_at, end_at)
	return resource

async def get_booking(
	room_name: str,
	id: UUID
	) -> dict:
	"""
	Function responsible for returning specific booking according to a correct ID
	provided during registration of the same.

	:Parameters:
	------------
	id: str
		UUID provided during the registration of booking.

	:Returns:
	---------
	resource: dict
		Resource following API REST architectural standards for GET.
		Contains all information about the booking: starting and end time,
		intra, name of the room in which booking is taking place, and 
		boolean value indicating if it's a staff member or not.
	"""
	resource: dict = db.db_get_booking(room_name, id)
	return resource

async def get_booking_per_room(room_name: str) -> dict:
	"""
	Function responsible for returning specific booking according to a correct ID
	provided during registration of the same.

	:Parameters:
	------------
	id: str
		UUID provided during the registration of booking.

	:Returns:
	---------
	resource: dict
		Resource following API REST architectural standards for GET.
		Contains all information about the booking: starting and end time,
		intra, name of the room in which booking is taking place, and 
		boolean value indicating if it's a staff member or not.
	"""
	resource: dict = db.db_get_booking_per_room(room_name)
	return resource

async def get_all_bookings() -> dict:
	"""
	NOT SUPPOSED TO BE DEPLOYED! MOSTLY FOR TESTING PURPOSES
	"""
	resource = db.db_get_all_bookings()
	return resource
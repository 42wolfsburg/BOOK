from loguru import logger
from uuid import UUID
from fastapi import HTTPException
from ..database.init import get_pool

class crud:
	def db_insert_booking(
		self, 
		intra: str,
		room_name: str, 
		begin_at: int, 
		end_at: int,
		is_staff: bool
		) -> dict:
		"""
		CRUD operation responsible for insertion of booking resource in database.

		:Parameters:
		------------
		intra: str
			Intra login of student/staff in string format.

		room_name: str
			Name of specific meeting room. Meeting rooms names must be hardcoded.

		begin_at: int
			UNIX timestamp specifying beginning of booking.

		end_at: int
			UNIX timestamp specifying end of booking.

		is_staff: bool
			Boolean identifying user as staff or not.

		:Returns:
		---------
		resource: dict
			Confirmation of booking in key value format.
		"""
		logger.info(f"New insertion for {intra}")
		conn = get_pool().getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				INSERT INTO bookings (intra, room_name, begin_at, end_at)
				VALUES (%s, %s, to_timestamp(%s), to_timestamp(%s))
				RETURNING id, intra, room_name, begin_at, end_at, is_staff
				""",
				(intra, room_name, begin_at, end_at, is_staff)
				)
				row = cursor.fetchone()
				column = [desc[0] for desc in cursor.description]
				resource = dict(zip(column, row))
			conn.commit()
			return resource
		finally:
			get_pool().putconn(conn)

	def db_get_booking_per_room(
		self,
		room_name: str
		) -> list:
		"""
		CRUD operation for getting booking resource from specific meeting rooms.

		:Parameters:
		------------
		room_name: str
			Name of specific meeting room. Meeting rooms names must be hardcoded 
		
		:Returns:
		---------
		resource: dict
			Resulting resource from CRUD interaction.
		"""
		logger.info(f"Retrieving info from database from room:{room_name}")
		conn = get_pool().getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				SELECT id, begin_at, end_at, intra, is_staff
				FROM bookings
				WHERE room_name = %s
				""", (room_name,))
				rows = cursor.fetchall()
				column = [desc[0] for desc in cursor.description]
				resource = [dict(zip(column, r)) for r in rows]
				# resource = dict(zip(column, row))
			return resource
		finally:
			get_pool().putconn(conn)

	def db_delete_booking(
		self, 
		id: UUID
		) -> None:
		"""
		CRUD operation responsible for deletion of booking resource.

		:Parameters:
		------------
		id: UUID
			Unique ID given during booking operation.
		
		:Returns:
		---------
		None
		"""
		logger.info(f"Deletion for id: {id}")
		conn = get_pool().getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				DELETE FROM bookings
				WHERE id = %s
				""", (str(id),))
			conn.commit()
		finally:
			get_pool().putconn(conn)


	def db_update_booking(
		self,
		room_name: str,
		id: UUID,
		begin_at: int,
		end_at: int
		) -> dict:
		"""
		CRUD operation responsible for updating booking resource.

		:Parameters:
		------------
		room_name: str
			Name of specific meeting room. Meeting rooms names must be hardcoded 

		id: UUID
			Unique ID given during booking operation.
					
		begin_at
			UNIX timestamp specifying beginning of booking

		end_at
			UNIX timestamp specifying end of booking

		:Returns:
		---------
		"""
		logger.info(f"Updating event for id: {id}")
		conn = get_pool().getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				UPDATE bookings
				SET begin_at = to_timestamp(%s), end_at = to_timestamp(%s)
				WHERE id = %s AND room_name = %s
				RETURNING id, intra, room_name, begin_at, end_at, is_staff
				""", (begin_at, end_at, str(id), room_name))
				row = cursor.fetchone()
				if row is None:
					raise HTTPException(status_code=404, detail={"Booking not found."})
				column = [desc[0] for desc in cursor.description]
				resource = dict(zip(column, row))
			conn.commit()
			print("here in repository")
			return resource
		finally:
			get_pool().putconn(conn)


	def db_get_booking(
		self,
		room_name: str,
		id: UUID
		) -> list:
		"""
		"""
		logger.info(f"GET called for id: {id}")
		conn = get_pool().getconn()
		try:
			print("here in repository")
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				SELECT begin_at, end_at, intra, is_staff
				FROM bookings
				WHERE id = %s
				AND room_name = %s
				""", (str(id), room_name))
				row = cursor.fetchone()
				if row is None:
					raise HTTPException(status_code=404, detail={"Booking not found."})
				column = [desc[0] for desc in cursor.description]
				resource = dict(zip(column, row))
			return resource

		finally:
			get_pool().putconn(conn)


	def db_get_all_bookings(self) -> dict:
		"""
		"""
		conn = get_pool().getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute("SELECT * FROM bookings;")
				return cursor.fetchall()
		finally:
			get_pool().putconn(conn)

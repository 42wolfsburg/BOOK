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
		end_at: int
		) -> dict:
		"""
		:Parameters:
		------------
		intra: str

		room_name: str

		begin_at

		end_at

		:Returns:
		---------
		
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
				(intra, room_name, begin_at, end_at)
				)
				row = cursor.fetchone()
				column = [desc[0] for desc in cursor.description]
				resource = dict(zip(column, row))
			conn.commit()
			return resource
		finally:
			get_pool().putconn(conn)


	def db_delete_booking(
		self, 
		id: UUID
		) -> None:
		"""
		"""
		logger.info(f"Deletion for id: {id}")
		conn = get_pool().getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				DELETE FROM bookings
				WHERE id = $1
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
		:Parameters:
		------------
		intra: str

		room_name: str

		begin_at

		end_at

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
				SET begin_at = $1, end_at = $2
				WHERE id = $3 AND room_name = $4
				RETURNING id, intra, room_name, begin_at, end_at, is_staff
				""", begin_at, end_at, str(id), room_name)
			conn.commit()
		finally:
			get_pool().putconn(conn)


	def db_get_booking(
		self,
		room_name: str,
		id: UUID
		) -> dict:
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

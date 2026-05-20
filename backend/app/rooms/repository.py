from ..database.init import connection_pool
from loguru import logger

class crud:
	def db_insert_booking(
		self, 
		intra: str,
		room_name: str, 
		begin_at: str, 
		end_at: str
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
		conn = connection_pool.getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				INSERT INTO bookings (intra, room_name, begin_at, end_at)
				VALUES ($1, $2, $3, $4)
				RETURNING id, intra, room_name, begin_at, end_at, is_staff
				""",
				intra, room_name, begin_at, end_at
				)
		finally:
			conn.commit()
			connection_pool.putconn(conn)


	def db_delete_booking(self, id: str) -> None:
		"""
		"""
		logger.info(f"Deletion for id: {id}")
		conn = connection_pool.getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				DELETE FROM bookings
				WHERE id = $1
				""", (id,))
		finally:
			conn.commit()
			connection_pool.putconn(conn)


	def db_update_booking(
		self,
		room_name: str,
		id: str,
		begin_at: str,
		end_at: str
		) -> dict:
		"""
		"""
		logger.info(f"Updating event for id: {id}")
		conn = connection_pool.getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				UPDATE bookings
				SET begin_at = $1, end_at = $2
				WHERE id = $3 AND room_name = $4
				RETURNING id, intra, room_name, begin_at, end_at, is_staff
				""", begin_at, end_at, id, room_name)
		finally:
			conn.commit()
			connection_pool.putconn(conn)


	def db_get_booking(
		self,
		room_name: str,
		id: str
		) -> dict:
		"""
		"""
		logger.info(f"GET called for id: {id}")
		conn = connection_pool.getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute(
				"""
				SELECT begin_at, end_at
				FROM bookings
				WHERE id = $1
				AND room_name = $2
				""", (id, room_name))
		finally:
			connection_pool.putconn(conn)


	def db_get_all_bookings(self) -> dict:
		"""
		"""
		conn = connection_pool.getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute("SELECT * FROM bookings;")
				return cursor.fetchall()
		finally:
			connection_pool.putconn(conn)

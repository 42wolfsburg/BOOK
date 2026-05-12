from ..database.init import connection_pool

class crud:
	def db_insert_booking(self, intra: str, begin_at, end_at):

		return

	def db_delete_booking(self, id):
		return

	def db_update_booking(self, id):
		return

	def db_get_booking(self, id):
		return

	def db_get_all_bookings(self):
		conn = connection_pool.getconn()
		try:
			with conn.cursor() as cursor:
				cursor.execute("SELECT * FROM rooms;")
				return cursor.fetchall()
		finally:
			connection_pool.putconn(conn)
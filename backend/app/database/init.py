from psycopg2 import pool
from config import settings
from pathlib import Path
import psycopg2

connection_pool: pool.SimpleConnectionPool | None = None

_SCHEMA_PATH = Path(__file__).parent / "schema.sql"

def init_db():
	global connection_pool
	connection_pool = pool.SimpleConnectionPool(
		minconn=1,
		maxconn=10,
		host=settings.POSTGRES_HOST,
		database=settings.POSTGRES_DB,
		user=settings.POSTGRES_USER,
		password=settings.POSTGRES_PASSWORD
	)
	conn = connection_pool.getconn()
	try:
		with conn.cursor() as cursor:
			cursor.execute(open("schema.sql", "r").read())
		conn.commit()
	finally:
		connection_pool.putconn(conn)
	
	return connection_pool

	def close_db():
		if connection_pool:
			connection_pool.closeall()


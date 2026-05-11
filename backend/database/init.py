from psycopg2 import pool
from config import settings

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

def close_db():
	if connection_pool:
		connection_pool.closeall()


from datetime import datetime
from config import settings
import psycopg2

def delete_past_bookings():
	conn=psycopg2.connect(
		host=settings.POSTGRES_HOST,
		database=settings.POSTGRES_DB,
		user=settings.POSTGRES_USER,
		password=settings.POSTGRES_PASSWORD
	)
	with conn.cursor() as cur:
		cur.execute("DELETE FROM bookings WHERE end_at < %s", (datetime.now(),))
	conn.commit()


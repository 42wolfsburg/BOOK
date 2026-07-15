from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header, status
from loguru import logger

from ..rooms.repository import crud
from config import settings

google_router = APIRouter()
db = crud()

@google_router.post("/webhook", status_code=status.HTTP_200_OK)
async def calendar_webhook(payload: dict, x_webhook_secret: str = Header(None)):
	"""
	Receives push notifications from each room's Apps Script trigger whenever
	the resource calendar changes — created, rescheduled, or cancelled,
	whether that happened through the app or directly in Google Calendar.
	"""
	if x_webhook_secret != settings.GOOGLE_WEBHOOK_SECRET:
		raise HTTPException(status_code=403, detail="Invalid signature")

	action = payload.get("action")
	room_name = payload.get("room_name")
	event_id = payload.get("event_id")

	if action == "deleted":
		db.db_delete_booking_by_google_event_id(event_id)
		logger.info(f"Webhook: removed booking for google event {event_id}")
		return {"status": "ok"}

	begin_at = datetime.fromtimestamp(payload["begin_at"], tz=timezone.utc)
	end_at = datetime.fromtimestamp(payload["end_at"], tz=timezone.utc)
	creator = payload.get("creator", "Unknown")

	db.db_upsert_google_booking(room_name, event_id, begin_at, end_at, creator)
	logger.info(f"Webhook: synced booking for google event {event_id}")
	return {"status": "ok"}
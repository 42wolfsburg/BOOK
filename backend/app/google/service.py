import json
import base64
from datetime import datetime, timezone
import httpx
from loguru import logger
from config import settings
from .auth import get_access_token

CALENDAR_API_BASE = "https://www.googleapis.com/calendar/v3"

def _load_credentials(b64_str: str) -> dict:
	decoded = base64.b64decode(b64_str)
	return json.loads(decoded)

ROOM_CREDENTIALS = {
	"piscine": _load_credentials(settings.GOOGLE_CREDENTIALS_PISCINE_B64),
	"galaxy": _load_credentials(settings.GOOGLE_CREDENTIALS_GALAXY_B64),
	"space-invader": _load_credentials(settings.GOOGLE_CREDENTIALS_SPACE_INVADER_B64),
	"gallery": _load_credentials(settings.GOOGLE_CREDENTIALS_GALLERY_B64),
}

# TODO: replace with each room's actual Gmail address
ROOM_CALENDAR_IDS = {
	"piscine": "meeting-piscine@42wolfsburg.de",
	"galaxy": "meeting-space@42wolfsburg.de",
	"space-invader": "meeting-spaceinvaders@42wolfsburg.de",
	"gallery": "meeting-gallery@42wolfsburg.de",
}

def _to_iso(timestamp: int) -> str:
	return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()

async def create_event(room_name: str, begin_at: int, end_at: int, summary: str = "Room booking") -> str:
	"""
	Creates an event on the given room's calendar and returns Google's event ID,
	which must be persisted (bookings.google_event_id) to allow later update/delete.
	"""
	credentials = ROOM_CREDENTIALS[room_name]
	calendar_id = ROOM_CALENDAR_IDS[room_name]
	token = await get_access_token(room_name, credentials)

	body = {
		"summary": summary,
		"start": {"dateTime": _to_iso(begin_at)},
		"end": {"dateTime": _to_iso(end_at)},
	}

	async with httpx.AsyncClient() as client:
		response = await client.post(
			f"{CALENDAR_API_BASE}/calendars/{calendar_id}/events",
			headers={"Authorization": f"Bearer {token}"},
			json=body,
		)
		response.raise_for_status()
		event = response.json()

	logger.info(f"Created Google Calendar event {event['id']} for {room_name}")
	return event["id"]

async def update_event(room_name: str, event_id: str, begin_at: int, end_at: int) -> None:
	"""
	Updates the start/end time of an existing event on the room's calendar.
	"""
	credentials = ROOM_CREDENTIALS[room_name]
	calendar_id = ROOM_CALENDAR_IDS[room_name]
	token = await get_access_token(room_name, credentials)

	body = {
		"start": {"dateTime": _to_iso(begin_at)},
		"end": {"dateTime": _to_iso(end_at)},
	}

	async with httpx.AsyncClient() as client:
		response = await client.patch(
			f"{CALENDAR_API_BASE}/calendars/{calendar_id}/events/{event_id}",
			headers={"Authorization": f"Bearer {token}"},
			json=body,
		)
		response.raise_for_status()

	logger.info(f"Updated Google Calendar event {event_id} for {room_name}")

async def delete_event(room_name: str, event_id: str) -> None:
	"""
	Deletes an event from the room's calendar. Tolerates 404 (already gone)
	so a double-delete or a stale google_event_id doesn't blow up the caller.
	"""
	credentials = ROOM_CREDENTIALS[room_name]
	calendar_id = ROOM_CALENDAR_IDS[room_name]
	token = await get_access_token(room_name, credentials)

	async with httpx.AsyncClient() as client:
		response = await client.delete(
			f"{CALENDAR_API_BASE}/calendars/{calendar_id}/events/{event_id}",
			headers={"Authorization": f"Bearer {token}"},
		)
		if response.status_code != 404:
			response.raise_for_status()

	logger.info(f"Deleted Google Calendar event {event_id} for {room_name}")
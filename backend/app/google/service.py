import httpx
from loguru import logger
from config import settings

ROOM_WEBAPP_URLS = {
	"piscine": settings.GOOGLE_WEBAPP_URL_PISCINE,
	"galaxy": settings.GOOGLE_WEBAPP_URL_GALAXY,
	"space-invader": settings.GOOGLE_WEBAPP_URL_SPACE_INVADER,
	"gallery": settings.GOOGLE_WEBAPP_URL_GALLERY,
}

async def _call_webapp(room_name: str, payload: dict) -> dict:
	url = ROOM_WEBAPP_URLS[room_name]
	payload["secret"] = settings.GOOGLE_WEBHOOK_SECRET

	async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
		response = await client.post(url, json=payload)
		if response.status_code >= 400:
			logger.error(f"Apps Script error {response.status_code}: {response.text}")
		response.raise_for_status()
		return response.json()

async def create_event(room_name: str, begin_at: int, end_at: int, summary: str = "Room booking") -> str:
	result = await _call_webapp(room_name, {
		"action": "create",
		"begin_at": begin_at,
		"end_at": end_at,
		"summary": summary,
	})
	logger.info(f"Created Google Calendar event {result['event_id']} for {room_name}")
	return result["event_id"]

async def update_event(room_name: str, event_id: str, begin_at: int, end_at: int) -> None:
	await _call_webapp(room_name, {
		"action": "update",
		"event_id": event_id,
		"begin_at": begin_at,
		"end_at": end_at,
	})
	logger.info(f"Updated Google Calendar event {event_id} for {room_name}")

async def delete_event(room_name: str, event_id: str) -> None:
	await _call_webapp(room_name, {
		"action": "delete",
		"event_id": event_id,
	})
	logger.info(f"Deleted Google Calendar event {event_id} for {room_name}")
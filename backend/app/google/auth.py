import time
import jwt
import httpx

_token_cache: dict[str, dict] = {}

async def get_access_token(room_name: str, credentials: dict) -> str:
	"""
	Returns a cached access token for the given room's service account,
	or signs a new JWT and exchanges it for one if the cache is empty or expired.

	:Parameters:
	------------
	room_name: str
		Room slug, used as the cache key.

	credentials: dict
		Decoded service account JSON for this room (client_email, private_key, token_uri).

	:Returns:
	---------
	access_token: str
		Bearer token usable against the Calendar API for ~the next hour.
	"""
	cached = _token_cache.get(room_name)
	if cached and cached["expires_at"] > time.time():
		return cached["access_token"]

	now = int(time.time())
	claims = {
		"iss": credentials["client_email"],
		"scope": "https://www.googleapis.com/auth/calendar",
		"aud": credentials["token_uri"],
		"iat": now,
		"exp": now + 3600,
	}
	assertion = jwt.encode(claims, credentials["private_key"], algorithm="RS256")

	async with httpx.AsyncClient() as client:
		response = await client.post(
			credentials["token_uri"],
			data={
				"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
				"assertion": assertion,
			},
		)
		response.raise_for_status()
		token_data = response.json()

	_token_cache[room_name] = {
		"access_token": token_data["access_token"],
		"expires_at": now + token_data["expires_in"] - 60,
	}
	return token_data["access_token"]
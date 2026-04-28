Docker container   → already using port 8000
uv run uvicorn     → tries to use port 8000 → conflict
for now:
    Option 2 — Keep Docker running, run uv on a different port:
    bash uv run uvicorn main:app --reload --port 8001

Every file that needs credentials just does:
    pythonfrom config import settings
    print(settings.POSTGRES_USER)  # reads from .env
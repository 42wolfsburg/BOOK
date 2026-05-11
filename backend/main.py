from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
	"""
	Lifespan function that takes care of setup and tear down of program. If something
	must be initialized once, you should insert it before the `yield` keyword and for
	whatever should be closed once at the end, put it after the keyword.
	"""
	logger.info("Initializing database...")
	init_db()
	logger.info("Database ready!")
	yield
	logger.info("Shutting down application...")
	close_db()

app = FastAPI(
	title="BOOK",
	description="BOOK's Online Occupancy Keeper",
	version="1.0.0",
	lifespan=lifespan	
)

app.include_router(router)

def setup_logger():
	"""
	Function responsible for setup of the stdout logging of the medic.
	Over here we also initialize the main log the `mediclogs`.

	:Returns:
	---------
	logger: Logger
		logger object from loguru that will be responsible for stdout
		and log file input.

	sink_id: int
		ID of the mediclogs log file.
	"""
	logger.remove() # closing double logging for stderr
	logger.level("INFO", color="<bold><green>")
	logger.level("WARNING", color="<yellow>")
	logger.level("ERROR", color="<red>")
	logger.level("CRITICAL", color="<bold><red>")
	sink_id = logger.add(
	    sys.stdout,
	    format="<level>{level} {time:YYYY-MM-DD HH:mm:ss}: {message}</level>",
	    colorize=True,
	    filter=lambda record: record["level"].name in ("INFO", "WARNING", "ERROR", "CRITICAL") or record["extra"].get("stdout_only")
	)
	logger.add(f"logs/medic.log", filter=lambda record: not record["extra"].get("stdout_only"))
	return logger, sink_id	

def main():
	# ------------------- Logging --------------------------
	main_sink_id: int
	logger, main_sink_id = setup_logger()
	logger.info("Logging system initialized")

	# ------------------- Server setup --------------------------
	from config import settings
	import uvicorn
	logger.info(f"starting server")
	uvicorn.run(
		"main:app",
		host=settings.BACKEND_HOST,
		port=settings.BACKEND_PORT,
		reload=True
	)
	return 0

	

if __name__ == "__main__":
	import sys
	sys.exit(main())
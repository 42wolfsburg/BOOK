CREATE TABLE IF NOT EXISTS bookings (
	id			UUID PRIMARY KEY default get_random_uuid(),
	intra		TEXT NOT NULL,
	room_name	TEXT NOT NULL,
	begin_at	TIMESTAMPTZ NOT NULL,
	end_at		TIMESTAMPTZ NOT NULL,
	is_staff	BOOLEAN NOT NULL DEFAULT FALSE
);
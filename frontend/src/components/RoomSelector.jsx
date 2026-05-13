import { motion } from "framer-motion";

export default function RoomSelector({
  rooms,
  selectedRoom,
  setSelectedRoom,
}) {
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {rooms.map((room) => {
        const active = room.id === selectedRoom;

        return (
          <motion.button
            key={room.id}
            whileHover={{ y: -2 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setSelectedRoom(room.id)}
            className={`
              rounded-2xl border p-4 text-left transition-all duration-300
              sm:p-5
              ${room.color}
              ${
                active
                  ? "ring-2 ring-violet-300 shadow-lg"
                  : "hover:shadow-md"
              }
            `}
          >
            <div className="flex items-start justify-between gap-3">

              {/* text */}
              <div className="min-w-0">
                <h3 className="truncate text-sm font-semibold sm:text-base">
                  {room.name}
                </h3>

                <p className="mt-1 text-xs opacity-70 sm:text-sm">
                  {room.seats} seats
                </p>
              </div>

              {/* active dot*/}
              {active && (
                <motion.div
                  layoutId="activeRoom"
                  className="mt-1 h-3 w-3 shrink-0 rounded-full bg-violet-500"
                />
              )}

            </div>
          </motion.button>
        );
      })}
    </div>
  );
}
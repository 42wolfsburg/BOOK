import { useContext, useState, useRef, useEffect } from "react";
import { AuthContext } from "./AuthGate";

export default function RoomDropdown({ rooms, selectedRoom, setSelectedRoom }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);
  const login = useContext(AuthContext);
  const canSee = login.isStaff;

  const visibleRooms = canSee
    ? rooms
    : rooms.filter((room) => room.slug !== "gallery" && room.slug !== "space-invader");

  useEffect(() => {
    function onDoc(e) {
      if (!ref.current) return;
      if (!ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("pointerdown", onDoc);
    return () => document.removeEventListener("pointerdown", onDoc);
  }, []);

  const current = visibleRooms.find((r) => r.id === selectedRoom) || visibleRooms[0];

  return (
    <div ref={ref} className="relative w-full max-w-md">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="w-full flex items-center justify-between gap-3 rounded-2xl border border-gray-100 bg-white px-4 py-3 text-left shadow-sm hover:shadow-md transition"
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <div className="min-w-0">
          <div className="truncate text-sm font-semibold text-slate-900">
            {current?.name}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div
            className="h-3 w-3 shrink-0 rounded-full ring-1 ring-gray-50"
            style={{ background: current?.accent }}
          />
          <svg className="h-4 w-4 text-slate-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden>
            <path fillRule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 011.08 1.04l-4.25 4.25a.75.75 0 01-1.08 0L5.25 8.27a.75.75 0 01-.02-1.06z" clipRule="evenodd" />
          </svg>
        </div>
      </button>

      {open && (
        <div className="absolute z-50 mt-2 w-full rounded-2xl border border-gray-100 bg-white shadow-lg ring-1 ring-black/5">
          {/* header */}
          <div className="flex items-center justify-between px-3 py-2 border-b border-gray-100">
            <div className="text-sm font-medium text-slate-700">Rooms</div>
            <button
              onClick={() => setOpen(false)}
              aria-label="Close rooms"
              className="p-1 rounded-md text-slate-400 hover:text-slate-600"
            >
              ✕
            </button>
          </div>

          {/* room list */}
          <ul role="listbox" tabIndex={-1} className="max-h-64 overflow-auto divide-y divide-gray-100 p-1">
            {visibleRooms.length === 0 && <li className="p-3 text-sm text-slate-500">No rooms available</li>}

            {visibleRooms.map((room) => {
              const active = room.id === selectedRoom;
              return (
                <li
                  key={room.id}
                  role="option"
                  aria-selected={active}
                  onClick={() => {
                    setSelectedRoom(room.id);
                    setOpen(false);
                  }}
                  tabIndex={0}
                  className={`flex items-center justify-between gap-3 px-3 py-2 rounded-md cursor-pointer transition ${
                    active ? "bg-violet-50 ring-1 ring-violet-100" : "hover:bg-gray-50"
                  }`}
                >
                  <div className="min-w-0">
                    <div className="truncate text-sm font-medium text-slate-900">{room.name}</div>
                  </div>

                  <div className="flex items-center gap-2">
                    <div className="h-3 w-3 rounded-full" style={{ background: room.accent }} />
                    {active && <span className="text-xs text-violet-600">Selected</span>}
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}
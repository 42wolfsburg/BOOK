import { useState, useRef, useEffect } from "react";

export default function RoomDropdown({ rooms, selectedRoom, setSelectedRoom }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    function onDoc(e) {
      if (!ref.current) return;
      if (!ref.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("pointerdown", onDoc);
    return () => document.removeEventListener("pointerdown", onDoc);
  }, []);

  const current = rooms.find((r) => r.id === selectedRoom) || rooms[0];

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
          <div className="text-xs text-slate-500">{current?.seats} seats</div>
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
          <div className="p-4 text-sm text-slate-600">TO DO </div>
        </div>
      )}
    </div>
  );
}
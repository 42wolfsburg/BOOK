
export default function BookingCard({ event }) {
  return (
    <div className="h-full overflow-hidden rounded-xl border border-violet-200 bg-violet-100 px-2 py-1 shadow-sm">

      <div className="truncate text-xs font-semibold text-violet-900">
        Reserved by
      </div>

      <div className="truncate text-[11px] text-violet-700">
        {new Date(
          event.start
        ).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        })}
        {" - "}
        {new Date(
          event.end
        ).toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        })}
      </div>
    </div>
  );
}
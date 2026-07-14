import React from "react";
import moment from "moment";
import RoomDropdown from "./RoomDropdown";

export default function CalendarHeader({
  currentDate,
  calendarView,
  setCalendarView,
  goToToday,
  goToPrevious,
  goToNext,
  dateInputRef,
  setCurrentDate,
  onOpenQuickBooking,
  rooms,
  selectedRoom,
  setSelectedRoom,
}) {
  return (
    <div className="mb-6 flex flex-col gap-5 xl:flex-row xl:items-center xl:justify-between">
      {/* left: Select Room label + dropdown */}
      <div className="flex items-center gap-3 min-w-0 w-full xl:w-auto">
        <div className="text-sm text-slate-500 flex-shrink-0 whitespace-nowrap">Select Room</div>
        <div className="min-w-0 flex-1 sm:w-[280px] sm:flex-none">
          <RoomDropdown
            rooms={rooms}
            selectedRoom={selectedRoom}
            setSelectedRoom={setSelectedRoom}
          />
        </div>
      </div>

      {/* right: New Booking button */}
      <div>
        <button
          onClick={() =>
            onOpenQuickBooking({
              start: new Date(),
              end: moment().add(1, "hour").toDate(),
            })
          }
          className="flex h-[44px] items-center justify-center rounded-xl bg-violet-600 px-5 text-sm font-medium leading-none text-white transition hover:bg-violet-700"
        >
          + New Booking
        </button>
      </div>
    </div>
  );
}
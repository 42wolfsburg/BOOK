import React from "react";
import moment from "moment";

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
}) {
  return (
    <div className="mb-6 flex flex-col gap-5 xl:flex-row xl:items-center xl:justify-between">

      {/* left side controls */}
      <div className="flex flex-col gap-4">

        <div className="flex flex-wrap items-center gap-6">

          {/* calendar navigation */}
          <div className="flex items-center">

            {/* reset to today */}
            <button
              onClick={goToToday}
              className="flex h-[44px] items-center justify-center rounded-xl border border-slate-200 bg-white px-5 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              Today
            </button>

            {/* prev/next buttons */}
            <div className="ml-2 flex items-center">
              <button
                onClick={goToPrevious}
                className="flex h-[44px] w-[44px] items-center justify-center rounded-xl border border-slate-200 bg-white text-lg font-medium text-slate-700 transition hover:bg-slate-50"
              >
                {"<"}
              </button>

              <button
                onClick={goToNext}
                className="flex h-[44px] w-[44px] items-center justify-center rounded-xl border border-slate-200 bg-white text-lg font-medium text-slate-700 transition hover:bg-slate-50"
              >
                {">"}
              </button>
            </div>
          </div>

          {/* current date */}
          <div className="relative inline-block">

            <div
              className="flex cursor-pointer select-none items-center gap-2"
              onClick={() => dateInputRef.current?.showPicker?.()}
            >
              <h2 className="text-2xl font-semibold text-slate-900">
                {calendarView === "week"
                  ? `${moment(currentDate).startOf("week").format("MMM DD")} – ${moment(currentDate).endOf("week").format("MMM DD, YYYY")}`
                  : moment(currentDate).format("MMMM DD, YYYY")}
              </h2>

              <span className="text-slate-500">▾</span>
            </div>

            {/* small hidden date picker */}
            <input
              ref={dateInputRef}
              type="date"
              value={moment(currentDate).format("YYYY-MM-DD")}
              onChange={(e) => {
                setCurrentDate(new Date(e.target.value));
              }}
              className="pointer-events-none absolute opacity-0"
            />

            <p className="mt-1 text-sm text-slate-500">Workspace scheduling overview</p>
          </div>
        </div>
      </div>

      {/* right side actions */}
      <div className="flex flex-wrap items-center gap-3">

        {/* switch calendar mode */}
        <select
          value={calendarView}
          onChange={(e) => setCalendarView(e.target.value)}
          className="flex h-[44px] rounded-xl border border-slate-200 bg-white px-4 text-sm font-medium text-slate-700 outline-none transition focus:border-violet-300"
        >
          <option value="week">Week View</option>
          <option value="day">Day View</option>
        </select>

        {/* quick booking button */}
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
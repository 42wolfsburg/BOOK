import React from "react";

export default function CalendarToolbar({ label, onNavigate, onView, view }) {
  return (
    <div className="flex items-center justify-center border-b border-slate-100 sm:justify-start">
      <div className="flex items-center gap-2 p-3">
        <button
          onClick={() => onNavigate("TODAY")}
          className="hidden sm:flex h-10 items-center justify-center rounded-xl border border-slate-200 bg-white px-4 text-sm font-medium text-slate-700 hover:bg-slate-50"
        >
          Today
        </button>

        <button
          onClick={() => onNavigate("PREV")}
          className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-lg font-medium text-slate-700 hover:bg-slate-50"
        >
          {"<"}
        </button>

        <button
          onClick={() => onNavigate("NEXT")}
          className="flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-lg font-medium text-slate-700 hover:bg-slate-50"
        >
          {">"}
        </button>
      </div>

      <div className="flex-1 text-center px-3">
        <div className="text-lg font-semibold text-slate-900">{label}</div>
      </div>

      <div className="hidden p-3 sm:block">
        <select
          value={view}
          onChange={(e) => onView(e.target.value)}
          className="h-[44px] rounded-xl border border-slate-200 bg-white px-4 text-sm font-medium text-slate-700 outline-none transition focus:border-violet-300"
        >
          <option value="week">Week View</option>
          <option value="day">Day View</option>
        </select>
      </div>
    </div>
  );
}
import { useState, useEffect } from "react";

import {
  Calendar,
  momentLocalizer,
} from "react-big-calendar";

import moment from "moment";
import BookingCard from '../components/BookingCards'
import DeleteBooking from '../components/DeleteBooking'
import CalendarToolbar from "../components/CalendarToolbar";

const localizer = momentLocalizer(moment);

export default function CalendarView({
  events,
  currentDate,
  setCurrentDate,
  calendarView,
  setCalendarView,
  onOpenBookingModal,
  onDeleteBooking,
}) {
  const [selectedSlot, setSelectedSlot] = useState(null);

  const [width, setWidth] = useState(typeof window !== "undefined" ? window.innerWidth : 1200);
  
  useEffect(() => {
    const onResize = () => setWidth(window.innerWidth);
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  const isMobile = width < 480;

  const formats = {
    dayFormat: (date, culture, loc) =>
      isMobile ? loc.format(date, "ddd", culture) : loc.format(date, "D ddd", culture),
    dayHeaderFormat: (date, culture, loc) =>
      isMobile ? loc.format(date, "ddd", culture) : loc.format(date, "D ddd", culture),
    weekdayFormat: (date, culture, loc) => loc.format(date, "ddd", culture),
    // eventTimeRangeFormat: () => "",
  };

  // time logic
  function isPast(date) { return date < new Date(); }

  function isTooLong(start, end) { return ((end - start) / (1000 * 60 * 60) > 3 ); }

  function isOverlapping(newEvent) {
    return events.some((event) => {
      return (
        newEvent.start <
          event.end &&
        newEvent.end >
          event.start
      );
    });
  }

  function isSlotDisabled(slot) {
    const fakeEvent = { start: slot.start, end: slot.end };

    if (isPast(slot.start)) return true;
    if (isTooLong(slot.start, slot.end)) return true;
    if (isOverlapping(fakeEvent)) return true;

    return false;
  }

  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white">
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        selectable
        date={currentDate}
        onNavigate={setCurrentDate}
        view={calendarView}
        onView={setCalendarView}
        views={["week", "day"]}
        style={{ height: "78vh" }}
        popup
        toolbar={true}
        components={{
          toolbar: CalendarToolbar,
          // event: BookingCard,
          event: (props) => <DeleteBooking {...props} onDelete={onDeleteBooking} />,

        }}
        formats={formats}

        // disable invalid slots
        onSelecting={(range) => {
          const now =
            new Date();

          // month view
          if (calendarView === "month") {
            const day =
              new Date(range.start);
              day.setHours(0, 0, 0, 0);
              const today = new Date();
              today.setHours(0, 0, 0, 0);
              return day >= today;
          }

          // past
          if (range.start < now) return false;

          // overlap
          return !isSlotDisabled(range);
        }}

        // slot click
        onSelectSlot={(slot) => {
          const now = new Date();

          // month view
          if (calendarView === "month") {
            const day = new Date(slot.start);

            day.setHours(0, 0, 0, 0);
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            if (day < today) return;

            setCalendarView("day");
            setCurrentDate(slot.start);
          }

          // past
          if (slot.start < now) return;

          // too long
          if (isTooLong(slot.start, slot.end)) return;

          // overlap
          if (isOverlapping({start: slot.start, end: slot.end})) return;

          // save slot
          setSelectedSlot(slot);
          onOpenBookingModal(slot);
        }}

        // past style
        dayPropGetter={(date) => {
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          const compareDate = new Date(date);
          compareDate.setHours(0, 0, 0, 0);
          
          if (compareDate < today) return { style: { opacity: 0.45 } };

          return {};
        }}

        // eventPropGetter={() => ({
        //   style: {
        //     backgroundColor: "transparent",
        //     border: "none",
        //     padding: 0,
        //   },
        // })}
      />
    </div>
  );
}
import { useState } from "react";

import {
  Calendar,
  momentLocalizer,
} from "react-big-calendar";

import moment from "moment";

import BookingCard from "./BookingCards";

const localizer = momentLocalizer(moment);

export default function CalendarView({
  events,
  currentDate,
  setCurrentDate,
  calendarView,
  setCalendarView,
  onOpenBookingModal,
}) {
  const [selectedSlot, setSelectedSlot] =
    useState(null);

  // time logic
  function isPast(date) {
    return date < new Date();
  }

  function isTooLong(start, end) {
    return (
      (end - start) /
        (1000 * 60 * 60) >
      3
    );
  }

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
    const fakeEvent = {
      start: slot.start,
      end: slot.end,
    };

    if (isPast(slot.start))
      return true;

    if (
      isTooLong(
        slot.start,
        slot.end
      )
    ) {
      return true;
    }

    if (
      isOverlapping(fakeEvent)
    ) {
      return true;
    }

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
        style={{ height: "78vh" }}
        popup
        toolbar={false}
        components={{
          event: BookingCard,
        }}

        // disable invalid slots
        onSelecting={(range) => {
          const now =
            new Date();

          // month view
          if (
            calendarView ===
            "month"
          ) {
            const day =
              new Date(
                range.start
              );

            day.setHours(
              0,
              0,
              0,
              0
            );

            const today =
              new Date();

            today.setHours(
              0,
              0,
              0,
              0
            );

            return day >= today;
          }

          // past
          if (
            range.start < now
          ) {
            return false;
          }

          // overlap
          return !isSlotDisabled(
            range
          );
        }}

        // slot click
        onSelectSlot={(slot) => {
          const now =
            new Date();

          // month view
          if (
            calendarView ===
            "month"
          ) {
            const day =
              new Date(
                slot.start
              );

            day.setHours(
              0,
              0,
              0,
              0
            );

            const today =
              new Date();

            today.setHours(
              0,
              0,
              0,
              0
            );

            if (day < today)
              return;

            setCalendarView(
              "day"
            );

            setCurrentDate(
              slot.start
            );

            return;
          }

          // past
          if (
            slot.start < now
          )
            return;

          // too long
          if (
            isTooLong(
              slot.start,
              slot.end
            )
          ) {
            return;
          }

          // overlap
          if (
            isOverlapping({
              start:
                slot.start,
              end: slot.end,
            })
          ) {
            return;
          }

          // save slot
          setSelectedSlot(slot);

          onOpenBookingModal(
            slot
          );
        }}

        // past style
        dayPropGetter={(
          date
        ) => {
          const today =
            new Date();

          today.setHours(
            0,
            0,
            0,
            0
          );

          const compareDate =
            new Date(date);

          compareDate.setHours(
            0,
            0,
            0,
            0
          );

          if (
            compareDate <
            today
          ) {
            return {
              style: {
                opacity: 0.45,
              },
            };
          }

          return {};
        }}
      />
    </div>
  );
}
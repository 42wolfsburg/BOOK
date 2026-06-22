import { useState, useRef } from "react";
import moment from "moment";

export default function useCalendar(initialDate = new Date(), initialView = "week") {
  const [currentDate, setCurrentDate] = useState(initialDate);
  const [calendarView, setCalendarView] = useState(initialView);
  const dateInputRef = useRef(null);

  const goToToday = () => {
    setCurrentDate(new Date());
  };

  const goToPrevious = () => {
    const newDate =
      calendarView === "week"
        ? moment(currentDate).subtract(1, "week").toDate()
        : moment(currentDate).subtract(1, "day").toDate();
    setCurrentDate(newDate);
  };

  const goToNext = () => {
    const newDate =
      calendarView === "week"
        ? moment(currentDate).add(1, "week").toDate()
        : moment(currentDate).add(1, "day").toDate();
    setCurrentDate(newDate);
  };

  return {
    currentDate,
    setCurrentDate,
    calendarView,
    setCalendarView,
    dateInputRef,
    goToToday,
    goToPrevious,
    goToNext,
  };
}
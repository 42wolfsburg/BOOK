import { useState, useEffect } from "react";

export default function useBookings(selectedRoom, eventsData) {
  const [events, setEvents] = useState(eventsData[selectedRoom] || []);
  const [showModal, setShowModal] = useState(false);
  const [bookingData, setBookingData] = useState(null);

  useEffect(() => {
    setEvents(eventsData[selectedRoom] || []);
  }, [selectedRoom, eventsData]);

  const openBookingModal = (slot) => {
    setBookingData({
      start: slot.start,
      end: slot.end,
    });
    setShowModal(true);
  };

  const saveBooking = () => {
    if (!bookingData) return;
    setEvents((prev) => [...prev, bookingData]);
    setShowModal(false);
  };

  return {
    events,
    setEvents,
    showModal,
    setShowModal,
    bookingData,
    setBookingData,
    openBookingModal,
    saveBooking,
  };
}
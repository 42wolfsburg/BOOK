import { useState } from "react";
import useCalendar from "./hooks/useCalendar";
import useBookings from "./hooks/useBookings";
import Header from "./components/Header";
import CalendarView from "./components/CalendarView";
import ResponsiveLayout from "./components/ResponsiveLayout";
import BookingModal from "./components/BookingModal";
import DeleteBookingModal from "./components/DeleteBookingModal";
import CalendarHeader from "./components/CalendarHeader";

import { rooms } from "./data/rooms";

export default function App() {
  const [selectedRoom, setSelectedRoom] = useState(3);

  const {
    currentDate,
    setCurrentDate,
    calendarView,
    setCalendarView,
    dateInputRef,
    goToToday,
    goToPrevious,
    goToNext,
  } = useCalendar();

  const currentRoom = rooms.find((room) => room.id === selectedRoom) || rooms[0];

  const {
    events,
    showModal,
    setShowModal,
    bookingData,
    setBookingData,
    openBookingModal,
    saveBooking,
    selectedEvent,
    showDeleteModal,
    openDeleteModal,
    closeDeleteModal,
    confirmDelete,
  } = useBookings(currentRoom);

  return (
    <div className="min-h-screen bg-[#f5f7fb] p-3 md:p-5 lg:p-8">
      <div className="mx-auto max-w-[1600px]">
        <Header />

        <div className="rounded-[32px] border border-white bg-white p-4 shadow-[0_15px_50px_rgba(15,23,42,0.06)] md:p-6">
          <ResponsiveLayout>
            <CalendarHeader
              currentDate={currentDate}
              calendarView={calendarView}
              setCalendarView={setCalendarView}
              goToToday={goToToday}
              goToPrevious={goToPrevious}
              goToNext={goToNext}
              dateInputRef={dateInputRef}
              setCurrentDate={setCurrentDate}
              onOpenQuickBooking={openBookingModal}
              rooms={rooms}
              selectedRoom={selectedRoom}
              setSelectedRoom={setSelectedRoom}
            />

            <CalendarView
              events={events}
              currentDate={currentDate}
              setCurrentDate={setCurrentDate}
              calendarView={calendarView}
              setCalendarView={setCalendarView}
              onOpenBookingModal={openBookingModal}
              onSelectEvent={openDeleteModal}
            />
          </ResponsiveLayout>
        </div>

        <BookingModal
          open={showModal}
          onClose={() => setShowModal(false)}
          bookingData={bookingData}
          setBookingData={setBookingData}
          onSave={saveBooking}
        />

        <DeleteBookingModal
          open={showDeleteModal}
          event={selectedEvent}
          onClose={closeDeleteModal}
          onDelete={confirmDelete}
        />
      </div>
    </div>
  );
}
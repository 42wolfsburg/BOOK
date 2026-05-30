import { useState, useRef, useEffect } from "react";
import moment from "moment";

import Header from "./components/Header";
import RoomSelector from "./components/RoomDropdown";
import CalendarView from "./components/CalendarView";
import ResponsiveLayout from "./components/ResponsiveLayout";
import BookingModal from "./components/BookingModal";
import CalendarHeader from "./components/CalendarHeader";

import { rooms, eventsData } from "./data/rooms";

export default function App() {
  // room id, TO DO when backend ready
  const [selectedRoom, setSelectedRoom] =
    useState(3);

  // current date in calendar
  const [currentDate, setCurrentDate] =
    useState(new Date());

  // change between week/day mode
  const [calendarView, setCalendarView] =
    useState("week");

  // events for selected room
  const [events, setEvents] = useState(
    eventsData[selectedRoom]
  );

  // booking popup
  const [showModal, setShowModal] =
    useState(false);

  // TODO: connect when backend ready
  const [bookingData, setBookingData] =
    useState(null);

  const currentRoom =
    rooms.find(
      (room) => room.id === selectedRoom
    ) || rooms[0];

  const dateInputRef = useRef(null);

  useEffect(() => {
    setEvents(eventsData[selectedRoom]);
  }, [selectedRoom]);

  // jump back to today
  const goToToday = () => {
    setCurrentDate(new Date());
  };

  // previous day/week navigation
  const goToPrevious = () => {
    const newDate =
      calendarView === "week"
        ? moment(currentDate)
          .subtract(1, "week")
          .toDate()
        : moment(currentDate)
          .subtract(1, "day")
          .toDate();

    setCurrentDate(newDate);
  };

  // next day/week navigation
  const goToNext = () => {
    const newDate =
      calendarView === "week"
        ? moment(currentDate)
          .add(1, "week")
          .toDate()
        : moment(currentDate)
          .add(1, "day")
          .toDate();

    setCurrentDate(newDate);
  };

  // open modal
  const handleOpenBookingModal = (
    slot
  ) => {
    setBookingData({
      start: slot.start,
      end: slot.end,
    });

    setShowModal(true);
  };

  const handleSaveBooking = () => {
    if (!bookingData) return;

    setEvents((prev) => [
      ...prev,
      bookingData,
    ]);

    setShowModal(false);
  };

  return (
    <div className="min-h-screen bg-[#f5f7fb] p-3 md:p-5 lg:p-8">
      <div className="mx-auto max-w-[1600px]">

        <Header />

        <div className="rounded-[32px] border border-white bg-white p-4 shadow-[0_15px_50px_rgba(15,23,42,0.06)] md:p-6">

          <ResponsiveLayout>

            {/* top controls section */}
            <CalendarHeader
              currentDate={currentDate}
              calendarView={calendarView}
              setCalendarView={setCalendarView}
              goToToday={goToToday}
              goToPrevious={goToPrevious}
              goToNext={goToNext}
              dateInputRef={dateInputRef}
              setCurrentDate={setCurrentDate}
              onOpenQuickBooking={handleOpenBookingModal}
            />

            {/* room tabs */}
            <RoomSelector
              rooms={rooms}
              selectedRoom={selectedRoom}
              setSelectedRoom={setSelectedRoom}
            />

            {/* main calendar */}
            <CalendarView
              events={events}
              currentDate={currentDate}
              setCurrentDate={
                setCurrentDate
              }
              calendarView={calendarView}
              setCalendarView={
                setCalendarView
              }
              onOpenBookingModal={
                handleOpenBookingModal
              }
            />

          </ResponsiveLayout>
        </div>

        {/* booking modal */}
        <BookingModal
          open={showModal}
          onClose={() =>
            setShowModal(false)
          }
          bookingData={bookingData}
          setBookingData={
            setBookingData
          }
          onSave={handleSaveBooking}
        />
      </div>
    </div>
  );
}
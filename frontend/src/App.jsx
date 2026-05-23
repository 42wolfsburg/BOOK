import { useState, useRef, useEffect } from "react";
import moment from "moment";

import Header from "./components/Header";
import RoomSelector from "./components/RoomDropdown";
import CalendarView from "./components/CalendarView";
import ResponsiveLayout from "./components/ResponsiveLayout";
import BookingModal from "./components/BookingModal";

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
                      onClick={() =>
                        dateInputRef.current?.showPicker?.()
                      }
                    >
                      <h2 className="text-2xl font-semibold text-slate-900">
                        {calendarView === "week"
                          ? `${moment(
                              currentDate
                            )
                              .startOf("week")
                              .format(
                                "MMM DD"
                              )} – ${moment(
                              currentDate
                            )
                              .endOf("week")
                              .format(
                                "MMM DD, YYYY"
                              )}`
                          : moment(
                              currentDate
                            ).format(
                              "MMMM DD, YYYY"
                            )}
                      </h2>

                      <span className="text-slate-500">
                        ▾
                      </span>
                    </div>

                    {/* small hidden date picker */}
                    <input
                      ref={dateInputRef}
                      type="date"
                      value={moment(
                        currentDate
                      ).format(
                        "YYYY-MM-DD"
                      )}
                      onChange={(e) => {
                        setCurrentDate(
                          new Date(
                            e.target.value
                          )
                        );
                      }}
                      className="pointer-events-none absolute opacity-0"
                    />

                    <p className="mt-1 text-sm text-slate-500">
                      Workspace scheduling
                      overview
                    </p>
                  </div>
                </div>
              </div>

              {/* right side actions */}
              <div className="flex flex-wrap items-center gap-3">

                {/* switch calendar mode */}
                <select
                  value={calendarView}
                  onChange={(e) =>
                    setCalendarView(
                      e.target.value
                    )
                  }
                  className="flex h-[44px] rounded-xl border border-slate-200 bg-white px-4 text-sm font-medium text-slate-700 outline-none transition focus:border-violet-300"
                >
                  <option value="week">
                    Week View
                  </option>

                  <option value="day">
                    Day View
                  </option>
                </select>

               {/* quick booking button */}
                <button
                  onClick={() => {
                    handleOpenBookingModal(
                      {
                        start:
                          new Date(),
                        end: moment()
                          .add(
                            1,
                            "hour"
                          )
                          .toDate(),
                      }
                    );
                  }}
                  className="flex h-[44px] items-center justify-center rounded-xl bg-violet-600 px-5 text-sm font-medium leading-none text-white transition hover:bg-violet-700"
                >
                  + New Booking
                </button>
              </div>
            </div>

            {/* room tabs */}
            <RoomSelector
              rooms={rooms}
              selectedRoom={selectedRoom}
              setSelectedRoom={
                setSelectedRoom
              }
            />

            {/* room info */}
            <div className="mb-4 mt-5 flex items-center gap-3">
              <div
                className="h-3 w-3 rounded-full"
                style={{
                  background:
                    currentRoom?.accent ||
                    "#000",
                }}
              />

              <div>
                <h3 className="text-lg font-semibold text-slate-900">
                  {currentRoom?.name}
                </h3>

                <p className="text-sm text-slate-500">
                  {
                    currentRoom?.seats
                  }{" "}
                  seats available
                </p>
              </div>
            </div>

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
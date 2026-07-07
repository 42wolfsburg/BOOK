import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../components/AuthGate'
import { getBookings, postBookings } from '../services/bookingService'

export default function useBookings(currentRoom) {
  const [events, setEvents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [bookingData, setBookingData] = useState(null);
  const login = useContext(AuthContext)

  useEffect(() => {
    async function loadBookings() {
      const { resource } = await getBookings(currentRoom.slug);
      setEvents(
        resource.map((b) => ({
          title: `Booked by ${b.intra}`,
          start: new Date(b.begin_at),
          end: new Date(b.end_at),
        }))
      );
    }
    loadBookings();
  }, [currentRoom]);

  const openBookingModal = (slot) => {
    setBookingData({ start: slot.start, end: slot.end });
    setShowModal(true);
  };

  const saveBooking = async () => {
    if (!bookingData) return;

    const payload = {
      room_name: currentRoom.slug,
      intra: login,
      begin_at: Math.floor(bookingData.start.getTime() / 1000),
      end_at: Math.floor(bookingData.end.getTime() / 1000),
    };

    const response = await postBookings(payload)

    setEvents((prev) => [
      ...prev, 
      { title: `Booked by ${login}`, start: bookingData.start, end: bookingData.end }
    ]);
    setShowModal(false);
  };

  return {
    events, setEvents, showModal, setShowModal,
    bookingData, setBookingData, openBookingModal, saveBooking,
  };
}
import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../components/AuthGate'
import { getBookings, postBookings, deleteBookingById } from '../services/bookingService'

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
          id: b.id,
          title: `${b.intra}`,
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
      intra: login.login,
      begin_at: Math.floor(bookingData.start.getTime() / 1000),
      end_at: Math.floor(bookingData.end.getTime() / 1000),
      is_staff: login.isStaff,
    };

    const { resource } = await postBookings(payload)

    setEvents((prev) => [
      ...prev, 
      {
        id: resource.id, 
        title: `${login}`, 
        start: bookingData.start, 
        end: bookingData.end 
      }
    ]);
    setShowModal(false);
  };

  const deleteBooking = async (event) => {
    await deleteBookingById({ 
      room_name: currentRoom.slug, 
      id: event.id, 
    });
    setEvents((prev) => prev.filter((e) => e.id !== event.id));
  }

  return {
    events, setEvents, showModal, setShowModal,
    bookingData, setBookingData, openBookingModal, saveBooking, deleteBooking,
  };
}
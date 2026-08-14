import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../components/AuthGate'
import { getBookings, postBookings, deleteBookingById } from '../services/bookingService'

export default function useBookings(currentRoom) {
  const [events, setEvents] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [bookingData, setBookingData] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const login = useContext(AuthContext)

  useEffect(() => {
    async function loadBookings() {
      try {
        const { resource } = await getBookings(currentRoom.slug);
        setEvents(
          resource.map((b) => ({
            id: b.id,
            title: `${b.intra}`,
            start: new Date(b.begin_at),
            end: new Date(b.end_at),
          }))
        )
      } catch (e) {
        throw (e)
      }
    }
    loadBookings();
  }, [currentRoom]);

  const openBookingModal = (slot) => {
    setBookingData({ start: slot.start, end: slot.end });
    setShowModal(true);
  };

  const saveBooking = async () => {
    if (!bookingData) return;
    if (login.login === "lottwotu") return;

    const payload = {
      room_name: currentRoom.slug,
      intra: login.login,
      begin_at: Math.floor(bookingData.start.getTime() / 1000),
      end_at: Math.floor(bookingData.end.getTime() / 1000),
      is_staff: login.isStaff,
    };

    setIsSaving(true);
    try {
      const { resource } = await postBookings(payload)

      setEvents((prev) => [
        ...prev,
        {
          id: resource.id,
          title: login.login,
          start: bookingData.start,
          end: bookingData.end
        }
      ]);
      setShowModal(false);
    } catch (e) {
      alert("Failed to save booking. Please try again.");
    } finally {
      setIsSaving(false);
    }
  };

  const deleteBooking = async (event) => {
    setDeletingId(event.id);
    try {
      await deleteBookingById({
        room_name: currentRoom.slug,
        id: event.id,
      });
      setEvents((prev) => prev.filter((e) => e.id !== event.id));
    } catch (e) {
      console.error("Failed to delete booking", e);
      alert("Failed to delete booking. Please try again.");
    } finally {
      setDeletingId(null);
    }
  };

  const openDeleteModal = (event) => {
    setSelectedEvent(event);
    setShowDeleteModal(true);
  };

  const closeDeleteModal = () => {
    setShowDeleteModal(false);
  };

  const confirmDelete = async () => {
    if (!selectedEvent) return;
    await deleteBooking(selectedEvent);
    closeDeleteModal();
  };

  return {
    events, setEvents, showModal, setShowModal,
    bookingData, setBookingData, openBookingModal, saveBooking, isSaving,
    selectedEvent, showDeleteModal, openDeleteModal, closeDeleteModal, confirmDelete,
    deleteBooking, deletingId
  };
}
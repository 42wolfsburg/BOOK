import { AnimatePresence, motion } from "framer-motion";
import moment from "moment";

export default function DeleteBookingModal({
  open,
  event,
  onClose,
  onDelete,
}) {
  if (!event) return null;

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 z-40 bg-black/30 backdrop-blur-sm"
          />

          {/* modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.96, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.96, y: 20 }}
            className="fixed left-1/2 top-1/2 z-50 w-[95%] max-w-md -translate-x-1/2 -translate-y-1/2 rounded-3xl bg-white p-6 shadow-2xl"
          >
            <h2 className="mb-6 text-2xl font-semibold text-slate-900">
              Booking Details
            </h2>

            <div className="space-y-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div>
                <span className="text-sm font-medium text-slate-500">Booked by</span>
                <p className="text-base font-semibold text-slate-900">{event.title}</p>
              </div>
              <div>
                <span className="text-sm font-medium text-slate-500">Time</span>
                <p className="text-base font-semibold text-slate-900">
                  {moment(event.start).format("MMM D, h:mm A")} – {moment(event.end).format("h:mm A")}
                </p>
              </div>
            </div>

            {/* actions */}
            <div className="mt-8 flex items-center justify-end gap-3">
              <button
                onClick={onClose}
                className="rounded-2xl border border-slate-200 px-5 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
              >
                Cancel
              </button>

              <button
                onClick={onDelete}
                className="rounded-2xl bg-red-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-red-700"
              >
                Delete Booking
              </button>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
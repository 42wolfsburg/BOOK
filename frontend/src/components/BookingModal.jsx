import {
  AnimatePresence,
  motion,
} from "framer-motion";

import moment from "moment";

export default function BookingModal({
  open,
  onClose,
  bookingData,
  setBookingData,
  onSave,
}) {
  if (!bookingData) return null;

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
            initial={{
              opacity: 0,
              scale: 0.96,
              y: 20,
            }}
            animate={{
              opacity: 1,
              scale: 1,
              y: 0,
            }}
            exit={{
              opacity: 0,
              scale: 0.96,
              y: 20,
            }}
            className="fixed left-1/2 top-1/2 z-50 w-[95%] max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-3xl bg-white p-6 shadow-2xl"
          >
            <h2 className="mb-6 text-2xl font-semibold text-slate-900">
              Create Booking
            </h2>

            <div className="space-y-5">

              {/* start date */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  Start Date & Time
                </label>

                <input
                  type="datetime-local"
                  value={moment(
                    bookingData.start
                  ).format("YYYY-MM-DDTHH:mm")}
                  onChange={(e) =>
                    setBookingData({
                      ...bookingData,
                      start: Math.floor(new Date(e.target.value).getTime() / 1000),
                    })
                  }
                  className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none transition focus:border-violet-300"
                />
              </div>

              {/* end date */}
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-700">
                  End Date & Time
                </label>

                <input
                  type="datetime-local"
                  value={moment(
                    bookingData.end
                  ).format("YYYY-MM-DDTHH:mm")}
                  onChange={(e) =>
                    setBookingData({
                      ...bookingData,
                      end: new Date(
                        e.target.value
                      ),
                    })
                  }
                  className="w-full rounded-2xl border border-slate-200 px-4 py-3 outline-none transition focus:border-violet-300"
                />
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
                onClick={onSave}
                className="rounded-2xl bg-violet-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-violet-700"
              >
                Save Booking
              </button>

            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

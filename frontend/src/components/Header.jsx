import { motion } from "framer-motion";
import logo from "../assets/logo.png";

export default function Header() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-5 rounded-3xl border border-white bg-white px-4 py-4 shadow-[0_10px_40px_rgba(15,23,42,0.05)] md:px-6"
    >
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">

        {/* left section */}
        <div className="flex items-center gap-3">

          <div className="flex h-11 w-11 items-center justify-center overflow-hidden rounded-2xl bg-violet-100">
            <img
              src={logo}
              alt="Logo"
              className="h-8 w-8 object-contain"
            />
          </div>

          <div>
            <h1 className="text-xl font-semibold text-slate-900">
              Workspace Booking
            </h1>
          </div>
        </div>

        {/* right section */}
        <div className="flex flex-wrap items-center gap-3">

          {/* divider */}
          <div className="h-6 w-px bg-slate-200" />

          {/* user */}
          <div className="flex h-[44px] items-center gap-3 rounded-xl border border-slate-200 bg-white px-3">
            <img
              src={logo}
              alt="User"
              className="h-9 w-9 rounded-full"
            />

            <div>
              <p className="text-sm font-medium text-slate-800">
                spenev
              </p>
            </div>
          </div>

          {/* Logout */}
          <button className="flex h-[44px] items-center justify-center rounded-xl border border-red-100 bg-red-50 px-5 text-sm font-medium text-red-600 transition hover:bg-red-100">
            Logout
          </button>

        </div>
      </div>
    </motion.div>
  );
}
import { motion } from "framer-motion";
import logo from "../assets/logo.png";
import { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from "./AuthGate"

export default function Header() {
  const login = useContext(AuthContext)
  const nav = useNavigate()

  const handleLogout = async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/logout`, {
        credentials: "include",
      });
      if (res.ok){
        nav("/login", { replace: true })
      }
    } catch (e) {
      console.error("Logout failure", e)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-5 rounded-3xl border border-white bg-white px-3 py-3 sm:px-4 sm:py-4 md:px-6 shadow-[0_10px_40px_rgba(15,23,42,0.05)]"
    >
      <div className="flex flex-nowrap items-center justify-between gap-2 sm:gap-3">

        {/* left section */}
        <div className="flex items-center gap-1 sm:gap-2 md:gap-3 min-w-0 flex-1">

          <div className="flex h-8 w-8 sm:h-10 sm:w-10 md:h-11 md:w-11 shrink-0 items-center justify-center overflow-hidden rounded-2xl bg-violet-100">
            <img
              src={logo}
              alt="Logo"
              className="h-5 w-5 sm:h-7 sm:w-7 md:h-8 md:w-8 object-contain"
            />
          </div>

          <h1 className="truncate text-sm sm:text-base md:text-xl font-semibold text-slate-900">
            Workspace Booking
          </h1>
        </div>

        {/* right section */}
        <div className="flex items-center gap-1 sm:gap-2 md:gap-3">

          {/* user */}
          <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-2 sm:px-3 h-9 sm:h-10 md:h-[44px]">
            <img
              src={logo}
              alt="User"
              className="h-6 w-6 sm:h-7 sm:w-7 md:h-9 md:w-9 rounded-full"
            />

            <p className="block text-xs sm:text-sm font-medium text-slate-800 max-w-[60px] sm:max-w-[80px] truncate">
              {login && <span>{login}</span>}
            </p>
          </div>

          {/* Logout */}
          <button 
            onClick={handleLogout}
            className="h-9 sm:h-10 md:h-[44px] px-2 sm:px-3 md:px-5 text-xs sm:text-sm font-medium text-red-600 bg-red-50 border border-red-100 rounded-xl hover:bg-red-100 whitespace-nowrap"
          >
            Logout
          </button>

        </div>
      </div>
    </motion.div>
  );
}
import { useContext } from 'react'
import { AuthContext } from "./AuthGate";

export default function DeleteBooking({ event, onDelete }) {
    const login = useContext(AuthContext)
    const canDelete = login.isStaff || event.title === login.login

    return (
        <div className="relative h-full">
            <span>{event.title}</span>
            <button
                onClick={(e) => {
                    e.stopPropagation();
                    onDelete(event);
                }}
                className={`absolute top-0 right-0 px-1 text-xs ${
                    canDelete
                        ? "opacity-70 hover:opacity-100"
                        : "opacity-30 cursor-not-allowed"
                }`}
            >   
                x
            </button>
        </div>
    );
}
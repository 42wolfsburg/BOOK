import { useContext } from 'react'
import { AuthContext } from "./AuthGate";

export default function DeleteBooking({ event, onDelete, isDeleting }) {
    const login = useContext(AuthContext)
    const canDelete = login.isStaff || event.title === login.login

    return (
        <div className="relative h-full">
            <span>{event.title}</span>
            <button
                onClick={(e) => {
                    e.stopPropagation();
                    if (isDeleting) return;
                    onDelete(event);
                }}
                disabled={isDeleting}
                className={`absolute top-0 right-0 px-1 text-xs ${
                    isDeleting
                        ? "cursor-not-allowed opacity-70"
                        : canDelete
                        ? "opacity-70 hover:opacity-100"
                        : "opacity-30 cursor-not-allowed"
                }`}
            >
                {isDeleting ? (
                    <span className="inline-block h-2.5 w-2.5 animate-spin rounded-full border-2 border-current border-t-transparent align-middle" />
                ) : (
                    "x"
                )}
            </button>
        </div>
    );
}
export default function DeleteBooking({ event, onDelete }) {
    return (
        <div className="relative h-full">
            <span>{event.title}</span>
            <button
                onClick={(e) => {
                    e.stopPropagation();
                    onDelete(event);
                }}
                className="absolute top-0 right-0 px-1 text-xs opacity-70 hover:opacity-100"
            >   
                x
            </button>

        </div>
    );
}
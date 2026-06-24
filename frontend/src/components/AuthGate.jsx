import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";

export default function AuthGate({children}) {

    const [loggedIn, setLoggedIn] = useState(null);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/me`, {
                    credentials: "include",
                });
                setLoggedIn(res.ok);
            } catch (e) {
                console.error("Auth check failed", e);
                setLoggedIn(false);
            }
        };

        checkAuth();
    }, []);

    if (loggedIn === null) return null;
    if (loggedIn === false) return <Navigate to="/login" replace />;
    return children;
}

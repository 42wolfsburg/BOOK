import { useState, useEffect, createContext, useContext } from "react";
import { Navigate } from "react-router-dom";

export const AuthContext = createContext(null)

export default function AuthGate({children}) {
    const [loggedIn, setLoggedIn] = useState(null)
    const [login, setLogin] = useState(null)
    const [isStaff, setIsStaff] = useState(null)

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/auth/me`, {
                    credentials: "include",
                });

                if (res.ok) {
                    const data = await res.json()
                    setLogin(data.login)
                    setLoggedIn(true)
                    setIsStaff(data.is_staff)
                } else {
                    setLoggedIn(false)
                }
            } catch (e) {
                console.error("Auth check failed", e);
                setLoggedIn(false)
            }
        };

        checkAuth()
    }, [])

    if (loggedIn === null) return null
    if (loggedIn === false) return <Navigate to="/login" replace />
    return (
        <AuthContext.Provider value={{login, isStaff}}>
            {children}
        </AuthContext.Provider>
    )
}

import logo from "../assets/logo.png";

export default function Landing() {
    const handleLogin = () => { window.location.href = import.meta.env.VITE_API_URL + "/auth/login" };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#d0d5dd] text-[#0f1724] font-sans">

            <div className="w-full max-w-[1100px] px-6 sm:px-10 py-10 flex flex-col justify-between min-h-screen text-center">

                <header className="flex justify-center mt-2">
                    <img
                        src={logo}
                        alt="42 logo"
                        className="w-[180px] sm:w-[300px] object-contain"
                    />
                </header>

                <main className="flex flex-col items-center gap-6">

                    <h1 className="uppercase font-light leading-[0.95] tracking-[6px] sm:tracking-[10px] md:tracking-[12px] text-[36px] sm:text-[54px] md:text-[72px]">
                        BOOKING <span className="text-[#72a8e6] font-semibold">SYSTEM</span>
                    </h1>

                    <div className="w-14 sm:w-[72px] h-[3px] sm:h-[4px] bg-[#72a8e6]" />

                    <p className="font-mono text-[#4b5563] text-sm tracking-[2px]">
                        Book meetings. Manage availability.
                    </p>

                    <button
                        onClick={handleLogin}
                        className="mt-6 inline-flex items-center gap-4 px-10 py-4 border-2 border-[#72a8e6] text-[#72a8e6] font-mono tracking-[3px] transition-all duration-200 hover:-translate-y-0.5 hover:bg-black/5 hover:shadow-md active:translate-y-0 active:bg-[#72a8e6] active:text-white"
                    >
                        LOGIN WITH 42 →
                    </button>

                </main>

                <footer className="text-xs text-[#4b5563] tracking-[4px] flex gap-3 justify-center">
                    <span>INTERNAL TOOL</span>
                    <span>•</span>
                    <span>42 WOLFSBURG</span>
                </footer>

            </div>
        </div>
    );
}

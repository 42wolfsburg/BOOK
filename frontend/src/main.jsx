import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import App from "./App";
import Landing from "./components/Landing";
import "./styles/index.css";
import AuthGate from "./components/AuthGate";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Landing />} />
	      <Route path="/*" element={<AuthGate><App /></AuthGate>} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

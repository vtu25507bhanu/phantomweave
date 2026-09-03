import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";

import Dashboard from "./pages/Dashboard";
import AdminLoginHoneypot from "./pages/AdminLoginHoneypot";
import AuditLog from "./pages/AuditLog";

function Home() {
  const [status, setStatus] = useState("Loading...");

  useEffect(() => {
    axios.get("https://phantomweave.onrender.com/")
      .then((response) => {
        setStatus(response.data.status);
      })
      .catch(() => {
        setStatus("Backend not reachable. Please check the backend server.");
      });
  }, []);

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1>PhantomWeave</h1>
      <p>
        Backend status: <strong>{status}</strong>
      </p>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/admin-login" element={<AdminLoginHoneypot />} />
        <Route path="/audit-log" element={<AuditLog />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;


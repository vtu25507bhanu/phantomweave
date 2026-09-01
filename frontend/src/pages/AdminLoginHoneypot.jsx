import { useState, useRef, useEffect } from "react";
import api from "../services/api";

function AdminLoginHoneypot() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const [loading, setLoading] = useState(false);

  // Behavior tracking కోసం refs (re-render అవ్వకుండా విలువలు నిల్వ చేయడానికి)
  const startTime = useRef(Date.now());
  const keystrokeTimestamps = useRef([]);
  const mouseMoved = useRef(false);
  const failedAttempts = useRef(0);
  const requestCount = useRef(0);

  // పేజీ లోడ్ అయినప్పుడు session start time సెట్ చేయడం
  useEffect(() => {
    startTime.current = Date.now();

    const handleMouseMove = () => {
      mouseMoved.current = true;
    };
    window.addEventListener("mousemove", handleMouseMove);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  // ప్రతి కీస్ట్రోక్ టైమ్ రికార్డ్ చేయడం (typing speed లెక్కించడానికి)
  const handleKeyDown = () => {
    keystrokeTimestamps.current.push(Date.now());
  };

  // కీస్ట్రోక్ టైమ్‌స్టాంప్‌ల మధ్య సగటు గ్యాప్ (ms) లెక్కించడం
  const calculateTypingSpeed = () => {
    const times = keystrokeTimestamps.current;
    if (times.length < 2) return 300; // డేటా చాలకపోతే default (human-ish) విలువ

    let totalGap = 0;
    for (let i = 1; i < times.length; i++) {
      totalGap += times[i] - times[i - 1];
    }
    return totalGap / (times.length - 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    requestCount.current += 1;
    failedAttempts.current += 1; // ఇది honeypot కాబట్టి, ఎప్పుడూ "fail" అవుతుంది

    const sessionDuration = (Date.now() - startTime.current) / 1000; // సెకన్లలో
    const typingSpeed = calculateTypingSpeed();

    const behaviorData = {
      page_visited: "/admin-login",
      request_count: requestCount.current,
      session_duration: sessionDuration,
      failed_login_attempts: failedAttempts.current,
      typing_speed: typingSpeed,
      mouse_movement: mouseMoved.current ? 1 : 0,
    };

    try {
      // ఈ డేటాని AI threat detection API కి పంపడం (visitor కి తెలియకుండా, background లో)
      await api.post("/detect/analyze", behaviorData);
    } catch (error) {
      console.log("Detection API error:", error);
      // Visitor కి ఈ error కనపడకూడదు — వాళ్ళకి మామూలు login page లానే కనపడాలి
    }

    // కొద్దిగా delay ఇచ్చి, నిజమైన login లా అనిపించేలా చేయడం
    setTimeout(() => {
      setErrorMsg("Invalid username or password. Please try again.");
      setPassword("");
      setLoading(false);
    }, 800);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#0f172a",
        fontFamily: "sans-serif",
      }}
    >
      <div
        style={{
          background: "#1e293b",
          padding: "40px",
          borderRadius: "10px",
          width: "340px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.4)",
        }}
      >
        <h2 style={{ color: "#fff", textAlign: "center", marginBottom: "6px" }}>
          Admin Portal
        </h2>
        <p style={{ color: "#94a3b8", textAlign: "center", fontSize: "13px", marginBottom: "24px" }}>
          Authorized personnel only
        </p>

        <form onSubmit={handleSubmit}>
          <label style={{ color: "#cbd5e1", fontSize: "13px" }}>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={handleKeyDown}
            required
            style={{
              width: "100%",
              padding: "10px",
              margin: "6px 0 16px",
              borderRadius: "6px",
              border: "1px solid #334155",
              background: "#0f172a",
              color: "#fff",
              boxSizing: "border-box",
            }}
          />

          <label style={{ color: "#cbd5e1", fontSize: "13px" }}>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={handleKeyDown}
            required
            style={{
              width: "100%",
              padding: "10px",
              margin: "6px 0 16px",
              borderRadius: "6px",
              border: "1px solid #334155",
              background: "#0f172a",
              color: "#fff",
              boxSizing: "border-box",
            }}
          />

          {errorMsg && (
            <p style={{ color: "#f87171", fontSize: "13px", marginBottom: "12px" }}>
              {errorMsg}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "10px",
              background: "#2563eb",
              color: "#fff",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
              fontWeight: "600",
            }}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AdminLoginHoneypot;
import { useState, useEffect } from "react";
import api from "../services/api";

import Navbar from "../components/Navbar";
import ThreatCard from "../components/ThreatCard";
import Charts from "../components/Charts";
import HistoryTable from "../components/HistoryTable";

function Dashboard() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    try {
      const response = await api.get("/detect/logs");
      setLogs(response.data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
    // ప్రతి 5 సెకన్లకు ఆటోమేటిక్‌గా రిఫ్రెష్ చేయడం — కొత్త honeypot విజిటర్స్ వస్తే వెంటనే కనపడేలా
    const interval = setInterval(fetchLogs, 5000);
    return () => clearInterval(interval);
  }, []);

  const totalVisitors = logs.length;
  const threatCount = logs.filter((l) => l.is_threat === 1).length;
  const safeCount = totalVisitors - threatCount;

  return (
    <div>
      <Navbar />

      <div style={{ padding: "20px" }}>
        <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "space-between" }}>
          <h2 style={{ margin: "10px" }}>Honeypot Monitoring Dashboard</h2>
          <button
            onClick={fetchLogs}
            style={{
              background: "#2563eb",
              color: "#fff",
              border: "none",
              padding: "8px 16px",
              borderRadius: "6px",
              cursor: "pointer",
              height: "38px",
              margin: "10px",
            }}
          >
            🔄 Refresh
          </button>
        </div>

        <div style={{ display: "flex", flexWrap: "wrap" }}>
          <ThreatCard title="Total Visitors" value={totalVisitors} />
          <ThreatCard title="Threats Detected" value={threatCount} />
          <ThreatCard title="Safe Visitors" value={safeCount} />
        </div>

        {loading ? (
          <p style={{ color: "#6b7280" }}>Loading logs...</p>
        ) : (
          <>
            <Charts logs={logs} />
            <HistoryTable logs={logs} />
          </>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
import { useState, useEffect } from "react";
import api from "../services/api";
import Navbar from "../components/Navbar";

function AuditLog() {
  const [blocks, setBlocks] = useState([]);
  const [verification, setVerification] = useState(null);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState(false);

  const fetchBlocks = async () => {
    try {
      const response = await api.get("/audit/logs");
      setBlocks(response.data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  const verifyChain = async () => {
    setVerifying(true);
    try {
      const response = await api.get("/audit/verify");
      setVerification(response.data);
    } catch (error) {
      console.log(error);
    } finally {
      setVerifying(false);
    }
  };

  useEffect(() => {
    fetchBlocks();
  }, []);

  return (
    <div>
      <Navbar />
      <div style={{ padding: "20px" }}>
        <div style={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap" }}>
          <h2 style={{ margin: "10px" }}>⛓️ Blockchain Audit Log</h2>
          <button
            onClick={verifyChain}
            disabled={verifying}
            style={{
              background: "#7c3aed",
              color: "#fff",
              border: "none",
              padding: "8px 16px",
              borderRadius: "6px",
              cursor: "pointer",
              height: "38px",
              margin: "10px",
            }}
          >
            {verifying ? "Verifying..." : "🔍 Verify Chain Integrity"}
          </button>
        </div>

        {verification && (
          <div
            style={{
              padding: "16px",
              borderRadius: "8px",
              margin: "10px",
              background: verification.is_valid ? "#dcfce7" : "#fee2e2",
              color: verification.is_valid ? "#166534" : "#991b1b",
              fontWeight: "600",
            }}
          >
            {verification.is_valid ? (
              <>✅ Chain Valid — అన్ని {verification.total_blocks} blocks tamper కాలేదు.</>
            ) : (
              <>
                ⚠️ Tampering Detected! Blocks: {verification.tampered_entries.join(", ")}
              </>
            )}
          </div>
        )}

        {loading ? (
          <p style={{ color: "#6b7280", margin: "10px" }}>Loading blocks...</p>
        ) : (
          <div style={{ margin: "10px" }}>
            {blocks.map((block) => (
              <div
                key={block.id}
                style={{
                  background: "#1f2937",
                  color: "#e5e7eb",
                  padding: "16px",
                  borderRadius: "8px",
                  marginBottom: "12px",
                  fontFamily: "monospace",
                  fontSize: "13px",
                  overflowWrap: "break-word",
                }}
              >
                <p style={{ margin: "4px 0", color: "#fff", fontWeight: "600" }}>
                  Block #{block.id}
                </p>
                <p style={{ margin: "4px 0" }}>
                  <span style={{ color: "#9ca3af" }}>Timestamp: </span>
                  {new Date(block.timestamp).toLocaleString()}
                </p>
                <p style={{ margin: "4px 0" }}>
                  <span style={{ color: "#9ca3af" }}>Previous Hash: </span>
                  {block.previous_hash.slice(0, 24)}...
                </p>
                <p style={{ margin: "4px 0" }}>
                  <span style={{ color: "#22c55e" }}>Current Hash: </span>
                  {block.current_hash.slice(0, 24)}...
                </p>
                <p style={{ margin: "4px 0" }}>
                  <span style={{ color: "#9ca3af" }}>Event Data: </span>
                  {block.event_data}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AuditLog;
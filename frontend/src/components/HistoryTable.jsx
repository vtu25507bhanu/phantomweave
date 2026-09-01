function HistoryTable({ logs }) {
  if (!logs || logs.length === 0) {
    return <p style={{ color: "#6b7280" }}>ఇంకా ఏ విజిటర్ లాగ్‌లు లేవు.</p>;
  }

  return (
    <div style={{ margin: "20px 0" }}>
      <h3 style={{ color: "#111827" }}>📜 Visitor Logs</h3>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#111827", color: "#fff" }}>
            <th style={{ padding: "8px", textAlign: "left" }}>IP</th>
            <th style={{ padding: "8px", textAlign: "left" }}>Page</th>
            <th style={{ padding: "8px" }}>Risk Score</th>
            <th style={{ padding: "8px" }}>Status</th>
            <th style={{ padding: "8px" }}>Time</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, i) => (
            <tr key={log.id} style={{ background: i % 2 === 0 ? "#f3f4f6" : "#e5e7eb" }}>
              <td style={{ padding: "8px" }}>{log.ip_address}</td>
              <td style={{ padding: "8px" }}>{log.page_visited}</td>
              <td style={{ padding: "8px", textAlign: "center" }}>{log.risk_score}</td>
              <td
                style={{
                  padding: "8px",
                  textAlign: "center",
                  color: log.is_threat ? "#dc2626" : "#16a34a",
                  fontWeight: "600",
                }}
              >
                {log.is_threat ? "⚠️ Threat" : "✅ Safe"}
              </td>
              <td style={{ padding: "8px", fontSize: "12px" }}>
                {new Date(log.timestamp).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default HistoryTable;
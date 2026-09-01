import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

function Charts({ logs }) {
  const safeCount = logs.filter((l) => l.is_threat === 0).length;
  const threatCount = logs.filter((l) => l.is_threat === 1).length;

  const data = [
    { name: "Safe Visitors", value: safeCount },
    { name: "Threats Detected", value: threatCount },
  ];

  return (
    <div style={{ background: "#1f2937", padding: "20px", borderRadius: "10px", margin: "20px 0" }}>
      <h3 style={{ color: "#fff" }}>📊 Visitor Classification</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="#9ca3af" />
          <YAxis allowDecimals={false} stroke="#9ca3af" />
          <Tooltip />
          <Bar dataKey="value">
            <Cell fill="#22c55e" />
            <Cell fill="#dc2626" />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default Charts;
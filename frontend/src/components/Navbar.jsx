import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav
      style={{
        padding: "15px 20px",
        background: "#111827",
        color: "#fff",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
      }}
    >
      <h2 style={{ margin: 0 }}>🛡️ PhantomWeave</h2>

      <div style={{ display: "flex", gap: "20px", alignItems: "center" }}>
        <Link to="/dashboard" style={linkStyle}>
          Dashboard
        </Link>
        <Link to="/audit-log" style={linkStyle}>
          Audit Log
        </Link>
        <Link to="/admin-login" style={linkStyle}>
          Honeypot
        </Link>
        <span style={{ fontSize: "14px", color: "#9ca3af" }}>
          Cyber Threat Simulation Dashboard
        </span>
      </div>
    </nav>
  );
}

const linkStyle = {
  color: "#e5e7eb",
  textDecoration: "none",
  fontSize: "14px",
  fontWeight: "500",
};

export default Navbar;
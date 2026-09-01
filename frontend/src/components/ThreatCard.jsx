function ThreatCard({ title, value }) {
    return (
        <div style={{
            background: "#1f2937",
            color: "#fff",
            padding: "20px",
            borderRadius: "10px",
            margin: "10px",
            minWidth: "180px",
            boxShadow: "0 2px 6px rgba(0,0,0,0.3)"
        }}>
            <p style={{ margin: 0, fontSize: "13px", color: "#9ca3af" }}>{title}</p>
            <h3 style={{ margin: "8px 0 0" }}>{value}</h3>
        </div>
    );
}

export default ThreatCard;

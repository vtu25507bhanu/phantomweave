import { useState } from "react";

function AttackForm({ onSubmit }) {
    const [ip, setIp] = useState("192.168.1.10");
    const [attackType, setAttackType] = useState("sql_injection");
    const [payload, setPayload] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ ip, attack_type: attackType, payload });
    };

    return (
        <form onSubmit={handleSubmit} style={{
            background: "#1f2937",
            padding: "20px",
            borderRadius: "10px",
            color: "#fff",
            maxWidth: "500px"
        }}>
            <h3>Simulate Attack</h3>

            <label>IP Address</label>
            <input
                value={ip}
                onChange={(e) => setIp(e.target.value)}
                style={{ width: "100%", padding: "8px", margin: "6px 0 14px", borderRadius: "6px", border: "none" }}
            />

            <label>Attack Type</label>
            <select
                value={attackType}
                onChange={(e) => setAttackType(e.target.value)}
                style={{ width: "100%", padding: "8px", margin: "6px 0 14px", borderRadius: "6px", border: "none" }}
            >
                <option value="sql_injection">SQL Injection</option>
                <option value="xss">XSS</option>
                <option value="ddos">DDoS</option>
                <option value="brute_force">Brute Force</option>
                <option value="phishing">Phishing</option>
                <option value="malware">Malware</option>
            </select>

            <label>Payload (optional)</label>
            <textarea
                value={payload}
                onChange={(e) => setPayload(e.target.value)}
                style={{ width: "100%", padding: "8px", margin: "6px 0 14px", borderRadius: "6px", border: "none" }}
            />

            <button type="submit" style={{
                background: "#dc2626",
                color: "#fff",
                border: "none",
                padding: "10px 20px",
                borderRadius: "6px",
                cursor: "pointer"
            }}>
                Analyze Attack
            </button>
        </form>
    );
}

export default AttackForm;

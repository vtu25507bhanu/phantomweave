function AIAnalysis({ analysis }) {
    return (
        <div style={{
            background: "#1f2937",
            color: "#fff",
            padding: "20px",
            borderRadius: "10px",
            margin: "20px 0"
        }}>
            <h3>🤖 AI Analysis</h3>
            <p style={{ lineHeight: "1.6" }}>{analysis}</p>
        </div>
    );
}

export default AIAnalysis;

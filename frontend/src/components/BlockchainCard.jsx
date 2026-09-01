function BlockchainCard({ blockchain }) {
    if (!blockchain) return null;

    return (
        <div style={{
            background: "#1f2937",
            color: "#fff",
            padding: "20px",
            borderRadius: "10px",
            margin: "20px 0",
            wordBreak: "break-all"
        }}>
            <h3>⛓️ Blockchain Record</h3>
            <p><strong>Hash:</strong> {blockchain.hash}</p>
            <p><strong>Timestamp:</strong> {blockchain.timestamp}</p>
        </div>
    );
}

export default BlockchainCard;

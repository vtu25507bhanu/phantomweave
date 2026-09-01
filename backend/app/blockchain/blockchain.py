import hashlib
import json
from datetime import datetime, timezone


def calculate_hash(event_data: str, previous_hash: str, timestamp: str) -> str:
    """
    event_data + previous_hash + timestamp కలిపి SHA-256 hash క్రియేట్ చేస్తుంది.
    ఈ మూడింటిలో ఏది మారినా, hash పూర్తిగా మారిపోతుంది.
    """
    block_string = f"{event_data}{previous_hash}{timestamp}"
    return hashlib.sha256(block_string.encode()).hexdigest()


def create_genesis_hash() -> str:
    """చైన్ లో మొదటి బ్లాక్ కోసం — దీనికి ముందు ఏమీ లేదు కాబట్టి '0' వాడతాం."""
    return "0" * 64


def verify_chain_integrity(audit_logs: list) -> dict:
    """
    మొత్తం audit log చైన్ ని వెరిఫై చేస్తుంది.
    ప్రతి entry యొక్క hash, దాని data నుండి తిరిగి calculate చేసి,
    database లో save అయిన hash తో సరిపోతుందో చెక్ చేస్తుంది.
    """
    tampered_entries = []

    for i, log in enumerate(audit_logs):
        recalculated_hash = calculate_hash(
            log.event_data,
            log.previous_hash,
            log.timestamp.isoformat()
        )

        if recalculated_hash != log.current_hash:
            tampered_entries.append(log.id)

        # Chain link చెక్ — ఈ entry యొక్క previous_hash, నిజంగా ముందు entry యొక్క current_hash తోనే సరిపోతుందో
        if i > 0:
            expected_previous = audit_logs[i - 1].current_hash
            if log.previous_hash != expected_previous:
                tampered_entries.append(log.id)

    return {
        "total_blocks": len(audit_logs),
        "is_valid": len(tampered_entries) == 0,
        "tampered_entries": list(set(tampered_entries))
    }
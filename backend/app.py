from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import time
import random
import sqlite3
from datetime import datetime

app = FastAPI(title="PhantomWeave API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "phantomweave.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            attack_type TEXT,
            payload TEXT,
            threat_score INTEGER,
            threat_level TEXT,
            block_hash TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


class AttackRequest(BaseModel):
    ip: str
    attack_type: str
    payload: str = ""


ATTACK_PROFILES = {
    "sql_injection": {"type": "Automated Bot", "intent": "Data Exfiltration", "base_score": 70},
    "xss": {"type": "Script Kiddie", "intent": "Website Defacement", "base_score": 50},
    "ddos": {"type": "Botnet", "intent": "Service Disruption", "base_score": 85},
    "brute_force": {"type": "Automated Bot", "intent": "Credential Theft", "base_score": 60},
    "phishing": {"type": "Social Engineer", "intent": "Credential Harvesting", "base_score": 65},
    "malware": {"type": "Advanced Persistent Threat", "intent": "System Compromise", "base_score": 90},
}


def get_threat_level(score):
    if score >= 80:
        return "Critical"
    elif score >= 60:
        return "High"
    elif score >= 40:
        return "Medium"
    return "Low"


def generate_ai_analysis(attack_type, ip, score, level):
    profile = ATTACK_PROFILES.get(attack_type, {"type": "Unknown", "intent": "Unclear"})
    action = (
        "immediate isolation and incident response"
        if level in ["Critical", "High"]
        else "continued monitoring and logging"
    )
    return (
        f"An attack of type '{attack_type}' was detected from IP {ip}. "
        f"Threat scoring places this incident at {score}/100 ({level} severity). "
        f"The behavior pattern matches a '{profile['type']}' with likely intent of "
        f"'{profile['intent']}'. Recommended action: {action}."
    )


def generate_block(ip, attack_type, score):
    timestamp = str(time.time())
    raw = f"{ip}-{attack_type}-{score}-{timestamp}"
    block_hash = hashlib.sha256(raw.encode()).hexdigest()
    return {"hash": block_hash, "timestamp": timestamp, "data": raw}


@app.get("/")
def root():
    return {"status": "PhantomWeave backend running"}


@app.post("/simulate")
def simulate_attack(attack: AttackRequest):
    profile = ATTACK_PROFILES.get(
        attack.attack_type, {"type": "Unknown", "intent": "Unclear", "base_score": 40}
    )
    score = min(100, max(0, profile["base_score"] + random.randint(-10, 10)))
    level = get_threat_level(score)
    ai_analysis = generate_ai_analysis(attack.attack_type, attack.ip, score, level)
    block = generate_block(attack.ip, attack.attack_type, score)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO history (ip, attack_type, payload, threat_score, threat_level, block_hash, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            attack.ip,
            attack.attack_type,
            attack.payload,
            score,
            level,
            block["hash"],
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()

    return {
        "ip": attack.ip,
        "threat_score": score,
        "threat_level": level,
        "profile": {"type": profile["type"], "intent": profile["intent"]},
        "ai_analysis": ai_analysis,
        "blockchain": block,
    }


@app.get("/history")
def get_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT ip, attack_type, threat_score, threat_level, created_at FROM history ORDER BY id DESC"
    )
    rows = c.fetchall()
    conn.close()
    return [
        {"ip": r[0], "attack_type": r[1], "threat_score": r[2], "threat_level": r[3], "created_at": r[4]}
        for r in rows
    ]

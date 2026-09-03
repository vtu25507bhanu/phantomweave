# PhantomWeave

A full-stack cybersecurity honeypot and SOC (Security Operations Center) platform with AI-powered threat detection, blockchain-style forensic logging, and a live monitoring dashboard.

## Live Demo

- Frontend Dashboard: https://phantomweave-frontend.onrender.com/#/dashboard
- Backend API: https://phantomweave.onrender.com

## Features

- Fake admin login honeypot to lure and log attacker activity
- IsolationForest-based anomaly detection to flag suspicious visitors
- SHA-256 hash-chained forensic ledger for tamper-evident logs
- JWT authentication for secure access
- Real-time dashboard showing visitor stats, risk scores, and threat classification
- Audit log with full visitor history

## Tech Stack

- Backend: FastAPI, SQLAlchemy, scikit-learn, JWT
- AI: IsolationForest
- Frontend: React, Vite, Chart.js
- Database: SQLite
- Deployment: Render

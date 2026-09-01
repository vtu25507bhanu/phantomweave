import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

np.random.seed(42)

# =====================
# BENIGN SESSIONS — 8750
# =====================
n_benign = 8750
benign = pd.DataFrame({
    "request_count":         np.random.poisson(5,   n_benign),
    "session_duration":      np.random.normal(120,  40,  n_benign).clip(10, 600),
    "failed_login_attempts": np.random.poisson(0.3, n_benign),
    "typing_speed":          np.random.normal(250,  80,  n_benign).clip(60, 650),
    "mouse_movement":        np.random.normal(0.88, 0.15, n_benign).clip(0, 1),
    "label": 0
})

# =====================
# ATTACK SESSIONS — 3750
# with realistic OVERLAP so scores are not trivially separated
# =====================

# Brute force (1000)
brute = pd.DataFrame({
    "request_count":         np.random.poisson(35,  1000),
    "session_duration":      np.random.normal(40,   25,  1000).clip(5, 200),
    "failed_login_attempts": np.random.poisson(8,   1000),
    "typing_speed":          np.random.normal(180,  80,  1000).clip(40, 500),
    "mouse_movement":        np.random.normal(0.35, 0.2, 1000).clip(0, 1),
    "label": 1
})

# SQL Injection (900)
sqli = pd.DataFrame({
    "request_count":         np.random.poisson(18,  900),
    "session_duration":      np.random.normal(60,   30,  900).clip(8, 300),
    "failed_login_attempts": np.random.poisson(4,   900),
    "typing_speed":          np.random.normal(210,  70,  900).clip(60, 500),
    "mouse_movement":        np.random.normal(0.4,  0.2, 900).clip(0, 1),
    "label": 1
})

# DDoS (800)
ddos = pd.DataFrame({
    "request_count":         np.random.poisson(120, 800),
    "session_duration":      np.random.normal(15,   10,  800).clip(2, 80),
    "failed_login_attempts": np.random.poisson(2,   800),
    "typing_speed":          np.random.normal(150,  60,  800).clip(40, 400),
    "mouse_movement":        np.random.normal(0.1,  0.1, 800).clip(0, 1),
    "label": 1
})

# Phishing (600)
phish = pd.DataFrame({
    "request_count":         np.random.poisson(8,   600),
    "session_duration":      np.random.normal(90,   35,  600).clip(10, 300),
    "failed_login_attempts": np.random.poisson(3,   600),
    "typing_speed":          np.random.normal(220,  70,  600).clip(60, 500),
    "mouse_movement":        np.random.normal(0.55, 0.2, 600).clip(0, 1),
    "label": 1
})

# Port Scan (450)
portscan = pd.DataFrame({
    "request_count":         np.random.poisson(60,  450),
    "session_duration":      np.random.normal(20,   12,  450).clip(2, 100),
    "failed_login_attempts": np.random.poisson(1,   450),
    "typing_speed":          np.random.normal(160,  60,  450).clip(40, 400),
    "mouse_movement":        np.random.normal(0.08, 0.1, 450).clip(0, 1),
    "label": 1
})

# =====================
# COMBINE + SHUFFLE
# =====================
attack = pd.concat([brute, sqli, ddos, phish, portscan], ignore_index=True)
df = pd.concat([benign, attack], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"Total records    : {len(df)}")
print(f"Benign sessions  : {len(df[df.label==0])} ({len(df[df.label==0])/len(df)*100:.1f}%)")
print(f"Attack sessions  : {len(df[df.label==1])} ({len(df[df.label==1])/len(df)*100:.1f}%)")

# =====================
# SAVE CSV
# =====================
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "training_data.csv")
df.to_csv(csv_path, index=False)
print(f"Dataset saved    : {csv_path}")

# =====================
# TRAIN — unsupervised, NO labels passed to fit()
# contamination = 3750/12500 = 0.30 (attack ratio)
# =====================
X_all = df.drop("label", axis=1)
y_all = df["label"]

# 70% train (unsupervised) — 30% holdout for scoring
train_size = int(0.70 * len(df))
X_train = X_all.iloc[:train_size]          # NO labels used here
X_test  = X_all.iloc[train_size:]
y_test  = y_all.iloc[train_size:]

model = IsolationForest(
    n_estimators=200,
    contamination=0.30,    # matches actual attack ratio in dataset
    max_samples="auto",
    random_state=42
)

print("\nTraining Isolation Forest (unsupervised — no labels seen)...")
model.fit(X_train)   # labels intentionally NOT passed

# =====================
# SCORE on labeled holdout
# IsolationForest returns: -1 = anomaly (attack), 1 = normal (benign)
# Convert to 0/1 to match our labels
# =====================
raw_pred = model.predict(X_test)
y_pred = (raw_pred == -1).astype(int)   # -1 → 1 (attack), 1 → 0 (benign)

print("\n--- Holdout Set Evaluation (labeled, post-training) ---")
print(f"Holdout size : {len(y_test)} records")
print(f"Accuracy     : {accuracy_score(y_test, y_pred)*100:.1f}%")
print()
print(classification_report(y_test, y_pred, target_names=["Benign", "Attack"]))

# =====================
# SAVE MODEL
# =====================
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "threat_model.pkl")
joblib.dump(model, model_path)
print(f"Model saved  : {model_path}")

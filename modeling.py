# ============================================================
#        ACCIDENT INTELLIGENCE SYSTEM - FINAL ML MODEL
# ============================================================

# Predictions:
# 1. Injury Severity
# 2. Vehicle Damage Extent
# 3. Crash Severity Index (CSI)  [Custom AI Feature]

# ============================================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("cleaned_accident_data.csv")

# ============================================================
# CLEAN TEXT COLUMNS
# ============================================================

for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].astype(str).str.upper().str.strip()

# ============================================================
# REMOVE UNNECESSARY COLUMNS
# ============================================================

drop_cols = [
    'REPORT NUMBER',
    'PERSON ID',
    'VEHICLE ID',
    'LOCATION',
    'VEHICLE MODEL'
]

for col in drop_cols:
    if col in df.columns:
        df.drop(col, axis=1, inplace=True)

# ============================================================
# CREATE CUSTOM FEATURE → CRASH SEVERITY INDEX (CSI)
# ============================================================

def create_csi(row):

    score = 0

    # ---------------- SPEED ----------------
    if row['Speed Limit'] >= 70:
        score += 3

    elif row['Speed Limit'] >= 50:
        score += 2

    elif row['Speed Limit'] >= 30:
        score += 1

    # ---------------- WEATHER ----------------
    if row['Weather'] in ['RAIN', 'RAINING', 'SNOW', 'SNOWING']:
        score += 2

    # ---------------- SURFACE ----------------
    if row['Surface Condition'] in ['WET', 'SNOW', 'ICE']:
        score += 2

    # ---------------- LIGHT ----------------
    if 'DARK' in row['Light']:
        score += 2

    # ---------------- DRIVER DISTRACTION ----------------
    if row['Driver Distracted By'] not in ['NONE', 'UNKNOWN', 'NOT DISTRACTED']:
        score += 2

    # ---------------- SUBSTANCE ABUSE ----------------
    if row['Driver Substance Abuse'] not in ['NONE DETECTED', 'UNKNOWN']:
        score += 3

    # ---------------- DRIVER AT FAULT ----------------
    if row['Driver At Fault'] == 1:
        score += 2

    # ---------------- COLLISION TYPE ----------------
    if row['Collision Type'] in [
        'HEAD ON',
        'ANGLE',
        'SIDE IMPACT'
    ]:
        score += 2

    # ---------------- VEHICLE TYPE ----------------
    if row['Is_Bus_Truck'] == 1:
        score += 2

    # ===================================================
    # FINAL LABEL
    # ===================================================

    if score >= 14:
        return 'CRITICAL'

    elif score >= 9:
        return 'HIGH'

    elif score >= 5:
        return 'MEDIUM'

    else:
        return 'LOW'

# Create new target column
df['Crash Severity Index'] = df.apply(create_csi, axis=1)

# ============================================================
# SELECT FEATURES
# ============================================================

features = [

    'Weather',
    'Surface Condition',
    'Light',
    'Traffic Control',

    'Driver Substance Abuse',
    'Driver Distracted By',

    'Collision Type',
    'Vehicle Movement',

    'Vehicle Body Type',
    'Vehicle Make',

    'Vehicle Year',
    'Speed Limit',

    'Driver At Fault',

    'Is_Bike',
    'Is_Car',
    'Is_Bus_Truck'
]

# ============================================================
# TARGETS
# ============================================================

target_injury = 'Injury Severity'
target_damage = 'Vehicle Damage Extent'
target_csi = 'Crash Severity Index'

# ============================================================
# REMOVE MISSING VALUES
# ============================================================

required_cols = features + [
    target_injury,
    target_damage,
    target_csi
]

df = df.dropna(subset=required_cols)

# ============================================================
# INPUT FEATURES
# ============================================================

X = df[features]

# Convert categorical → numeric
X = pd.get_dummies(X)

# ============================================================
# TARGET VARIABLES
# ============================================================

y_injury = df[target_injury]
y_damage = df[target_damage]
y_csi = df[target_csi]

# ============================================================
# TRAIN TEST SPLIT
# ============================================================

X_train, X_test, yInjury_train, yInjury_test = train_test_split(
    X,
    y_injury,
    test_size=0.2,
    random_state=42
)

_, _, yDamage_train, yDamage_test = train_test_split(
    X,
    y_damage,
    test_size=0.2,
    random_state=42
)

_, _, yCSI_train, yCSI_test = train_test_split(
    X,
    y_csi,
    test_size=0.2,
    random_state=42
)

# ============================================================
# CREATE MODELS
# ============================================================

injury_model = RandomForestClassifier(
    n_estimators=120,
    random_state=42
)

damage_model = RandomForestClassifier(
    n_estimators=120,
    random_state=42
)

csi_model = RandomForestClassifier(
    n_estimators=120,
    random_state=42
)

# ============================================================
# TRAIN MODELS
# ============================================================

injury_model.fit(X_train, yInjury_train)

damage_model.fit(X_train, yDamage_train)

csi_model.fit(X_train, yCSI_train)

# ============================================================
# PREDICTIONS
# ============================================================

injury_pred = injury_model.predict(X_test)

damage_pred = damage_model.predict(X_test)

csi_pred = csi_model.predict(X_test)

# ============================================================
# ACCURACY
# ============================================================

injury_acc = accuracy_score(yInjury_test, injury_pred)

damage_acc = accuracy_score(yDamage_test, damage_pred)

csi_acc = accuracy_score(yCSI_test, csi_pred)

# ============================================================
# FINAL PERFORMANCE REPORT
# ============================================================

print("\n====================================================")
print("       ACCIDENT INTELLIGENCE ML REPORT")
print("====================================================\n")

print("MODEL PERFORMANCE:\n")

print(f"Injury Severity Prediction  : {round(injury_acc * 100, 2)}%")

print(f"Vehicle Damage Prediction   : {round(damage_acc * 100, 2)}%")

print(f"Crash Severity Index (CSI)  : {round(csi_acc * 100, 2)}%")

print("\n====================================================")

# ============================================================
# SAMPLE ACCIDENT ANALYSIS
# ============================================================

sample = X_test.iloc[[5]]

pred_injury = injury_model.predict(sample)[0]

pred_damage = damage_model.predict(sample)[0]

pred_csi = csi_model.predict(sample)[0]

# ============================================================
# RISK FACTORS ANALYSIS
# ============================================================

sample_original = df.iloc[sample.index[0]]

reasons = []

if sample_original['Speed Limit'] >= 60:
    reasons.append("High Speed Driving")

if sample_original['Weather'] in ['RAIN', 'SNOW']:
    reasons.append("Bad Weather Conditions")

if sample_original['Surface Condition'] in ['WET', 'ICE']:
    reasons.append("Slippery Road Surface")

if 'DARK' in sample_original['Light']:
    reasons.append("Poor Lighting Conditions")

if sample_original['Driver At Fault'] == 1:
    reasons.append("Driver Responsible for Crash")

if sample_original['Driver Distracted By'] not in [
    'NONE',
    'UNKNOWN',
    'NOT DISTRACTED'
]:
    reasons.append("Distracted Driving")

if sample_original['Driver Substance Abuse'] not in [
    'NONE DETECTED',
    'UNKNOWN'
]:
    reasons.append("Substance Abuse Detected")

# ============================================================
# FINAL ACCIDENT REPORT
# ============================================================

print("\n")
print("====================================================")
print("          ACCIDENT ANALYSIS REPORT")
print("====================================================\n")

print(f"Predicted Injury Severity:")
print(f"→ {pred_injury}\n")

print(f"Predicted Vehicle Damage:")
print(f"→ {pred_damage}\n")

print(f"Crash Severity Index:")
print(f"→ {pred_csi}\n")

print("Main Risk Factors:")

if len(reasons) == 0:
    print("→ No Major Risk Factors Detected")

else:
    for r in reasons:
        print(f"✔ {r}")

print("\nOverall Crash Assessment:")

if pred_csi == 'CRITICAL':
    print("→ Extremely Dangerous Crash Conditions")

elif pred_csi == 'HIGH':
    print("→ High Crash Severity Detected")

elif pred_csi == 'MEDIUM':
    print("→ Moderate Accident Conditions")

else:
    print("→ Relatively Safer Driving Conditions")

print("\n====================================================")

# ============================================================
# CLASSIFICATION REPORTS
# ============================================================

print("\nINJURY MODEL REPORT\n")
print(classification_report(yInjury_test, injury_pred))

print("\nDAMAGE MODEL REPORT\n")
print(classification_report(yDamage_test, damage_pred))

print("\nCSI MODEL REPORT\n")
print(classification_report(yCSI_test, csi_pred))

print("\n====================================================")
print("      SYSTEM EXECUTION COMPLETED SUCCESSFULLY")
print("====================================================")
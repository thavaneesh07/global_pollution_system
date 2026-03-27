import pandas as pd

# -------------------------------
# LOAD DATA
# -------------------------------
df = pd.read_csv("data/water/water_data.csv")

print("✅ Loaded\n")

# -------------------------------
# STEP 1: STANDARDIZE COLUMNS
# -------------------------------
# Adjust based on your dataset
df.columns = df.columns.str.strip()

print("Columns:")
print(df.columns)
# -------------------------------
# STEP 2: HANDLE MIN/MAX PROPERLY
# -------------------------------

# Create averaged columns
df["pH"] = (df["pH Min"] + df["pH Max"]) / 2
df["DO"] = (df["Dissolved Oxygen (mg/L) Min"] + df["Dissolved Oxygen (mg/L) Max"]) / 2
df["Temperature"] = (df["Temperature (°C) Min"] + df["Temperature (°C) Max"]) / 2

# ❗ IMPORTANT: DROP ORIGINAL COLUMNS
df = df[["pH", "DO", "Temperature"]]

# Remove missing values
df = df.dropna()

print("\nCleaned Data:")
print(df.head())
# -------------------------------
# STEP 3: CREATE WATER QUALITY SCORE
# -------------------------------
def calculate_score(row):
    score = 0

    # pH (ideal: 6.5 - 8.5)
    if 6.5 <= row.get("pH", 7) <= 8.5:
        score += 25

    # DO (higher is better)
    if row.get("DO", 0) > 5:
        score += 25

    # Temperature (moderate)
    if 10 <= row.get("Temperature", 20) <= 30:
        score += 25

    # Turbidity (lower is better)
    if row.get("Turbidity", 0) < 5:
        score += 25

    return score

df["Score"] = df.apply(calculate_score, axis=1)

# -------------------------------
# STEP 4: CLASSIFY
# -------------------------------
def classify(score):
    if score >= 75:
        return "Good"
    elif score >= 50:
        return "Moderate"
    else:
        return "Unsafe"

df["Quality"] = df["Score"].apply(classify)

# -------------------------------
# OUTPUT
# -------------------------------
print("\nFinal Output:")
print(df.head())

print("\nQuality Distribution:")
print(df["Quality"].value_counts())

import matplotlib.pyplot as plt

# -------------------------------
# GRAPH 1: Quality Distribution
# -------------------------------
plt.figure()
df["Quality"].value_counts().plot(kind='bar')

plt.title("Water Quality Distribution")
plt.xlabel("Quality")
plt.ylabel("Count")

plt.show()


# -------------------------------
# GRAPH 2: DO vs pH
# -------------------------------
plt.figure()
plt.scatter(df["pH"], df["DO"])

plt.title("pH vs Dissolved Oxygen")
plt.xlabel("pH")
plt.ylabel("DO")

plt.show()


# -------------------------------
# GRAPH 3: Temperature Distribution
# -------------------------------
plt.figure()
df["Temperature"].plot(kind='hist', bins=30)

plt.title("Temperature Distribution")
plt.xlabel("Temperature")

plt.show()
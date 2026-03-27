import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("data/air_data.csv")

# Clean
df = df.dropna(subset=["Country"])

# Rename columns
df = df.rename(columns={
    "AQI Value": "AQI",
    "PM2.5 AQI Value": "PM25",
    "NO2 AQI Value": "NO2",
    "Ozone AQI Value": "Ozone",
    "CO AQI Value": "CO"
})

# -------------------------------
# Features and Target
# -------------------------------
features = ["PM25"]
X = df[features]

y = df["AQI Category"]

# -------------------------------
# Train/Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Model
# -------------------------------
model = RandomForestClassifier()
model.fit(X_train, y_train)

# -------------------------------
# Prediction
# -------------------------------
y_pred = model.predict(X_test)

# -------------------------------
# Accuracy
# -------------------------------
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)
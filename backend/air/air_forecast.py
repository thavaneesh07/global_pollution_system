import pandas as pd

# Load dataset
df = pd.read_csv("data/air_time.csv")

print("✅ Loaded\n")

# -------------------------------
# 1. Select ONE pollutant (NO2)
# -------------------------------
df = df[df["Name"] == "Nitrogen dioxide (NO2)"]

# -------------------------------
# 2. Select required columns
# -------------------------------
df = df[["Start_Date", "Data Value"]]

# Rename columns
df = df.rename(columns={
    "Start_Date": "Date",
    "Data Value": "Value"
})

# -------------------------------
# 3. Convert Date
# -------------------------------
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------
# 4. Sort by Date
# -------------------------------
df = df.sort_values("Date")

print("\nCleaned Data:")
print(df.head())

from sklearn.linear_model import LinearRegression
import numpy as np


# -------------------------------
# 4.5 Group by Date (IMPORTANT FIX)
# -------------------------------
df = df.groupby("Date")["Value"].mean().reset_index()

# -------------------------------
# 5. Prepare Data for ML
# -------------------------------
# Convert date to ordinal (number)
df["Date_ordinal"] = df["Date"].map(pd.Timestamp.toordinal)

X = df[["Date_ordinal"]]
y = df["Value"]

# -------------------------------
# 6. Train Model
# -------------------------------
model = LinearRegression()
model.fit(X, y)

# -------------------------------
# 7. Predict Future
# -------------------------------
future_dates = pd.date_range(start=df["Date"].max(), periods=10)

future_ordinal = pd.DataFrame({
    "Date_ordinal": future_dates.map(pd.Timestamp.toordinal)
})

predictions = model.predict(future_ordinal)

# -------------------------------
# 8. Show Predictions
# -------------------------------
print("\nFuture Predictions:")
for date, pred in zip(future_dates, predictions):
    print(date.date(), "→", round(pred, 2))


import matplotlib.pyplot as plt

# Plot actual data
plt.figure()
plt.plot(df["Date"], df["Value"], label="Actual Data")

# Plot predictions
plt.plot(future_dates, predictions, label="Predicted", linestyle='dashed')

plt.title("Air Pollution Forecast")
plt.xlabel("Date")
plt.ylabel("Pollution Level")
plt.legend()

plt.show()
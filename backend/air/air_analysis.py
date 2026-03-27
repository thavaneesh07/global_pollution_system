import pandas as pd

# Load dataset
file_path = "data/air_data.csv"
df = pd.read_csv(file_path)

print("✅ Loaded Successfully\n")

# -------------------------------
# 1. Handle Missing Values
# -------------------------------
print("Missing values before cleaning:")
print(df.isnull().sum())

# Drop rows with missing Country
df = df.dropna(subset=["Country"])

# -------------------------------
# 2. Rename Columns (VERY IMPORTANT)
# -------------------------------
df = df.rename(columns={
    "AQI Value": "AQI",
    "PM2.5 AQI Value": "PM25",
    "NO2 AQI Value": "NO2",
    "Ozone AQI Value": "Ozone",
    "CO AQI Value": "CO"
})

print("\nColumns after renaming:")
print(df.columns)

# -------------------------------
# 3. Basic Analysis
# -------------------------------
print("\nTop 10 Most Polluted Countries:")
print(df.groupby("Country")["AQI"].mean().sort_values(ascending=False).head(10))

print("\nCleaned Data Preview:")
print(df.head())

import matplotlib.pyplot as plt

# -------------------------------
# 4. Visualization
# -------------------------------

# Top 10 polluted countries (again for plotting)
top_countries = df.groupby("Country")["AQI"].mean().sort_values(ascending=False).head(10)

plt.figure()
top_countries.plot(kind='bar')

plt.title("Top 10 Most Polluted Countries (Average AQI)")
plt.xlabel("Country")
plt.ylabel("AQI")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

plt.figure()
df["AQI"].plot(kind='hist', bins=30)

plt.title("AQI Distribution")
plt.xlabel("AQI")
plt.ylabel("Frequency")

plt.show()

plt.figure()
df["AQI"].plot(kind='hist', bins=30)

plt.title("AQI Distribution")
plt.xlabel("AQI")
plt.ylabel("Frequency")

plt.show()

top_cities = df.groupby("City")["AQI"].mean().sort_values(ascending=False).head(10)

plt.figure()
top_cities.plot(kind='bar')

plt.title("Top 10 Most Polluted Cities")
plt.ylabel("AQI")

plt.xticks(rotation=45)
plt.show()
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import requests

app = Flask(__name__)
CORS(app)

uploaded_df = None
uploaded_type = None


# -----------------------
# DEFAULT LOADERS
# -----------------------
def load_air():
    df = pd.read_csv("data/air_data.csv")
    return df

def load_water():
    return pd.read_csv("data/water/water_data.csv")


# -----------------------
# HELPER FUNCTIONS
# -----------------------
def find_column(df, keywords):
    for col in df.columns:
        name = col.lower()
        if any(k in name for k in keywords):
            return col
    return None


# -----------------------
# AIR ANALYSIS
# -----------------------
@app.route('/air-analysis')
def air_analysis():
    global uploaded_df, uploaded_type

    df = uploaded_df if uploaded_type == "air" else load_air()

    aqi_col = find_column(df, ["aqi", "value"])
    country_col = find_column(df, ["country", "location"])

    if not aqi_col or not country_col:
        return jsonify({"labels": ["Invalid Air Data"], "values": [0]})

    df = df.rename(columns={aqi_col: "AQI", country_col: "Country"})

    result = df.groupby("Country")["AQI"].mean().sort_values(ascending=False).head(5)

    return jsonify({
        "labels": result.index.tolist(),
        "values": result.values.tolist()
    })


# -----------------------
# AIR FORECAST
# -----------------------
@app.route('/air-forecast')
def air_forecast():
    global uploaded_df, uploaded_type

    if uploaded_type == "air":
        df = uploaded_df.copy()
    else:
        df = pd.read_csv("data/air_time.csv")

    date_col = find_column(df, ["date"])
    value_col = find_column(df, ["value", "aqi"])

    if not date_col or not value_col:
        return jsonify({"labels": ["Invalid Data"], "values": [0]})

    df = df.rename(columns={date_col: "Date", value_col: "Value"})
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

    df = df.dropna(subset=["Date"])
    df = df.groupby("Date")["Value"].mean().reset_index()

    df["Date_ordinal"] = df["Date"].map(pd.Timestamp.toordinal)

    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(df[["Date_ordinal"]], df["Value"])

    future_dates = pd.date_range(start=df["Date"].max(), periods=10)
    future_ord = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)

    preds = model.predict(future_ord)

    return jsonify({
        "labels": [str(d.date()) for d in future_dates],
        "values": preds.tolist()
    })


# -----------------------
# WATER ANALYSIS
# -----------------------
@app.route('/water-analysis')
def water_analysis():
    global uploaded_df, uploaded_type

    df = uploaded_df if uploaded_type == "water" else load_water()

    ph_min = find_column(df, ["ph", "min"])
    ph_max = find_column(df, ["ph", "max"])
    do_min = find_column(df, ["oxygen", "min"])
    do_max = find_column(df, ["oxygen", "max"])

    if not (ph_min and ph_max and do_min and do_max):
        return jsonify({"labels": ["Invalid Water Data"], "values": [0]})

    df["pH"] = (df[ph_min] + df[ph_max]) / 2
    df["DO"] = (df[do_min] + df[do_max]) / 2

    avg = df[["pH", "DO"]].mean()

    return jsonify({
        "labels": ["pH", "DO"],
        "values": [float(avg["pH"]), float(avg["DO"])]
    })


# -----------------------
# WATER FORECAST
# -----------------------
@app.route('/water-forecast')
def water_forecast():
    global uploaded_df, uploaded_type

    df = uploaded_df if uploaded_type == "water" else load_water()

    do_min = find_column(df, ["oxygen", "min"])
    do_max = find_column(df, ["oxygen", "max"])
    year_col = find_column(df, ["year"])

    if not (do_min and do_max and year_col):
        return jsonify({"labels": ["Invalid Data"], "values": [0]})

    df["DO"] = (df[do_min] + df[do_max]) / 2

    df = df[[year_col, "DO"]].dropna()
    df = df.groupby(year_col).mean().reset_index()

    from sklearn.linear_model import LinearRegression
    model = LinearRegression()
    model.fit(df[[year_col]], df["DO"])

    future_years = [[int(df[year_col].max()) + i] for i in range(1, 6)]
    preds = model.predict(future_years)

    return jsonify({
        "labels": [str(y[0]) for y in future_years],
        "values": preds.tolist()
    })


# -----------------------
# UPLOAD
# -----------------------
@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_df, uploaded_type

    file = request.files['file']
    uploaded_df = pd.read_csv(file)

    cols = [c.lower() for c in uploaded_df.columns]

    if any("aqi" in c for c in cols):
        uploaded_type = "air"
    elif any("ph" in c for c in cols):
        uploaded_type = "water"
    else:
        uploaded_type = "unknown"

    return jsonify({"type": uploaded_type})


# -----------------------
# CHATBOT (OLLAMA)
# -----------------------
@app.route('/chat', methods=['POST'])
def chat():
    global uploaded_df

    if uploaded_df is None:
        return jsonify({"reply": "Upload a dataset first."})

    question = request.json.get("message")

    prompt = f"""
    You are a data analyst.

    Dataset:
    {uploaded_df.head().to_string()}

    Question: {question}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False}
    )

    return jsonify({"reply": response.json()["response"]})


# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
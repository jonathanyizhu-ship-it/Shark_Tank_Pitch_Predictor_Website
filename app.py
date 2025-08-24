from flask import Flask, render_template, jsonify, request
import sqlite3
import pandas as pd
import numpy as np

app = Flask(__name__)

INPUT_DATA = [
   {'id': 1, 'Title': 'Market Value', 'Description': 'The total value of the market your company is involved in'},
   {'id': 2, 'Title': 'Total Revenue', 'Description': 'Total Sales/Revenue of the company'},
   {'id': 3, 'Title': 'Profit Margin', 'Description': 'Unit Cost of Manufacturing/Selling Price of Product (in percentage, e.g. 50)'},
   {'id': 4, 'Title': 'Years of Operation', 'Description': 'How many years has the company been in operation (decimals allowed)'},
   {'id': 5, 'Title': 'Debt', 'Description': 'What is the company’s total debt?'},
   {'id': 6, 'Title': 'Company Valuation', 'Description': 'How much is your company worth?'}
]

@app.route("/")
def home():
    return render_template('home.html', input_data=INPUT_DATA)

@app.route("/predict", methods=["POST"])
def predict():
    conn = sqlite3.connect("sharktank.db")
    train_data = pd.read_sql_query("SELECT * FROM shark_pitch", conn)
    train_labels = pd.read_sql_query("SELECT * FROM shark_labels", conn)
    conn.close()

    def normalize(df):
        return (df - df.min()) / (df.max() - df.min())

    X_train = normalize(train_data.drop(columns=["Title"]))
    y_train = train_labels["Shark_deals"]

    def euclidean(a, b):
        return np.sqrt(np.sum((a - b) ** 2))

    def classify_knn(unknown, k=7):
        distances = [(euclidean(unknown, X_train.iloc[i]), y_train.iloc[i]) for i in range(len(X_train))]
        distances.sort(key=lambda x: x[0])
        neighbors = [label for _, label in distances[:k]]
        return round(sum(neighbors) / k, 0)

    user_input = [
        float(request.form["market_value"]),
        float(request.form["total_revenue"]),
        float(request.form["profit_margin"]),
        float(request.form["years_of_operation"]),
        float(request.form["debt"]),
        float(request.form["company_valuation"])
    ]

    prediction = classify_knn(user_input, k=7)
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


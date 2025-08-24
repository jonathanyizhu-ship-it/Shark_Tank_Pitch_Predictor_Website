import sqlite3
import pandas as pd
import numpy as np

# 1. Connect to the database
conn = sqlite3.connect("sharktank.db")

# 2. Read data + labels into DataFrames
train_data = pd.read_sql_query("SELECT * FROM shark_pitch", conn)
train_labels = pd.read_sql_query("SELECT * FROM shark_labels", conn)

# 3. Close the connection (good practice)
conn.close()

# 4. Normalize features
def normalize(df):
    return (df - df.min()) / (df.max() - df.min())

X_train = normalize(train_data.drop(columns=["Title"]))   # features only
y_train = train_labels["Shark_deals"]                     # labels

# 5. Euclidean distance function
def euclidean(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# 6. KNN classifier
def classify_knn(unknown, k=7):
    distances = []
    for i in range(len(X_train)):
        dist = euclidean(unknown, X_train.iloc[i])
        distances.append((dist, y_train.iloc[i]))
    distances.sort(key=lambda x: x[0])
    neighbors = [label for _, label in distances[:k]]
    return round(sum(neighbors) / k, 0)



import sqlite3
import pandas as pd

# Connect (or create) DB
conn = sqlite3.connect('sharktank.db')
cursor = conn.cursor()

# Create table for training data
cursor.execute('''
CREATE TABLE IF NOT EXISTS shark_pitch (
    Title TEXT PRIMARY KEY,
    Market_Value REAL,
    Total_Revenue REAL,
    Profit_Margin REAL,
    Years_Of_Operation REAL,
    Debt REAL,
    Company_Valuation REAL
)
''')

# Create table for training labels
cursor.execute('''
CREATE TABLE IF NOT EXISTS shark_labels (
    Title TEXT PRIMARY KEY,
    Shark_deals INTEGER
)
''')

# Validation tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS shark_validation (
    Title TEXT PRIMARY KEY,
    Market_Value REAL,
    Total_Revenue REAL,
    Profit_Margin REAL,
    Years_Of_Operation REAL,
    Debt REAL,
    Company_Valuation REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS validation_labels (
    Title TEXT PRIMARY KEY,
    Shark_deals INTEGER
)
''')

conn.commit()

train_data = pd.read_csv("Shark_Tank_Train.csv")
train_labels = pd.read_csv("Sharktank_labels.csv")
validation_data = pd.read_csv("SharkTankValidation.csv")
validation_labels = pd.read_csv("Validation_Labels.csv")

# Insert training data
for _, row in train_data.iterrows():
    cursor.execute('''
        INSERT OR REPLACE INTO shark_pitch (Title, Market_Value, Total_Revenue, Profit_Margin, Years_Of_Operation, Debt, Company_Valuation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (row['Title'], row['Market_Value'], row['Total_Revenue'], row['Profit_Margin'], row['Years_Of_Operation'], row['Debt'], row['Company_Valuation']))

# Insert training labels
for _, row in train_labels.iterrows():
    cursor.execute('''
        INSERT OR REPLACE INTO shark_labels (Title, Shark_deals)
        VALUES (?, ?)
    ''', (row['Title'], row['Shark_deals']))

# Insert validation data
for _, row in validation_data.iterrows():
    cursor.execute('''
        INSERT OR REPLACE INTO shark_validation (Title, Market_Value, Total_Revenue, Profit_Margin, Years_Of_Operation, Debt, Company_Valuation)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (row['Title'], row['Market_Value'], row['Total_Revenue'], row['Profit_Margin'], row['Years_Of_Operation'], row['Debt'], row['Company_Valuation']))

# Insert validation labels
for _, row in validation_labels.iterrows():
    cursor.execute('''
        INSERT OR REPLACE INTO validation_labels (Title, Shark_deals)
        VALUES (?, ?)
    ''', (row['Title'], row['Shark_deals']))

# Commit and close
conn.commit()
conn.close()

print("CSV data uploaded to the database successfully!")

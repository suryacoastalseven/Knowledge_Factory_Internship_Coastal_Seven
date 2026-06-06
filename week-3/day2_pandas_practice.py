import pandas as pd
import numpy as np

print("=" * 50)
print("DAY 2 - PANDAS PRACTICE")
print("=" * 50)

# Sample Dataset

data = {
    "Name": ["Ayyappa", "Ram", "Sita", "Krishna", "Ravi"],
    "Department": ["IT", "IT", "HR", "HR", "Finance"],
    "Salary": [50000, 60000, np.nan, 45000, 70000],
    "JoiningDate": [
        "2023-01-10",
        "2022-05-20",
        "2021-07-15",
        "2024-02-01",
        "2020-12-25"
    ]
}

df = pd.DataFrame(data)

# 1. Display DataFrame
print("\n1. DATAFRAME")
print(df)

# 2. loc
print("\n2. LOC")
print(df.loc[0])

# 3. iloc
print("\n3. ILOC")
print(df.iloc[0])

# 4. Filtering
print("\n4. FILTERING")

high_salary = df[df["Salary"] > 50000]

print(high_salary)

# 5. Missing Values
print("\n5. MISSING VALUES")

print(df.isnull().sum())

df["Salary"] = df["Salary"].fillna(df["Salary"].mean())

print("\nAfter Fillna:")
print(df)

# 6. GroupBy
print("\n6. GROUPBY")

grouped = df.groupby("Department")["Salary"].mean()

print(grouped)

# 7. Datetime Parsing
print("\n7. DATETIME")

df["JoiningDate"] = pd.to_datetime(df["JoiningDate"])

df["Year"] = df["JoiningDate"].dt.year

print(df[["Name", "Year"]])

# 8. Pivot Table
print("\n8. PIVOT TABLE")

pivot = pd.pivot_table(
    df,
    values="Salary",
    index="Department",
    aggfunc="mean"
)

print(pivot)

# 9. EDA
print("\n9. EDA")

print("\nDataset Info:")
print(df.info())

print("\nStatistics:")
print(df.describe())

print("\nFirst 5 Rows:")
print(df.head())

print("\nDay 2 Completed Successfully!")
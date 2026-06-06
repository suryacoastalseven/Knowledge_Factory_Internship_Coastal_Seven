import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# DAY 3 - DATA VISUALIZATION PROJECT
# Matplotlib + Seaborn + EDA
# ==========================================

print("=" * 60)
print("DAY 3 - DATA VISUALIZATION WITH MATPLOTLIB & SEABORN")
print("=" * 60)

# ------------------------------------------
# Create Sample Dataset
# ------------------------------------------

np.random.seed(42)

data = {
    "Student": [f"Student_{i}" for i in range(1, 51)],
    "Hours_Studied": np.random.randint(1, 10, 50),
    "Marks": np.random.randint(40, 100, 50),
    "Attendance": np.random.randint(60, 100, 50),
    "Department": np.random.choice(
        ["CSE", "ECE", "MECH"],
        50
    )
}

df = pd.DataFrame(data)

print("\nDataset Preview:")
print(df.head())

# ------------------------------------------
# Basic EDA
# ------------------------------------------

print("\nDataset Information:")
print(df.info())

print("\nStatistical Summary:")
print(df.describe())

print("\nMissing Values:")
print(df.isnull().sum())

# ==========================================
# 1. LINE CHART
# ==========================================

plt.figure(figsize=(8, 5))

plt.plot(
    df.index,
    df["Marks"],
    marker="o"
)

plt.title("Line Chart - Marks Trend")
plt.xlabel("Student Index")
plt.ylabel("Marks")

plt.grid(True)

plt.show()

# ==========================================
# 2. BAR CHART
# ==========================================

dept_avg = df.groupby("Department")["Marks"].mean()

plt.figure(figsize=(8, 5))

plt.bar(
    dept_avg.index,
    dept_avg.values
)

plt.title("Average Marks by Department")
plt.xlabel("Department")
plt.ylabel("Average Marks")

plt.show()

# ==========================================
# 3. SCATTER PLOT
# ==========================================

plt.figure(figsize=(8, 5))

plt.scatter(
    df["Hours_Studied"],
    df["Marks"]
)

plt.title("Hours Studied vs Marks")
plt.xlabel("Hours Studied")
plt.ylabel("Marks")

plt.show()

# ==========================================
# 4. HISTOGRAM
# ==========================================

plt.figure(figsize=(8, 5))

plt.hist(
    df["Marks"],
    bins=10
)

plt.title("Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Frequency")

plt.show()

# ==========================================
# 5. BOXPLOT
# ==========================================

plt.figure(figsize=(8, 5))

sns.boxplot(
    y=df["Marks"]
)

plt.title("Box Plot of Marks")

plt.show()

# ==========================================
# 6. HEATMAP
# ==========================================

numeric_df = df.select_dtypes(include=np.number)

plt.figure(figsize=(8, 6))

sns.heatmap(
    numeric_df.corr(),
    annot=True
)

plt.title("Correlation Heatmap")

plt.show()

# ==========================================
# 7. PAIRPLOT
# ==========================================

sns.pairplot(
    df[
        [
            "Hours_Studied",
            "Marks",
            "Attendance"
        ]
    ]
)

plt.show()

# ==========================================
# 8. SUBPLOTS
# ==========================================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8)
)

# Line
axes[0, 0].plot(df["Marks"])
axes[0, 0].set_title("Line Plot")

# Bar
axes[0, 1].bar(
    dept_avg.index,
    dept_avg.values
)
axes[0, 1].set_title("Bar Plot")

# Scatter
axes[1, 0].scatter(
    df["Hours_Studied"],
    df["Marks"]
)
axes[1, 0].set_title("Scatter Plot")

# Histogram
axes[1, 1].hist(
    df["Marks"],
    bins=10
)
axes[1, 1].set_title("Histogram")

plt.tight_layout()

plt.show()

# ==========================================
# 9. SEABORN THEMES
# ==========================================

sns.set_theme()

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="Department",
    y="Marks"
)

plt.title("Seaborn Styled Chart")

plt.show()

# ==========================================
# 10. CHART ANNOTATION
# ==========================================

plt.figure(figsize=(8, 5))

plt.plot(
    df["Marks"],
    marker="o"
)

highest_index = df["Marks"].idxmax()
highest_mark = df["Marks"].max()

plt.annotate(
    f"Highest = {highest_mark}",
    xy=(highest_index, highest_mark),
    xytext=(highest_index + 2, highest_mark),
    arrowprops=dict()
)

plt.title("Annotation Example")

plt.show()

# ==========================================
# EDA STORY
# ==========================================

print("\n" + "=" * 60)
print("EDA INSIGHTS")
print("=" * 60)

print(
    "\nAverage Marks by Department:"
)

print(
    df.groupby("Department")["Marks"].mean()
)

print(
    "\nHighest Marks:"
)

print(
    df["Marks"].max()
)

print(
    "\nLowest Marks:"
)

print(
    df["Marks"].min()
)

print(
    "\nAverage Attendance:"
)

print(
    round(
        df["Attendance"].mean(),
        2
    )
)

print(
    "\nCorrelation Matrix:"
)

print(
    numeric_df.corr()
)

print("\nVisualization Project Completed Successfully!")
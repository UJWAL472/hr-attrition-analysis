# =====================================================
# HR Attrition Analysis - Python Script
# Dataset: IBM HR Analytics Employee Attrition (Kaggle)
# Place "HR_Attrition.csv" in the same folder as this script
# =====================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

sns.set_style("whitegrid")

# -----------------------------------------------------
# 1. Load and inspect the data
# -----------------------------------------------------
df = pd.read_csv("HR_Attrition.csv")

print("Shape of dataset:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values per column:")
print(df.isnull().sum().sum(), "total missing values")

print("\nAttrition breakdown:")
print(df["Attrition"].value_counts(normalize=True) * 100)


# -----------------------------------------------------
# 2. Feature engineering
# -----------------------------------------------------
# Tenure groups
def tenure_group(years):
    if years <= 2:
        return "0-2"
    elif years <= 5:
        return "3-5"
    elif years <= 10:
        return "6-10"
    else:
        return "10+"

df["TenureGroup"] = df["YearsAtCompany"].apply(tenure_group)

# Salary bands (quartiles)
df["SalaryBand"] = pd.qcut(df["MonthlyIncome"], 4, labels=["Low", "Medium", "High", "Very High"])

# Binary attrition flag for correlation/modeling
df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0})


# -----------------------------------------------------
# 3. Key summary stats (mirrors the SQL queries)
# -----------------------------------------------------
print("\n--- Attrition rate by Department ---")
print(df.groupby("Department")["AttritionFlag"].mean().round(3) * 100)

print("\n--- Attrition rate by OverTime ---")
print(df.groupby("OverTime")["AttritionFlag"].mean().round(3) * 100)

print("\n--- Attrition rate by Tenure Group ---")
print(df.groupby("TenureGroup")["AttritionFlag"].mean().round(3) * 100)

print("\n--- Attrition rate by Job Satisfaction ---")
print(df.groupby("JobSatisfaction")["AttritionFlag"].mean().round(3) * 100)


# -----------------------------------------------------
# 4. Correlation with numeric features
# -----------------------------------------------------
numeric_cols = df.select_dtypes(include=np.number).columns
corr = df[numeric_cols].corr()["AttritionFlag"].sort_values(ascending=False)
print("\n--- Correlation with Attrition (numeric features) ---")
print(corr)


# -----------------------------------------------------
# 5. Charts
# -----------------------------------------------------

# Chart 1: Attrition rate by department
plt.figure(figsize=(7, 4))
dept_attrition = df.groupby("Department")["AttritionFlag"].mean() * 100
dept_attrition.sort_values(ascending=False).plot(kind="bar", color="#4C72B0")
plt.title("Attrition Rate by Department")
plt.ylabel("Attrition Rate (%)")
plt.xlabel("")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("chart_attrition_by_department.png", dpi=150)
plt.close()

# Chart 2: Attrition by overtime
plt.figure(figsize=(5, 4))
overtime_attrition = df.groupby("OverTime")["AttritionFlag"].mean() * 100
overtime_attrition.plot(kind="bar", color="#DD8452")
plt.title("Attrition Rate: OverTime vs No OverTime")
plt.ylabel("Attrition Rate (%)")
plt.xlabel("")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart_attrition_by_overtime.png", dpi=150)
plt.close()

# Chart 3: Tenure distribution for leavers vs stayers
plt.figure(figsize=(7, 4))
sns.histplot(data=df, x="YearsAtCompany", hue="Attrition", multiple="stack", bins=15)
plt.title("Years at Company: Leavers vs Stayers")
plt.tight_layout()
plt.savefig("chart_tenure_distribution.png", dpi=150)
plt.close()

print("\nCharts saved: chart_attrition_by_department.png, "
      "chart_attrition_by_overtime.png, chart_tenure_distribution.png")


# -----------------------------------------------------
# 6. Logistic regression - what predicts attrition?
# -----------------------------------------------------
features = [
    "Age", "MonthlyIncome", "YearsAtCompany", "JobSatisfaction",
    "DistanceFromHome", "WorkLifeBalance", "OverTime",
    "EnvironmentSatisfaction", "NumCompaniesWorked"
]

model_df = df[features + ["AttritionFlag"]].copy()

# Encode OverTime (Yes/No) as 1/0
le = LabelEncoder()
model_df["OverTime"] = le.fit_transform(model_df["OverTime"])  # No=0, Yes=1

X = model_df[features]
y = model_df["AttritionFlag"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print("\n--- Logistic Regression Performance ---")
print(classification_report(y_test, y_pred))

# Coefficients = relative importance/direction of each feature
coef_df = pd.DataFrame({
    "feature": features,
    "coefficient": clf.coef_[0]
}).sort_values("coefficient", ascending=False)

print("\n--- Feature Coefficients (higher = stronger link to leaving) ---")
print(coef_df)


# -----------------------------------------------------
# 7. Save cleaned dataset for use in Power BI / Tableau
# -----------------------------------------------------
df.to_csv("HR_Attrition_cleaned.csv", index=False)
print("\nCleaned dataset saved as HR_Attrition_cleaned.csv")
print("\nDone! Use the printed numbers above to write your README findings.")


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

sns.set_style("whitegrid")

df = pd.read_csv("HR_Attrition.csv")

print("Shape of dataset:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values per column:")
print(df.isnull().sum().sum(), "total missing values")

print("\nAttrition breakdown:")
print(df["Attrition"].value_counts(normalize=True) * 100)

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

df["SalaryBand"] = pd.qcut(df["MonthlyIncome"], 4, labels=["Low", "Medium", "High", "Very High"])

df["AttritionFlag"] = df["Attrition"].map({"Yes": 1, "No": 0})


print("\n--- Attrition rate by Department ---")
print(df.groupby("Department")["AttritionFlag"].mean().round(3) * 100)

print("\n--- Attrition rate by OverTime ---")
print(df.groupby("OverTime")["AttritionFlag"].mean().round(3) * 100)

print("\n--- Attrition rate by Tenure Group ---")
print(df.groupby("TenureGroup")["AttritionFlag"].mean().round(3) * 100)

print("\n--- Attrition rate by Job Satisfaction ---")
print(df.groupby("JobSatisfaction")["AttritionFlag"].mean().round(3) * 100)

numeric_cols = df.select_dtypes(include=np.number).columns
corr = df[numeric_cols].corr()["AttritionFlag"].sort_values(ascending=False)
print("\n--- Correlation with Attrition (numeric features) ---")
print(corr)

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

plt.figure(figsize=(7, 4))
sns.histplot(data=df, x="YearsAtCompany", hue="Attrition", multiple="stack", bins=15)
plt.title("Years at Company: Leavers vs Stayers")
plt.tight_layout()
plt.savefig("chart_tenure_distribution.png", dpi=150)
plt.close()

print("\nCharts saved: chart_attrition_by_department.png, "
      "chart_attrition_by_overtime.png, chart_tenure_distribution.png")


features = [
    "Age", "MonthlyIncome", "YearsAtCompany", "JobSatisfaction",
    "DistanceFromHome", "WorkLifeBalance", "OverTime",
    "EnvironmentSatisfaction", "NumCompaniesWorked"
]

model_df = df[features + ["AttritionFlag"]].copy()

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

coef_df = pd.DataFrame({
    "feature": features,
    "coefficient": clf.coef_[0]
}).sort_values("coefficient", ascending=False)

print("\n--- Feature Coefficients (higher = stronger link to leaving) ---")
print(coef_df)

df.to_csv("HR_Attrition_cleaned.csv", index=False)
print("\nCleaned dataset saved as HR_Attrition_cleaned.csv")
print("\nDone! Use the printed numbers above to write your README findings.")

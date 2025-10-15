import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# ================================== Connect to CSV file ==========================

file_path = "C:/Users/Admin/Downloads/Work Documents/Data Job and Career/Projects/Global Cybersecurity Threats 2015-2024.csv"
df = pd.read_csv("C:/Users/Admin/Downloads/Work Documents/Data Job and Career/Projects/Global Cybersecurity Threats 2015-2024.csv")

# ============================================= Data Cleaning =======================================
print("=== Dataset Overview ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print("\nColumn Names:")
print(df.columns.tolist())
print("\nData Types:")
print(df.dtypes)
print("\nFirst 5 Rows:")
print(df.head())

# ====== Missing values check ======
print("\n=== Missing Values Summary ===")
missing_summary = df.isnull().sum()
missing_percent = (missing_summary / len(df)) * 100
missing_report = pd.DataFrame({'Missing Values': missing_summary, '% Missing': missing_percent})
print(missing_report.sort_values(by='Missing Values', ascending=False))

# ====== Duplicates check ======
duplicate_count = df.duplicated().sum()
print(f"\n=== Duplicated Rows ===\nTotal duplicated rows: {duplicate_count}")

# ====== Detect anomalies / outliers using IQR ======
numeric_cols = df.select_dtypes(include=[np.number]).columns
outlier_report = {}

for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    outlier_report[col] = len(outliers)

print("\n=== Outlier Detection (IQR Method) ===")
for col, count in outlier_report.items():
    print(f"{col}: {count} potential outliers")

# ===== Logic-based anomaly check ======
# Negative financial loss (check possibility)

if "Financial_Loss_in_Million_USD" in df.columns:
    neg_impact = df[df["Financial_Loss_in_Million_USD"] < 0]
    print(f"Negative financial impact values: {len(neg_impact)}")
else: print("\nNo 'Financial_Loss_in_Million_USD' column found for negative value check.")

# Convert data types
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Financial Loss (in Million $)'] = pd.to_numeric(df['Financial Loss (in Million $)'], errors='coerce')
df['Number of Affected Users'] = pd.to_numeric(df['Number of Affected Users'], errors='coerce')
df['Incident Resolution Time (in Hours)'] = pd.to_numeric(df['Incident Resolution Time (in Hours)'], errors='coerce')


# Set seaborn style
sns.set_theme(style="white", palette="YlOrBr")

# Figure size
plt.figure(figsize=(14, 8))

# 1. Number of Attacks per Year
plt.subplot(2, 1)
sns.countplot(data=df, x="Year", order=sorted(df["Year"].unique()), palette = "YlOrBr")
plt.xticks(rotation=45)
plt.title("Cyber Attacks Over the Years", fontsize=14, fontweight='bold')

# 2. Top 10 Most Affected Countries
plt.subplot(2, 2)
top_countries = df["Country"].value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, palette = "YlOrBr")
plt.title("Top 10 Affected Countries", fontsize=14, fontweight='bold')

# 3. Attack Type Distribution
plt.subplot(2, 3)
df["Attack Type"].value_counts().plot.pie(autopct="%1.1f%%", colors=sns.color_palette("YlOrBr"),
startangle=90,wedgeprops={"edgecolor": "white"})
plt.ylabel("")
plt.title("Attack Types Distribution", fontsize=14, fontweight='bold')

# 4. Most Targeted Industries
plt.subplot(2, 4)
top_industries = df["Target Industry"].value_counts().head(10)
sns.barplot(y=top_industries.index, x=top_industries.values, palette = "YlOrBr")
plt.title("Most Targeted Industries", fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()

pivot_table = df.pivot_table(index='Country', columns='Attack Type', values='Financial Loss (in Million $)')

# Plot the Heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(pivot_table, cmap='YlOrBr', annot=True, fmt=".1f", cbar_kws={'label': 'Financial Loss (in Million $)'})
plt.xlabel("Attack Type")
plt.ylabel("Country")
plt.title("Total Financial Loss by Country and Attack Type")
plt.tight_layout()
plt.show()

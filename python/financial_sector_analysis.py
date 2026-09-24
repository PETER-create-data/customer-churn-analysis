from pathlib import Path
import pandas as pd

# Find the project folder
project_root = Path(__file__).resolve().parent.parent

# Load the cleaned CBS dataset
csv_path = project_root / "data" / "cbs_dutch_financial_clean.csv"
df = pd.read_csv(csv_path)

# Show the first 5 rows
print(df.head())

# Check dataset size
print("\nDataset shape:")
print(df.shape)

# View all column names
print("\nColumns:")
print(df.columns.tolist())

# Check data types
print("\nData types:")
print(df.dtypes)

# Check unique categories
print("\nInstitutional sectors:")
print(df["institutional_sector"].unique())

print("\nTransaction types:")
print(df["transaction_type"].unique())

print("\nPeriods:")
print(df["period"].unique())

# Check missing values
print("\nMissing values:")
print(df.isna().sum())

# Analyse financial corporations
financial_closing = df[
    (df["institutional_sector"] == "Financial corporations") &
    (df["transaction_type"] == "Closing balance sheet")
]

print("\nFinancial corporations - Closing balance sheet:")
print(
    financial_closing[
        ["period", "assets_total", "liabilities_total", "net_worth"]
    ]
)

# Keep annual periods only
annual_financial = financial_closing[
    financial_closing["period"].str.match(r"^\d{4}\*?$")
].copy()

# Calculate year-over-year asset growth
annual_financial["asset_growth_pct"] = (
    annual_financial["assets_total"].pct_change() * 100
)

print("\nAnnual asset growth - Financial corporations:")
print(
    annual_financial[
        ["period", "assets_total", "asset_growth_pct"]
    ]
)

# Find strongest growth and largest decline
highest_growth = annual_financial.loc[
    annual_financial["asset_growth_pct"].idxmax()
]

largest_decline = annual_financial.loc[
    annual_financial["asset_growth_pct"].idxmin()
]

print("\nStrongest asset growth:")
print(
    highest_growth["period"],
    round(highest_growth["asset_growth_pct"], 2),
    "%"
)

print("\nLargest asset decline:")
print(
    largest_decline["period"],
    round(largest_decline["asset_growth_pct"], 2),
    "%"
)

import matplotlib.pyplot as plt

# Create asset trend chart
plt.figure(figsize=(10, 6))

plt.plot(
    annual_financial["period"],
    annual_financial["assets_total"],
    marker="o"
)

plt.title("Financial Corporations Total Assets in the Netherlands")
plt.xlabel("Year")
plt.ylabel("Assets (million euros)")
plt.xticks(rotation=45)
plt.tight_layout()

# Save chart to project images folder
chart_path = project_root / "images" / "python_financial_assets_trend.png"
plt.savefig(chart_path)

plt.show()
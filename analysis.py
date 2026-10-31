
import pandas as pd

# Load the dataset
df = pd.read_csv("data/orders_sample.csv")

# Display first five rows
print(df.head())

# Check dataset size
print("Dataset shape:", df.shape)

# Check column information
print(df.info())

# Check missing values
print(df.isnull().sum())

# Clean final status
df["final_status"] = (
    df["final_status"].astype(str).str.strip().str.upper()
)

# Calculate delivered and RTO orders
print(df["final_status"].value_counts())

# Calculate RTO percentage
completed = df[df["final_status"].isin(["RTO", "DELIVERED"])]

rto_rate = (completed["final_status"] == "RTO").mean() * 100

print("RTO Rate:", round(rto_rate, 2), "%")


# RTO rate by previous customer RTOs
print("\nRTO Rate by Previous RTOs")

print(
    completed.groupby("customer_prior_rto")["final_status"]
    .apply(lambda x: (x == "RTO").mean() * 100)
)

# RTO rate by courier
print("\nRTO Rate by Courier")

print(
    completed.groupby("courier")["final_status"]
    .apply(lambda x: (x == "RTO").mean() * 100)
)

# RTO rate by marketing source
print("\nRTO Rate by Marketing Source")

print(
    completed.groupby("utm_source")["final_status"]
    .apply(lambda x: (x == "RTO").mean() * 100)
)

# RTO rate by city
print("\nRTO Rate by City")

print(
    completed.groupby("city")["final_status"]
    .apply(lambda x: (x == "RTO").mean() * 100)
)

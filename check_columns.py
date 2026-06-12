import pandas as pd

file_name = input("Enter dataset name: ")

df = pd.read_csv(f"datasets/{file_name}")

print("\nColumns:")
print(df.columns.tolist())

print("\nShape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())



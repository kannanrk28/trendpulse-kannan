import os
import pandas as pd
from datetime import datetime

# Read the file from the Task 1
file_path = "data/trends_20260405.json"
df = pd.read_json(file_path)

# Display the first few rows
print(df.head())


initial_count = len(df)
print(f"Loaded {initial_count} stories from {file_path}")


# Duplicates — remove any rows with the same post_id
id_cols = ['post_id']

for col in id_cols:
    dup_count = df.duplicated(subset=[col]).sum()
    if dup_count > 0:
        print(f"Removing {dup_count} duplicates from {col}...")
        df.drop_duplicates(subset=[col], inplace=True)

print(f"After removing duplicates: {len(df)}")

# Missing values — drop rows where post_id, title, or score is missing
required_cols = ['title', 'score']

for col in required_cols:
    null_count = df[col].isnull().sum()
    if null_count > 0:
        print(f"Removing {null_count} rows with null values in {col}...")
        df.dropna(subset=[col], inplace=True)

print(f"After removing nulls: {len(df)}")

# Data types — make sure score and num_comments are integers
numeric_cols = ['score', 'num_comments']

for col in numeric_cols:
    # 1. Convert to numeric (strings/garbage become NaN)
    # 2. Fill NaN with 0 (Assign back to the column, not the whole df!)
    # 3. Cast to integer
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
   

# Low quality — remove stories where score is less than 5
df = df[df['score'] >= 5]

print(f"After removing low scores: {len(df)}")

# Whitespace — strip extra spaces from the title column
text_cols = ['title']

for col in text_cols:
    df[col] = df[col].str.strip()

# 6. Save to CSV
# 1. Get the current date in YYYYMMDD format
current_date = datetime.now().strftime('%Y%m%d')
os.makedirs("data", exist_ok=True)
output_file = f"data/trends_clean_{current_date}.csv"
df.to_csv(output_file, index=False)
print(f"\nSaved {len(df)} rows to {output_file}")

# 7. Summary Results (Stories per category)
print("\nStories per category:")
category_counts = df['category'].value_counts()
for category, count in category_counts.items():
    print(f"  {category:<15} {count}")



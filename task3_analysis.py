import pandas as pd
import numpy as np
import os
from datetime import datetime

# Load the cleaned data from Task 2
file_path = "data/trends_clean_20260405.csv"
df = pd.read_csv(file_path)

# Display the first 5 rows
print(df.head(5))

#Display rows and columns
print(f"Data Frame Shape: {df.shape}")

# Print the average score and average num_comments across all stories
# List of columns to calculate the average for
metrics = ['score', 'num_comments']

for col in metrics:
    # Calculate the mean
    avg_value = df[col].mean()
    
    # Print the result, rounding to 2 decimal places for cleanliness
    print(f"Average {col.replace('_', ' ').title()}: {avg_value:.2f}")

# What is the mean, median, and standard deviation of score?

score_mean = np.mean(df['score'])
score_median = np.median(df['score'])
score_std = np.std(df['score'])

print(f"\nScore Statistics:")
print(f"Mean: {score_mean:.2f}")
print(f"Median: {score_median:.2f}")
print(f"Standard Deviation: {score_std:.2f}")
print(f"\nHighest Score: {df['score'].max()}")
print(f"Lowest Score: {df['score'].min()}")

# Which category has the most stories?
categories, counts = np.unique(df['category'], return_counts=True) # Get unique categories and their counts

max_idx = np.argmax(counts)# Find the index of the highest count

max_category = categories[max_idx] # Use that index to get the category name and the count value
highest_count = counts[max_idx]

print(f"The category with the most stories is: {max_category} and the count is ({highest_count} stories out of {len(df)} total stories)")

# Which story has the most comments? Print its title and comment count.
max_idx = np.argmax(df['num_comments'])

print(f"Most Commented Story: {df['title'][max_idx]}")
print(f"Comment Count: {df['num_comments'][max_idx]}")

# Add these two new columns to your DataFrame:
# 1. Calculate the 'engagement' column
# We add +1 to the score to avoid the "Division by Zero" error
df['engagement'] = df['num_comments'] / (df['score'] + 1)

# 2. Calculate the 'is_popular' column
avg_score = df['score'].mean()
df['is_popular'] = df['score'] > avg_score

# 3. View the first 5 rows to verify
print(f"Average Score: {avg_score:.2f}")
print(df[['title', 'score', 'num_comments', 'engagement', 'is_popular']].head())


# 1. Define the output path

current_date = datetime.now().strftime('%Y%m%d')
output_analysed_filename = f"data/trends_analysed_{current_date}.csv"

# 2. Ensure the directory exists (just in case)
os.makedirs("data", exist_ok=True)

# 3. Save the DataFrame
# index=False prevents pandas from adding an extra 'Unnamed: 0' column
df.to_csv(output_analysed_filename, index=False)

# 4. Print confirmation with a quick summary
print("-" * 30)
print(f"✅ SUCCESS: Analysis complete!")
print(f"File saved to: {output_analysed_filename}")
print(f"New columns added: 'engagement' and 'is_popular'")
print(f"Total rows exported: {len(df)}")
print("-" * 30)
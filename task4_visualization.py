import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Define a helper function to shorten titles
def shorten_text(text):
    if len(text) > 50:
        return text[:47] + "..."
    else:
        return text

# 2. Load the data
file_path = 'data/trends_analysed_20260406.csv'
df = pd.read_csv(file_path)
print(f"Setup Complete: Loaded {len(df)} rows.")
print(f"Output folder 'outputs/' is ready.")


# 3. Filter Top 10 Stories by Score
top_10 = df.sort_values(by='score', ascending=False).head(10)

# 4. Apply the function to the title column
top_10['short_title'] = top_10['title'].apply(shorten_text)

# 5. Create the Horizontal Bar Chart
plt.figure(figsize=(10, 6))
# We reverse the order using [::-1] so the #1 story is at the top
plt.barh(top_10['short_title'][::-1], top_10['score'][::-1], color='skyblue')

# 6. Add Labels and Title
plt.title('Top 10 Stories by Score', fontsize=14, fontweight='bold')
plt.xlabel('Score')
plt.ylabel('Story Title')
plt.tight_layout()

# 7. Save and Show
os.makedirs("outputs", exist_ok=True)
plt.savefig('outputs/chart1_top_stories.png')
plt.show()

print("Chart 1 saved to outputs/chart1_top_stories.png")

# Create a bar chart showing how many stories came from each category

# 2. Count stories per category
# value_counts() gives us the labels and the numbers automatically
cat_counts = df['category'].value_counts()

# 3. Create a list of colors (one for each unique category)
# You can use a Matplotlib colormap for an automatic rainbow effect
colors = plt.cm.Paired(range(len(cat_counts)))

# 4. Create the Bar Chart
plt.figure(figsize=(10, 6))
plt.bar(cat_counts.index, cat_counts.values, color=colors)

# 5. Add Labels and Title
plt.title('Total Stories per Category', fontsize=14, fontweight='bold')
plt.xlabel('Category', fontsize=12)
plt.ylabel('Number of Stories', fontsize=12)

# Optional: Add gridlines for readability on the y-axis
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 6. Save and Show
plt.savefig('outputs/chart2_categories.png')
plt.show()

print("Chart 2 saved to outputs/chart2_categories.png")

# Score vs Comments Scatter Plot with Popularity Highlight
# 2. Split data into two groups for easier legend handling
# This ensures that we have separate 'labels' for each set of dots
popular = df[df['is_popular'] == True]
not_popular = df[df['is_popular'] == False]

# 3. Create the Scatter Plot
plt.figure(figsize=(10, 6))

# Plot non-popular stories first (using gray dots)
plt.scatter(not_popular['score'], not_popular['num_comments'], 
            alpha=0.6, label='Not Popular', color='gray')

# Plot popular stories on top (using orange dots for contrast)
plt.scatter(popular['score'], popular['num_comments'], 
            alpha=0.8, label='Popular', color='orange', edgecolor='black')

# 4. Add Labels, Legend, and Title
plt.title('Score vs Number of Comments', fontsize=14, fontweight='bold')
plt.xlabel('Score (Upvotes)', fontsize=12)
plt.ylabel('Number of Comments', fontsize=12)

# Legend uses the 'label' from the scatter commands above
plt.legend(title='Story Status')

# Optional: Add gridlines to help guide the eye
plt.grid(True, linestyle=':', alpha=0.6)

# 5. Save and Show
# Always save before showing!
plt.savefig('outputs/chart3_scatter.png')
plt.show()

print("Chart 3 saved to outputs/chart3_scatter.png")

# create a dashboard with all three charts together
# 2. Setup the figure and axes (1 row, 3 columns)
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# --- Chart 1: Stories per Category ---
category_counts = df['category'].value_counts()
axes[0].bar(category_counts.index, category_counts.values, color='skyblue', edgecolor='black')
axes[0].set_title('Stories per Category', fontsize=12)
axes[0].set_ylabel('Count')
axes[0].tick_params(axis='x', rotation=45)

# --- Chart 2: Average Score per Category ---
avg_scores = df.groupby('category')['score'].mean().sort_values(ascending=False)
axes[1].bar(avg_scores.index, avg_scores.values, color='salmon', edgecolor='black')
axes[1].set_title('Avg Score by Category', fontsize=12)
axes[1].set_ylabel('Avg Score')
axes[1].tick_params(axis='x', rotation=45)

# --- Chart 3: Score vs Comments Relationship ---
axes[2].scatter(df['score'], df['num_comments'], alpha=0.5, color='green')
axes[2].set_title('Score vs Comments', fontsize=12)
axes[2].set_xlabel('Score')
axes[2].set_ylabel('Comments')

# 3. Add the Overall Title
plt.suptitle('TrendPulse Dashboard', fontsize=16, fontweight='bold')

# 4. Final layout adjustments and saving
plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust to leave room for the suptitle
plt.savefig('outputs/dashboard.png')
plt.show()
print("Dashboard saved to outputs/dashboard.png")
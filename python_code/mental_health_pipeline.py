import pandas as pd

# Load dataset
df = pd.read_csv('mental_health_pipeline/Student_mental_health.csv')

# Create Age Bands
bins = [0, 19, 30, 40, 100]
labels = ['<19', '20–30', '30–40', '40+']
df['Age Band'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

# Filter by gender
females = df[df['Choose your gender'] == 'Female']
males = df[df['Choose your gender'] == 'Male']

# Count how many women answered 'Yes'
females_with_depression = females[females['Do you have Depression?'] == 'Yes']
females_with_anxiety = females[females['Do you have Anxiety?'] == 'Yes']

# Count how many men answered 'Yes'
males_with_depression = males[males['Do you have Depression?'] == 'Yes']
males_with_anxiety = males[males['Do you have Anxiety?'] == 'Yes']

# Calculate % females
depression_pct_females = (len(females_with_depression) / len(females)) * 100
anxiety_pct_females = (len(females_with_anxiety) / len(females)) * 100

# Calculate % males
depression_pct_males = (len(males_with_depression) / len(males)) * 100
anxiety_pct_males = (len(males_with_anxiety) / len(males)) * 100

# === Overall Summary by Gender ===
print("=== Mental Health Percentages by Gender ===")
print(f"Female - Depression: {depression_pct_females:.2f}%")
print(f"Female - Anxiety:    {anxiety_pct_females:.2f}%")
print(f"Male   - Depression: {depression_pct_males:.2f}%")
print(f"Male   - Anxiety:    {anxiety_pct_males:.2f}%")

# Build summary table by gender
summary = pd.DataFrame({
    'Gender': ['Female', 'Male'],
    'Depression (%)': [depression_pct_females, depression_pct_males],
    'Anxiety (%)': [anxiety_pct_females, anxiety_pct_males],
    'Count': [len(females), len(males)]
})
print("\nSummary Table by Gender:")
print(summary)

# === Optional: Breakdown by Gender AND Age Band ===
breakdown = df.groupby(['Choose your gender', 'Age Band']).agg(
    Total=('Age', 'count'),
    Depression=('Do you have Depression?', lambda x: (x == 'Yes').sum()),
    Anxiety=('Do you have Anxiety?', lambda x: (x == 'Yes').sum())
).reset_index()

# Calculate percentages
breakdown['Depression (%)'] = round((breakdown['Depression'] / breakdown['Total']) * 100, 2)
breakdown['Anxiety (%)'] = round((breakdown['Anxiety'] / breakdown['Total']) * 100, 2)

print("\nDetailed Breakdown by Gender and Age Band:")
print(breakdown)

# Optional: Export both
summary.to_csv('mental_health_pipeline/mental_health_summary_by_gender.csv', index=False)
breakdown.to_csv('mental_health_pipeline/mental_health_by_gender_ageband.csv', index=False)

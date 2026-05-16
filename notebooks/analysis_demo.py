# notebooks/analysis_demo.py
# This serves as an exploratory analysis notebook equivalent

"""
Exploratory Data Analysis for Fintech Reviews
==============================================

This notebook-style script demonstrates the key findings from our analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('../data/reviews_with_sentiment.csv')

print("="*60)
print("EXPLORATORY DATA ANALYSIS")
print("="*60)

# 1. Data Overview
print("\n1. DATASET OVERVIEW")
print("-"*40)
print(f"Total reviews: {len(df)}")
print(f"Banks: {df['bank'].unique()}")
print(f"Date range: {df['review_date'].min()} to {df['review_date'].max()}")

# 2. Rating Statistics
print("\n2. RATING STATISTICS")
print("-"*40)
print(df.groupby('bank')['rating'].describe())

# 3. Sentiment Distribution
print("\n3. SENTIMENT DISTRIBUTION")
print("-"*40)
sentiment_counts = df.groupby(['bank', 'sentiment_label']).size().unstack()
print(sentiment_counts)

# 4. Review Length Analysis
print("\n4. REVIEW LENGTH ANALYSIS")
print("-"*40)
print(f"Average review length: {df['review_length'].mean():.0f} characters")
print(f"Shortest review: {df['review_length'].min()} chars")
print(f"Longest review: {df['review_length'].max()} chars")

# 5. Correlation between rating and review length
print("\n5. RATING vs REVIEW LENGTH")
print("-"*40)
print(df.groupby('rating')['review_length'].mean())

# 6. Sample reviews by sentiment
print("\n6. SAMPLE REVIEWS")
print("-"*40)
print("\n--- POSITIVE REVIEWS ---")
for review in df[df['sentiment_label'] == 'POSITIVE']['cleaned_review'].head(3):
    print(f"  • {review[:100]}...")

print("\n--- NEGATIVE REVIEWS ---")
for review in df[df['sentiment_label'] == 'NEGATIVE']['cleaned_review'].head(3):
    print(f"  • {review[:100]}...")

print("\n" + "="*60)
print("END OF ANALYSIS")
print("="*60)
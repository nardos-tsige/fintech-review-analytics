import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("="*50)
print("TASK 4: GENERATING VISUALIZATIONS")
print("="*50)

# Create plots folder
os.makedirs("plots", exist_ok=True)

# Load data
df = pd.read_csv('data/reviews_with_sentiment.csv')
print(f" Loaded {len(df)} reviews")

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")

# ============================================
# PLOT 1: Sentiment Distribution by Bank
# ============================================
print("\n Creating Plot 1: Sentiment Distribution...")
sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'])
sentiment_by_bank_pct = sentiment_by_bank.div(sentiment_by_bank.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(10, 6))
sentiment_by_bank_pct.plot(kind='bar', stacked=True, ax=ax, 
                            color=['#E74C3C', '#F39C12', '#27AE60'])
ax.set_title('Sentiment Distribution by Bank', fontsize=14, fontweight='bold')
ax.set_xlabel('Bank', fontsize=12)
ax.set_ylabel('Percentage (%)', fontsize=12)
ax.legend(title='Sentiment', loc='upper right')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

for c in ax.containers:
    ax.bar_label(c, fmt='%.0f%%', label_type='center')

plt.tight_layout()
plt.savefig('plots/sentiment_distribution.png', dpi=300)
plt.close()
print("   Saved: plots/sentiment_distribution.png")

# ============================================
# PLOT 2: Average Rating by Bank
# ==========================================
print("\n Creating Plot 2: Average Rating...")
avg_ratings = df.groupby('bank')['rating'].mean().sort_values()

fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#2E86C1', '#28B463', '#E74C3C']
bars = ax.bar(avg_ratings.index, avg_ratings.values, color=colors)
ax.set_title('Average Rating by Bank', fontsize=14, fontweight='bold')
ax.set_xlabel('Bank', fontsize=12)
ax.set_ylabel('Average Rating (1-5 stars)', fontsize=12)
ax.set_ylim(0, 5)

for bar, value in zip(bars, avg_ratings.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
            f'{value:.2f}', ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('plots/avg_rating.png', dpi=300)
plt.close()
print("   Saved: plots/avg_rating.png")

# ============================================
# PLOT 3: Rating Distribution (Histogram)
# ============================================
print("\n Creating Plot 3: Rating Distribution...")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

for i, bank in enumerate(df['bank'].unique()):
    bank_data = df[df['bank'] == bank]
    rating_counts = bank_data['rating'].value_counts().sort_index()
    
    axes[i].bar(rating_counts.index, rating_counts.values, color=colors[i])
    axes[i].set_title(bank, fontsize=12, fontweight='bold')
    axes[i].set_xlabel('Rating (Stars)', fontsize=10)
    axes[i].set_ylabel('Number of Reviews', fontsize=10)
    axes[i].set_xticks([1, 2, 3, 4, 5])
    
    mean_rating = bank_data['rating'].mean()
    axes[i].axvline(x=mean_rating, color='red', linestyle='--', alpha=0.7)
    axes[i].text(mean_rating + 0.2, max(rating_counts.values) * 0.9, 
                 f'Mean: {mean_rating:.2f}', fontsize=9)

plt.suptitle('Rating Distribution by Bank', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('plots/rating_distribution.png', dpi=300)
plt.close()
print("   Saved: plots/rating_distribution.png")

# ============================================
# PLOT 4: Sentiment Pie Chart (Overall)
# ============================================
print("\n Creating Plot 4: Overall Sentiment...")
overall_sentiment = df['sentiment_label'].value_counts()

fig, ax = plt.subplots(figsize=(8, 8))
colors_pie = ['#27AE60', '#E74C3C', '#F39C12']
wedges, texts, autotexts = ax.pie(overall_sentiment.values, 
                                    labels=overall_sentiment.index,
                                    autopct='%1.1f%%',
                                    colors=colors_pie,
                                    explode=(0.05, 0.05, 0.05))
ax.set_title('Overall Sentiment Distribution', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('plots/overall_sentiment_pie.png', dpi=300)
plt.close()
print("   Saved: plots/overall_sentiment_pie.png")

# ============================================
# SUMMARY
# ============================================
print("\n" + "="*50)
print(" TASK 4 COMPLETE! All visualizations saved in 'plots/' folder")
print("="*50)
print("\n Generated files:")
for f in os.listdir('plots'):
    print(f"   - {f}")
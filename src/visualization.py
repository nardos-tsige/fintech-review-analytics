# src/visualization.py
"""
Visualization functions
"""

import matplotlib.pyplot as plt
import seaborn as sns

def plot_sentiment_distribution(df, save_path='plots/sentiment_distribution.png'):
    """Create sentiment distribution plot"""
    sentiment_by_bank = pd.crosstab(df['bank'], df['sentiment_label'])
    sentiment_by_bank_pct = sentiment_by_bank.div(sentiment_by_bank.sum(axis=1), axis=0) * 100
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sentiment_by_bank_pct.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Sentiment Distribution by Bank')
    ax.set_xlabel('Bank')
    ax.set_ylabel('Percentage (%)')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

def plot_rating_distribution(df, save_path='plots/rating_distribution.png'):
    """Create rating distribution plot"""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for i, bank in enumerate(df['bank'].unique()):
        bank_data = df[df['bank'] == bank]
        ratings = bank_data['rating'].value_counts().sort_index()
        axes[i].bar(ratings.index, ratings.values)
        axes[i].set_title(bank)
        axes[i].set_xlabel('Rating')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
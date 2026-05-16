# src/utils.py
"""
Utility functions for data processing and analysis
"""

import re
import pandas as pd

def clean_review_text(text):
    """Clean review text by removing special characters"""
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?]', '', text)
    text = text.lower()
    text = ' '.join(text.split())
    return text

def get_sentiment_summary(df):
    """Get sentiment summary by bank"""
    return pd.crosstab(df['bank'], df['sentiment_label'])

def get_rating_stats(df):
    """Get rating statistics by bank"""
    return df.groupby('bank')['rating'].describe()
    
# scripts/preprocess_data.py

import pandas as pd
import re

def clean_text(text):
    """Clean review text"""
    if pd.isna(text):
        return ""
    
    text = str(text)
    # Remove special characters but keep letters, numbers, spaces, basic punctuation
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = ' '.join(text.split())
    
    return text

def preprocess_data():
    """Main preprocessing function"""
    print("LOADING raw data...")
    df = pd.read_csv("data/raw/raw_reviews.csv")
    print(f"Loaded {len(df)} total reviews")
    
    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset=['review_id'])
    print(f"Removed {before - len(df)} duplicate reviews")
    
    # Remove rows with missing review text or rating
    before = len(df)
    df = df.dropna(subset=['review_text', 'rating'])
    print(f"Removed {before - len(df)} rows with missing data")
    
    # Clean the review text
    print("Cleaning review text...")
    df['cleaned_review'] = df['review_text'].apply(clean_text)
    
    # Remove rows with empty reviews after cleaning
    before = len(df)
    df = df[df['cleaned_review'].str.len() > 0]
    print(f"Removed {before - len(df)} empty reviews after cleaning")
    
    # Add helpful columns
    df['review_length'] = df['cleaned_review'].str.len()
    df['word_count'] = df['cleaned_review'].str.split().str.len()
    
    # Keep only needed columns
    final_columns = ['review_id', 'cleaned_review', 'rating', 'review_date', 'bank', 'source', 'review_length', 'word_count']
    df = df[final_columns]
    
    # Save processed data
    df.to_csv("data/processed_reviews.csv", index=False)
    
    print("\n" + "="*50)
    print("PROCESSING COMPLETE!")
    print("="*50)
    print(f"Final dataset: {len(df)} reviews")
    print(f"Reviews per bank:\n{df['bank'].value_counts()}")
    print(f"Saved to: data/processed_reviews.csv")
    
    return df

if __name__ == "__main__":
    df = preprocess_data()
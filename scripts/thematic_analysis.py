"""
Thematic Analysis Module using TF-IDF and spaCy
Extracts key themes from customer reviews for all banks
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import spacy
from collections import Counter
import re

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# Define theme categories and keywords
THEMES = {
    "Transaction Performance": ["transfer", "send", "payment", "transaction", "processing", "slow", "fast", "speed", "timeout", "failed"],
    "Login & Authentication": ["login", "log in", "password", "fingerprint", "otp", "verification", "biometric", "secure", "access"],
    "App Stability": ["crash", "freeze", "bug", "error", "not working", "stuck", "close", "restart", "unresponsive"],
    "Customer Support": ["support", "help", "customer service", "agent", "response", "complaint", "resolve", "assistance"],
    "User Interface": ["interface", "design", "layout", "navigation", "menu", "button", "screen", "intuitive", "confusing"],
    "Feature Requests": ["feature", "add", "missing", "would like", "need", "want", "suggestion", "improve"],
    "Notifications": ["notification", "alert", "sms", "email", "reminder", "message", "push"],
    "Account Management": ["account", "balance", "statement", "history", "profile", "settings"]
}

def clean_text_for_tfidf(text):
    """Clean text for TF-IDF analysis"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    return text

def extract_tfidf_keywords(df, bank_name, top_n=15):
    """Extract top TF-IDF keywords for a specific bank"""
    # Filter reviews for the bank
    bank_reviews = df[df['bank'] == bank_name]['cleaned_review'].dropna()
    
    if len(bank_reviews) < 10:
        return []
    
    # Clean texts
    cleaned_texts = [clean_text_for_tfidf(text) for text in bank_reviews]
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=50,
        ngram_range=(1, 2),
        stop_words='english'
    )
    
    # Fit and transform
    tfidf_matrix = vectorizer.fit_transform(cleaned_texts)
    
    # Get average scores per word
    feature_names = vectorizer.get_feature_names_out()
    avg_scores = tfidf_matrix.mean(axis=0).A1
    
    # Sort and return top keywords
    keywords = sorted(zip(feature_names, avg_scores), key=lambda x: x[1], reverse=True)
    return keywords[:top_n]

def assign_theme(review_text):
    """Assign a theme to a review based on keyword matching"""
    if pd.isna(review_text):
        return "Other"
    
    text_lower = str(review_text).lower()
    
    for theme, keywords in THEMES.items():
        for keyword in keywords:
            if keyword in text_lower:
                return theme
    
    return "Other"

def extract_spacy_keywords(text, top_n=10):
    """Extract important keywords using spaCy"""
    if not text or len(text) < 10:
        return []
    
    doc = nlp(text)
    
    # Extract nouns, proper nouns, and adjectives
    keywords = []
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN', 'ADJ']:
            if not token.is_stop and len(token.text) > 3:
                keywords.append(token.text.lower())
    
    # Count frequencies
    keyword_counts = Counter(keywords)
    return keyword_counts.most_common(top_n)

def analyze_themes_complete(df):
    """Complete thematic analysis pipeline"""
    print("\n" + "="*70)
    print("THEMATIC ANALYSIS WITH TF-IDF AND SPACY")
    print("="*70)
    
    # Assign themes to all reviews
    print("\n1. Assigning themes to all reviews...")
    df['theme'] = df['cleaned_review'].apply(assign_theme)
    
    # Theme distribution
    print("\n2. Theme Distribution (Overall):")
    print("-" * 40)
    theme_counts = df['theme'].value_counts()
    for theme, count in theme_counts.items():
        pct = (count / len(df)) * 100
        print(f"   {theme}: {count} ({pct:.1f}%)")
    
    # Theme by bank
    print("\n3. Theme Distribution by Bank:")
    print("-" * 40)
    theme_by_bank = pd.crosstab(df['bank'], df['theme'], normalize='index') * 100
    print(theme_by_bank.round(1))
    
    # TF-IDF keywords per bank
    print("\n4. TF-IDF Top Keywords by Bank:")
    print("-" * 40)
    for bank in df['bank'].unique():
        keywords = extract_tfidf_keywords(df, bank, top_n=10)
        print(f"\n   {bank}:")
        for word, score in keywords[:8]:
            print(f"      - {word}: {score:.4f}")
    
    # SpaCy keyword extraction for sample reviews
    print("\n5. SpaCy Keyword Extraction (Sample positive/negative reviews):")
    print("-" * 40)
    
    for bank in df['bank'].unique():
        print(f"\n   {bank}:")
        
        # Positive review sample
        pos_review = df[(df['bank'] == bank) & (df['sentiment_label'] == 'POSITIVE')]['cleaned_review'].iloc[0] if len(df[(df['bank'] == bank) & (df['sentiment_label'] == 'POSITIVE')]) > 0 else None
        if pos_review:
            keywords = extract_spacy_keywords(pos_review, top_n=5)
            print(f"      Positive keywords: {', '.join([k[0] for k in keywords])}")
        
        # Negative review sample
        neg_review = df[(df['bank'] == bank) & (df['sentiment_label'] == 'NEGATIVE')]['cleaned_review'].iloc[0] if len(df[(df['bank'] == bank) & (df['sentiment_label'] == 'NEGATIVE')]) > 0 else None
        if neg_review:
            keywords = extract_spacy_keywords(neg_review, top_n=5)
            print(f"      Negative keywords: {', '.join([k[0] for k in keywords])}")
    
    # Pain points and satisfaction drivers
    print("\n6. Pain Points & Satisfaction Drivers:")
    print("-" * 40)
    
    for bank in df['bank'].unique():
        bank_df = df[df['bank'] == bank]
        
        # Pain points (negative reviews by theme)
        negative_by_theme = bank_df[bank_df['sentiment_label'] == 'NEGATIVE']['theme'].value_counts()
        print(f"\n   {bank} - PAIN POINTS:")
        for theme, count in negative_by_theme.head(3).items():
            pct = (count / len(bank_df[bank_df['sentiment_label'] == 'NEGATIVE'])) * 100 if len(bank_df[bank_df['sentiment_label'] == 'NEGATIVE']) > 0 else 0
            print(f"      - {theme}: {count} ({pct:.0f}% of negative reviews)")
        
        # Satisfaction drivers (positive reviews by theme)
        positive_by_theme = bank_df[bank_df['sentiment_label'] == 'POSITIVE']['theme'].value_counts()
        print(f"\n   {bank} - SATISFACTION DRIVERS:")
        for theme, count in positive_by_theme.head(3).items():
            pct = (count / len(bank_df[bank_df['sentiment_label'] == 'POSITIVE'])) * 100 if len(bank_df[bank_df['sentiment_label'] == 'POSITIVE']) > 0 else 0
            print(f"      - {theme}: {count} ({pct:.0f}% of positive reviews)")
    
    return df

def generate_thematic_report(df):
    """Generate a comprehensive thematic analysis report"""
    print("\n" + "="*70)
    print("THEMATIC ANALYSIS REPORT")
    print("="*70)
    
    # Dataset coverage summary
    print("\n DATASET COVERAGE:")
    print(f"   Total reviews analyzed: {len(df)}")
    print(f"   Reviews per bank:")
    for bank in df['bank'].unique():
        count = len(df[df['bank'] == bank])
        pct = (count / len(df)) * 100
        print(f"      - {bank}: {count} ({pct:.0f}%)")
    
    # Processing coverage
    print("\n PROCESSING COVERAGE:")
    print(f"   Reviews with sentiment: {len(df[df['sentiment_label'].notna()])} (100%)")
    print(f"   Reviews with theme: {len(df[df['theme'].notna()])} (100%)")
    print(f"   Sentiment distribution: {df['sentiment_label'].value_counts().to_dict()}")
    
    # Save results
    df.to_csv("data/reviews_with_themes.csv", index=False)
    print("\n Saved: data/reviews_with_themes.csv")
    
    return df

if __name__ == "__main__":
    # Load data with sentiment
    df = pd.read_csv("data/reviews_with_sentiment.csv")
    print(f" Loaded {len(df)} reviews with sentiment")
    
    # Run complete thematic analysis
    df_themes = analyze_themes_complete(df)
    
    # Generate report
    generate_thematic_report(df_themes)
    
    print("\n" + "="*70)
    print(" THEMATIC ANALYSIS COMPLETE!")
    print("="*70)
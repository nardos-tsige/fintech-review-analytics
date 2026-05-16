"""
Complete Pipeline Runner
Runs all tasks from data collection to final output
"""

import subprocess
import sys
import pandas as pd

def print_section(title):
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def run_script(script_name):
    """Run a Python script and return success status"""
    print(f"\n▶ Running: {script_name}")
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    return result.returncode == 0

def main():
    print_section("FINTECH REVIEW ANALYTICS - COMPLETE PIPELINE")
    
    # Check if data exists
    import os
    
    if not os.path.exists("data/reviews_with_themes.csv"):
        print("\n Running full pipeline...")
        
        # Task 1: Data Collection
        if not os.path.exists("data/processed_reviews.csv"):
            print("\n Step 1: Data Collection & Preprocessing")
            run_script("scripts/scrape_reviews.py")
            run_script("scripts/preprocess_data.py")
        else:
            print("\n Data already exists, skipping Task 1")
        
        # Task 2: Sentiment Analysis
        if not os.path.exists("data/reviews_with_sentiment.csv"):
            print("\n Step 2: Sentiment Analysis")
            run_script("scripts/sentiment_analysis.py")
        else:
            print("\n Sentiment data exists, skipping Task 2")
        
        # Task 2b: Thematic Analysis
        print("\n Step 3: Thematic Analysis (TF-IDF + spaCy)")
        run_script("scripts/thematic_analysis.py")
    else:
        print("\n Complete dataset found: data/reviews_with_themes.csv")
        
        # Load and display summary
        df = pd.read_csv("data/reviews_with_themes.csv")
        print(f"\n Dataset Summary:")
        print(f"   Total reviews: {len(df)}")
        print(f"   Banks: {df['bank'].unique()}")
        print(f"   Themes: {df['theme'].unique()}")
        print(f"   Sentiment distribution: {df['sentiment_label'].value_counts().to_dict()}")
    
    # Task 3: Database
    print("\n Step 4: PostgreSQL Database")
    run_script("scripts/insert_to_db.py")
    
    # Task 4: Visualizations
    print("\n Step 5: Visualizations")
    run_script("scripts/visualizations.py")
    
    print_section("PIPELINE COMPLETE!")
    print("\n Output files:")
    print("   - data/processed_reviews.csv")
    print("   - data/reviews_with_sentiment.csv")
    print("   - data/reviews_with_themes.csv")
    print("   - plots/ (4 PNG files)")
    print("   - PostgreSQL database: bank_reviews")

if __name__ == "__main__":
    main()
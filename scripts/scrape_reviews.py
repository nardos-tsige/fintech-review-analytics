# scripts/scrape_reviews.py

import logging
import sys
import traceback

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Your existing code here
        pass
    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()

"""
Google Play Store Review Scraper for Ethiopian Banking Apps
Collects reviews for CBE, Bank of Abyssinia, and Dashen Bank
"""

from google_play_scraper import reviews, Sort
import pandas as pd
import time
from datetime import datetime

# The app IDs for each bank's app on Google Play Store
BANK_APPS = {
    "Commercial Bank of Ethiopia": "com.cbe.mobile",
    "Bank of Abyssinia": "com.abyssinia.bank",
    "Dashen Bank": "com.dashen.mobilebanking"
}

def scrape_bank_reviews(app_name, app_id, count=500):
    """
    Scrape reviews for one bank
    """
    print(f"Scraping {app_name}...")
    
    try:
        # Get reviews from Google Play
        result, _ = reviews(
            app_id,
            lang='en',
            country='et',
            sort=Sort.NEWEST,
            count=count
        )
        
        # Convert to list of dictionaries
        reviews_data = []
        for review in result:
            reviews_data.append({
                'review_id': review['reviewId'],
                'review_text': review['content'],
                'rating': review['score'],
                'review_date': review['at'].strftime('%Y-%m-%d'),
                'bank': app_name,
                'source': 'Google Play'
            })
        
        df = pd.DataFrame(reviews_data)
        print(f"Got {len(df)} reviews for {app_name}")
        return df
        
    except Exception as e:
        print(f"Error scraping {app_name}: {e}")
        return pd.DataFrame()

def scrape_all_banks():
    """Scrape all three banks"""
    all_reviews = []
    
    for bank_name, app_id in BANK_APPS.items():
        print("\n" + "="*50)
        print(f"Scraping: {bank_name}")
        print("="*50)
        
        df = scrape_bank_reviews(bank_name, app_id, count=500)
        
        if not df.empty:
            all_reviews.append(df)
        
        # Wait 2 seconds between requests (be nice to Google)
        time.sleep(2)
    
    # Combine all data
    if all_reviews:
        combined_df = pd.concat(all_reviews, ignore_index=True)
        print(f"\n TOTAL REVIEWS COLLECTED: {len(combined_df)}")
        return combined_df
    else:
        return pd.DataFrame()

# RUN THE SCRAPER
if __name__ == "__main__":
    print("STARTING WEB SCRAPER...")
    print("This will take 2-3 minutes...")
    
    reviews_df = scrape_all_banks()
    
    if not reviews_df.empty:
        # Save to CSV
        reviews_df.to_csv("data/raw/raw_reviews.csv", index=False)
        print("\n Data saved to data/raw/raw_reviews.csv")
        
        # Show summary
        print("\n SUMMARY BY BANK:")
        print(reviews_df.groupby('bank').size())
        print("\n RATING DISTRIBUTION:")
        print(reviews_df['rating'].value_counts().sort_index())
    else:
        print("No data collected! Check your internet connection.")
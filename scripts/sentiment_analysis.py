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
    
import pandas as pd
from transformers import pipeline

print("Loading sentiment model...")
classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

df = pd.read_csv("data/processed_reviews.csv")
print(f"Analyzing {len(df)} reviews...")

sentiments = []
for text in df['cleaned_review']:
    if len(str(text)) > 5:
        result = classifier(str(text)[:512])[0]
        label = result['label']
        score = result['score']
        if score < 0.6:
            sentiments.append(("NEUTRAL", score))
        else:
            sentiments.append((label, score))
    else:
        sentiments.append(("NEUTRAL", 0.5))

df['sentiment_label'] = [s[0] for s in sentiments]
df['sentiment_score'] = [s[1] for s in sentiments]

df.to_csv("data/reviews_with_sentiment.csv", index=False)
print("\nResults:")
print(df['sentiment_label'].value_counts())
print("\nBy bank:")
print(pd.crosstab(df['bank'], df['sentiment_label']))
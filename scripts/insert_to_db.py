import pandas as pd
import psycopg2

print("="*50)
print("INSERTING REVIEWS INTO POSTGRESQL")
print("="*50)

# Load your sentiment data
df = pd.read_csv('data/reviews_with_sentiment.csv')
print(f" Loaded {len(df)} reviews")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host='localhost',
    database='bank_reviews',
    user='postgres',
    password='postgres',
    port='5432'
)
cur = conn.cursor()

# Bank ID mapping (from your database)
bank_ids = {
    'Commercial Bank of Ethiopia': 1,
    'Bank of Abyssinia': 2,
    'Dashen Bank': 3
}

# Insert each review
inserted = 0
for _, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO reviews (review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (review_id) DO NOTHING
        """, (
            str(row['review_id']),
            bank_ids[row['bank']],
            str(row['cleaned_review'])[:1000],
            int(row['rating']),
            str(row['review_date']),
            str(row['sentiment_label']),
            float(row.get('sentiment_score', 0.5))
        ))
        inserted += 1
    except Exception as e:
        print(f"Error: {e}")

conn.commit()
print(f" Inserted {inserted} reviews into database")

# Verify
print("\n VERIFICATION:")
cur.execute("""
    SELECT b.bank_name, COUNT(r.review_id) as count, AVG(r.rating) as avg_rating
    FROM reviews r
    JOIN banks b ON r.bank_id = b.bank_id
    GROUP BY b.bank_name
""")

for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]} reviews, avg rating: {row[2]:.2f}")

cur.close()
conn.close()
print("\n TASK 3 COMPLETE! Data is in PostgreSQL")
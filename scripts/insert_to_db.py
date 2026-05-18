"""
PostgreSQL Database Insertion Script
Loads processed review data into the database with complete schema
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
import sys
import traceback
from datetime import datetime

# Setup logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/database_insert.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'bank_reviews',
    'user': 'postgres',
    'password': 'postgres'  # Change this to your password
}

def get_bank_id_mapping(cur):
    """Get mapping of bank names to IDs from database"""
    cur.execute("SELECT bank_id, bank_name FROM banks")
    return {bank_name: bank_id for bank_id, bank_name in cur.fetchall()}

def create_schema_if_not_exists(conn):
    """Create database schema if tables don't exist"""
    schema_sql = """
    -- Banks Table
    CREATE TABLE IF NOT EXISTS banks (
        bank_id SERIAL PRIMARY KEY,
        bank_name VARCHAR(100) NOT NULL UNIQUE,
        app_name VARCHAR(200),
        app_id VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Reviews Table with all columns
    CREATE TABLE IF NOT EXISTS reviews (
        review_id VARCHAR(100) PRIMARY KEY,
        bank_id INTEGER NOT NULL REFERENCES banks(bank_id),
        review_text TEXT NOT NULL,
        rating INTEGER CHECK (rating >= 1 AND rating <= 5),
        review_date DATE NOT NULL,
        source VARCHAR(50) DEFAULT 'Google Play',
        sentiment_label VARCHAR(20),
        sentiment_score FLOAT,
        identified_theme VARCHAR(100),
        review_length INTEGER,
        word_count INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
    CREATE INDEX IF NOT EXISTS idx_reviews_review_date ON reviews(review_date);
    CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label);
    CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
    CREATE INDEX IF NOT EXISTS idx_reviews_theme ON reviews(identified_theme);

    -- Insert bank data if not exists
    INSERT INTO banks (bank_name, app_name, app_id) VALUES
        ('Commercial Bank of Ethiopia', 'CBE Mobile Banking', 'com.cbe.mobilebanking'),
        ('Bank of Abyssinia', 'BOA Mobile Banking', 'com.bankofabyssinia.boa'),
        ('Dashen Bank', 'Dashen Mobile Banking', 'com.dashen.mbank')
    ON CONFLICT (bank_name) DO NOTHING;
    """
    
    try:
        cur = conn.cursor()
        cur.execute(schema_sql)
        conn.commit()
        logger.info(" Database schema created/verified successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create schema: {e}")
        conn.rollback()
        return False

def insert_reviews(df, conn):
    """
    Insert reviews into the database with complete column mapping
    
    Args:
        df: DataFrame with all review data
        conn: Database connection
    """
    cur = conn.cursor()
    
    # Get bank ID mapping
    bank_mapping = get_bank_id_mapping(cur)
    logger.info(f"Bank mapping: {bank_mapping}")
    
    # Prepare data for insertion
    reviews_data = []
    missing_banks = set()
    
    for idx, row in df.iterrows():
        bank_name = row['bank']
        if bank_name not in bank_mapping:
            missing_banks.add(bank_name)
            continue
            
        # Build tuple for insertion
        review_tuple = (
            str(row['review_id']),                                    # review_id
            bank_mapping[bank_name],                                  # bank_id
            str(row['cleaned_review'])[:5000],                       # review_text
            int(row['rating']),                                       # rating
            str(row['review_date']),                                  # review_date
            'Google Play',                                            # source
            str(row.get('sentiment_label', 'NEUTRAL')),              # sentiment_label
            float(row.get('sentiment_score', 0.5)),                  # sentiment_score
            str(row.get('theme', 'Other'))[:100],                    # identified_theme
            int(row.get('review_length', 0)),                        # review_length
            int(row.get('word_count', 0))                            # word_count
        )
        reviews_data.append(review_tuple)
    
    if missing_banks:
        logger.warning(f"Missing bank mappings for: {missing_banks}")
    
    if not reviews_data:
        logger.error("No data to insert!")
        return 0
    
    # Insert using execute_values for better performance
    insert_sql = """
        INSERT INTO reviews (
            review_id, bank_id, review_text, rating, review_date, 
            source, sentiment_label, sentiment_score, identified_theme, 
            review_length, word_count
        )
        VALUES %s
        ON CONFLICT (review_id) DO UPDATE SET
            sentiment_label = EXCLUDED.sentiment_label,
            sentiment_score = EXCLUDED.sentiment_score,
            identified_theme = EXCLUDED.identified_theme,
            review_length = EXCLUDED.review_length,
            word_count = EXCLUDED.word_count
    """
    
    try:
        execute_values(cur, insert_sql, reviews_data, page_size=500)
        conn.commit()
        logger.info(f" Inserted/Updated {len(reviews_data)} reviews into database")
        return len(reviews_data)
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        conn.rollback()
        return 0

def verify_data_integrity(conn):
    """Run verification queries to ensure data quality"""
    logger.info("\n" + "="*50)
    logger.info("VERIFYING DATA INTEGRITY")
    logger.info("="*50)
    
    cur = conn.cursor()
    
    # Query 1: Review counts per bank
    cur.execute("""
        SELECT b.bank_name, COUNT(r.review_id) as review_count, 
               ROUND(AVG(r.rating), 2) as avg_rating
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id
        GROUP BY b.bank_name
        ORDER BY avg_rating DESC
    """)
    
    logger.info("\n Reviews per bank:")
    for row in cur.fetchall():
        logger.info(f"   {row[0]}: {row[1]} reviews, avg rating: {row[2]}★")
    
    # Query 2: Check for nulls in key columns
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) as null_text,
            SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END) as null_rating,
            SUM(CASE WHEN review_date IS NULL THEN 1 ELSE 0 END) as null_date,
            SUM(CASE WHEN sentiment_label IS NULL THEN 1 ELSE 0 END) as null_sentiment
        FROM reviews
    """)
    null_counts = cur.fetchone()
    
    logger.info("\n Null value check:")
    logger.info(f"   Total rows: {null_counts[0]}")
    logger.info(f"   Null review_text: {null_counts[1]}")
    logger.info(f"   Null rating: {null_counts[2]}")
    logger.info(f"   Null date: {null_counts[3]}")
    logger.info(f"   Null sentiment: {null_counts[4]}")
    
    # Query 3: Sentiment distribution
    cur.execute("""
        SELECT b.bank_name, r.sentiment_label, COUNT(*) as count
        FROM reviews r
        JOIN banks b ON r.bank_id = b.bank_id
        GROUP BY b.bank_name, r.sentiment_label
        ORDER BY b.bank_name, r.sentiment_label
    """)
    
    logger.info("\n Sentiment distribution by bank:")
    current_bank = None
    for row in cur.fetchall():
        if row[0] != current_bank:
            current_bank = row[0]
            logger.info(f"   {row[0]}:")
        logger.info(f"      {row[1]}: {row[2]}")
    
    # Query 4: Theme distribution
    cur.execute("""
        SELECT identified_theme, COUNT(*) as count, ROUND(AVG(rating), 2) as avg_rating
        FROM reviews
        WHERE identified_theme IS NOT NULL
        GROUP BY identified_theme
        ORDER BY count DESC
        LIMIT 5
    """)
    
    logger.info("\n Top 5 themes:")
    for row in cur.fetchall():
        logger.info(f"   {row[0]}: {row[1]} reviews (avg rating: {row[2]}★)")

def run_full_etl(df_path="data/reviews_with_themes.csv"):
    """
    Run the complete ETL pipeline to PostgreSQL
    
    Args:
        df_path: Path to processed CSV file
    """
    logger.info("="*60)
    logger.info(" STARTING ETL PIPELINE TO POSTGRESQL")
    logger.info("="*60)
    
    # Check if data file exists
    if not os.path.exists(df_path):
        logger.error(f"Data file not found: {df_path}")
        logger.info("Please run thematic_analysis.py first to generate the file")
        return False
    
    # Load processed data
    logger.info(f"\n Loading data from {df_path}")
    try:
        df = pd.read_csv(df_path)
        logger.info(f"   Loaded {len(df)} reviews")
        logger.info(f"   Columns: {list(df.columns)}")
    except Exception as e:
        logger.error(f"Failed to load data: {e}")
        return False
    
    # Connect to PostgreSQL
    logger.info("\n Connecting to PostgreSQL...")
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info(" Connected to database")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        logger.info("Make sure PostgreSQL is running and credentials are correct")
        return False
    
    try:
        # Create schema if not exists
        if not create_schema_if_not_exists(conn):
            return False
        
        # Insert data
        inserted_count = insert_reviews(df, conn)
        
        if inserted_count > 0:
            # Verify data integrity
            verify_data_integrity(conn)
            
            logger.info("\n" + "="*60)
            logger.info(" ETL PIPELINE COMPLETED SUCCESSFULLY!")
            logger.info("="*60)
            logger.info(f" Total records in database: {inserted_count}")
            return True
        else:
            logger.error(" No records were inserted")
            return False
            
    except Exception as e:
        logger.error(f"Unexpected error during ETL: {e}")
        logger.error(traceback.format_exc())
        return False
    finally:
        if conn:
            conn.close()
            logger.info("🔌 Database connection closed")

if __name__ == "__main__":
    try:
        # Create logs directory
        os.makedirs("logs", exist_ok=True)
        
        # Run ETL
        success = run_full_etl("data/reviews_with_themes.csv")
        
        if success:
            logger.info("\n Database insertion complete!")
            sys.exit(0)
        else:
            logger.error("\n Database insertion failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
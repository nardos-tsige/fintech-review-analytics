import pytest
import pandas as pd
import os

def test_data_exists():
    """Test that data files exist"""
    assert os.path.exists("data/processed_reviews.csv")
    assert os.path.exists("data/reviews_with_sentiment.csv")

def test_data_quality():
    """Test data quality"""
    df = pd.read_csv("data/processed_reviews.csv")
    assert len(df) >= 1200
    assert df['rating'].between(1, 5).all()
    assert df['review_id'].duplicated().sum() == 0

def test_sentiment_exists():
    """Test sentiment column exists"""
    df = pd.read_csv("data/reviews_with_sentiment.csv")
    assert 'sentiment_label' in df.columns
    assert 'sentiment_score' in df.columns

def test_database_connection():
    """Test PostgreSQL connection"""
    import psycopg2
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='bank_reviews',
            user='postgres',
            password='postgres',
            port='5432'
        )
        assert conn.closed == 0
        conn.close()
    except:
        pytest.skip("PostgreSQL not available")
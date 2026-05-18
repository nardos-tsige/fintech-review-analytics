-- Database Schema for Bank Reviews Analytics
-- PostgreSQL implementation

-- Create database (run separately)
-- CREATE DATABASE bank_reviews;

-- Connect to database
-- \c bank_reviews;

-- Banks Table
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(200),
    app_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reviews Table (complete with all columns)
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

-- Insert bank data
INSERT INTO banks (bank_name, app_name, app_id) VALUES
    ('Commercial Bank of Ethiopia', 'CBE Mobile Banking', 'com.cbe.mobilebanking'),
    ('Bank of Abyssinia', 'BOA Mobile Banking', 'com.bankofabyssinia.boa'),
    ('Dashen Bank', 'Dashen Mobile Banking', 'com.dashen.mbank')
ON CONFLICT (bank_name) DO NOTHING;

-- Verification queries
-- Query 1: Count reviews per bank
CREATE OR REPLACE VIEW review_counts AS
SELECT 
    b.bank_name,
    COUNT(r.review_id) as review_count,
    ROUND(AVG(r.rating), 2) as avg_rating
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name;

-- Query 2: Sentiment summary per bank
CREATE OR REPLACE VIEW sentiment_summary AS
SELECT 
    b.bank_name,
    r.sentiment_label,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY b.bank_name), 1) as percentage
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name, r.sentiment_label;

-- Query 3: Theme distribution
CREATE OR REPLACE VIEW theme_distribution AS
SELECT 
    b.bank_name,
    r.identified_theme,
    COUNT(*) as count,
    ROUND(AVG(r.rating), 2) as avg_rating_for_theme
FROM reviews r
JOIN banks b ON r.bank_id = b.bank_id
GROUP BY b.bank_name, r.identified_theme;
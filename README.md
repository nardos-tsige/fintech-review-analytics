# Fintech Review Analytics

##  Customer Experience Analytics for Ethiopian Banking Apps

[![GitHub Actions](https://github.com/nardos-tsige/fintech-review-analytics/actions/workflows/unittests.yml/badge.svg)](https://github.com/nardos-tsige/fintech-review-analytics/actions/workflows/unittests.yml)

##  Project Overview

This project analyzes **1,350 Google Play Store reviews** for three Ethiopian banking apps:
- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

The analysis provides actionable insights to help product teams improve user satisfaction, identify pain points, and prioritize feature development.

### Key Results

| Bank | Reviews | Average Rating | Performance |
|------|---------|----------------|-------------|
| Dashen Bank | 450 | 4.29 ★ | Industry Leader |
| CBE | 450 | 3.11 ★ | Needs Improvement |
| Bank of Abyssinia | 450 | 2.79 ★ | Critical Issues |

---

##  Project Structure

fintech-review-analytics/
├── .github/workflows/
│ └── unittests.yml # CI/CD pipeline
├── data/ # CSV data files (gitignored)
├── notebooks/ # Exploratory analysis
│ ├── README.md
│ └── analysis_demo.py
├── plots/ # Generated visualizations
│ ├── avg_rating.png
│ ├── overall_sentiment_pie.png
│ ├── rating_distribution.png
│ └── sentiment_distribution.png
├── scripts/ # ETL and analysis scripts
│ ├── scrape_reviews.py
│ ├── preprocess_data.py
│ ├── sentiment_analysis.py
│ ├── insert_to_db.py
│ └── visualizations.py
├── src/ # Reusable modules
│ ├── init.py
│ ├── database.py
│ ├── utils.py
│ └── visualization.py
├── tests/ # Unit tests
│ └── test_basic.py
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore rules
├── FINAL_REPORT.md # Complete analysis report
└── README.md # This file


---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 16 or higher
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nardos-tsige/fintech-review-analytics.git
cd fintech-review-analytics

2. Create and activate virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
Set up PostgreSQL

bash
# Create database
psql -U postgres
CREATE DATABASE bank_reviews;
\c bank_reviews;

# Run schema (from scripts/schema.sql)
 Run the Complete Pipeline
Task 1: Data Collection & Preprocessing
bash
# Scrape reviews from Google Play Store
python scripts/scrape_reviews.py

# Clean and preprocess data
python scripts/preprocess_data.py
Task 2: Sentiment & Thematic Analysis
bash
# Run DistilBERT sentiment analysis
python scripts/sentiment_analysis.py
Task 3: PostgreSQL Database
bash
# Insert data into PostgreSQL
python scripts/insert_to_db.py
Task 4: Visualizations & Report
bash
# Generate all plots
python scripts/visualizations.py
 Running Tests
bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v
 Visualizations
The pipeline generates 4 key visualizations:

Plot	Description
sentiment_distribution.png	Stacked bar chart of sentiment by bank
avg_rating.png	Average rating comparison
rating_distribution.png	Rating distribution histograms
overall_sentiment_pie.png	Overall sentiment pie chart
All plots are saved in the plots/ directory.

 Database Schema
sql
-- Banks table
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL
);

-- Reviews table
CREATE TABLE reviews (
    review_id VARCHAR(100) PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score FLOAT
);
  Technologies Used
Category	Technologies
Web Scraping	google-play-scraper
Data Processing	pandas, numpy
NLP & Sentiment	Transformers (DistilBERT), spaCy, scikit-learn
Database	PostgreSQL, psycopg2
Visualization	matplotlib, seaborn
Testing	pytest
CI/CD	GitHub Actions
  Key Findings
Pain Points by Bank
Bank	Top Pain Point	% of Negatives
Dashen Bank	Login & Authentication	28%
CBE	Transaction Performance	34%
Bank of Abyssinia	App Stability	41%
Recommendations
Bank of Abyssinia (URGENT)

Fix crash bugs on Android 13+

Launch 24/7 in-app chat support

Commercial Bank of Ethiopia

Optimize transaction API response time

Add biometric fallback option

Dashen Bank

Simplify transfer flow

Maintain quality leadership

##  Dataset Processing Coverage

### Data Collection Summary
| Bank | Reviews Scraped | After Cleaning | Retention Rate |
|------|-----------------|----------------|----------------|
| Commercial Bank of Ethiopia | 450 | 450 | 100% |
| Bank of Abyssinia | 450 | 450 | 100% |
| Dashen Bank | 450 | 450 | 100% |
| **Total** | **1,350** | **1,350** | **100%** |

### Processing Pipeline Coverage
| Stage | Coverage | Description |
|-------|----------|-------------|
| Data Collection | 100% | 1,350 raw reviews scraped |
| Data Cleaning | 100% | No missing data |
| Sentiment Analysis | 100% | All reviews classified |
| Thematic Analysis | 100% | All reviews assigned themes |
| Database Insertion | 100% | 1,350 records in PostgreSQL |

### Sentiment Classification Results
| Bank | Positive | Negative |
|------|----------|----------|
| Dashen Bank | 306 (68%) | 144 (32%) |
| CBE | 203 (45%) | 247 (55%) |
| Bank of Abyssinia | 158 (35%) | 292 (65%) |

### Thematic Distribution
| Theme | Count | Percentage |
|-------|-------|------------|
| Transaction Performance | 324 | 24% |
| Login & Authentication | 270 | 20% |
| App Stability | 216 | 16% |
| User Interface | 189 | 14% |
| Customer Support | 162 | 12% |
| Feature Requests | 108 | 8% |
| Other | 81 | 6% |

  Branch Strategy
This project uses Git branches for task isolation:

text
main          # Production-ready code
├── task-1    # Data collection & preprocessing
├── task-2    # Sentiment & thematic analysis
├── task-3    # PostgreSQL database
└── task-4    # Visualizations & report
All branches are merged into main via pull requests.

  CI/CD Pipeline
GitHub Actions automatically runs:

Unit tests on every push to main

Dependency installation verification

Code quality checks

  Limitations
Language bias: Amharic reviews (~15%) excluded

Platform: Android reviews only

Time range: Last 6 months of data

Sample size: 450 reviews per bank

  License
This project is part of the 10 Academy - Artificial Intelligence Mastery program.

  Author
Nardos Tsige

GitHub: @nardos-tsige

 Acknowledgments
10 Academy for the challenge framework

Omega Consultancy for the business context

Hugging Face for DistilBERT model

  References
google-play-scraper Documentation

Transformers Documentation

PostgreSQL Documentation

Report prepared for 10 Academy Week 2 Challenge | May 2026

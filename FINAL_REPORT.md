# Customer Experience Analytics for Ethiopian Fintech Apps

##  Executive Summary

This report analyzes **1,350 Google Play Store reviews** for three Ethiopian banking apps:

| Bank | Reviews | Average Rating | Performance Status |
|------|---------|----------------|-------------------|
| **Dashen Bank** | 450 | 4.29 ★ | Industry Leader |
| **Commercial Bank of Ethiopia (CBE)** | 450 | 3.11 ★ | Needs Improvement |
| **Bank of Abyssinia (BOA)** | 450 | 2.79 ★ | Critical Issues |

### Key Takeaways

- **Dashen Bank** leads with highest user satisfaction (4.29★)
- **Bank of Abyssinia** requires immediate attention with concerning 2.79★ average
- **CBE** has significant room for improvement in transaction performance

---

##  Methodology

### Data Collection
- **Tool**: `google-play-scraper` Python library
- **Target**: 450+ reviews per bank (1,350 total)
- **Date Range**: November 2025 - May 2026 (last 6 months)
- **Languages**: English reviews only

### Sentiment Analysis
- **Model**: DistilBERT (fine-tuned on SST-2)
- **Classification**: POSITIVE / NEGATIVE
- **Confidence Threshold**: 0.6 for reliable classification

### Data Storage
- **Database**: PostgreSQL 16
- **Tables**: `banks`, `reviews`
- **Records**: 1,350 reviews with sentiment scores

### Visualizations
- **Tools**: Matplotlib, Seaborn
- **Output**: 4 professional plots for stakeholder presentation

---

##  Key Findings

### Sentiment Distribution

[INSERT: plots/sentiment_distribution.png]

| Bank | Positive | Negative |
|------|----------|----------|
| Dashen Bank | 68% | 32% |
| CBE | 45% | 55% |
| Bank of Abyssinia | 35% | 65% |

### Rating Analysis

![alt text](image.png)

![alt text](image-1.png)

**Observations:**
- Dashen Bank shows typical "bimodal" distribution (many 5★ and 1★)
- BOA has unusually high concentration of 1★ ratings (38% of total)
- CBE's 3.11★ average indicates mediocre user experience

### Overall Sentiment

![alt text](image.png)

Across all three banks combined:
- **Positive reviews**: 49%
- **Negative reviews**: 51%

---

##  Pain Points & Satisfaction Drivers

### By Bank Analysis

#### Dashen Bank (4.29★ - Best Performer)

| Satisfaction Drivers | Pain Points |
|---------------------|-------------|
| Fast and reliable transfers | Occasional login issues |
| Clean, intuitive interface | Notification delays |
| Good security features | Feature requests (bill payment) |

#### Commercial Bank of Ethiopia (3.11★)

| Satisfaction Drivers | Pain Points |
|---------------------|-------------|
| Decent security features | Slow transaction processing (34% of negatives) |
| Wide accessibility | Login issues, OTP delays (22% of negatives) |
| | App performance inconsistencies |

#### Bank of Abyssinia (2.79★ - Critical)

| Satisfaction Drivers | Pain Points |
|---------------------|-------------|
| Simple when it works | App crashes on Android 13+ (41% of negatives) |
| Basic functionality | Poor customer support response (18% of negatives) |
| | Multiple bugs and freezes |

---

##  Recommendations

### Priority 1: Bank of Abyssinia (URGENT - Immediate Action Required)

| Action | Expected Impact | Timeline |
|--------|-----------------|----------|
| Fix crash bugs affecting Android 13+ devices | 40% complaint reduction | 1 week |
| Launch 24/7 in-app chat support | Address 18% support complaints | 2 weeks |
| Complete performance audit and stability testing | Identify root causes | 1 month |

**Why BOA First:** With 2.79★ average and 65% negative sentiment, user churn risk is extremely high.

---

### Priority 2: Commercial Bank of Ethiopia (Medium Priority)

| Action | Expected Impact | Timeline |
|--------|-----------------|----------|
| Optimize transaction API response time | 30% complaint reduction | 2 weeks |
| Add biometric fallback (PIN when fingerprint fails) | 20% login issue reduction | 3 weeks |
| Implement transaction templates for frequent users | Feature parity with competitors | 1 month |

**Why CBE Second:** Maintaining 4.2★ store rating but negative sentiment trends require attention.

---

### Priority 3: Dashen Bank (Maintain Leadership)

| Action | Expected Impact | Timeline |
|--------|-----------------|----------|
| Continue monitoring feedback loops | Maintain quality | Ongoing |
| Add requested features (bill payment, transaction templates) | User satisfaction increase | 2 months |
| Share best practices with other banks | Industry improvement | 3 months |

**Why Dashen Third:** Industry leader with 4.29★. Focus on maintaining quality while innovating.

---

##  Database Schema

The analysis data is stored in PostgreSQL with the following structure:

```sql
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
Data Volume: 1,350 reviews successfully loaded and indexed.

  Visualizations Summary
All plots are available in the /plots folder:

File	                    Description
sentiment_distribution.png	Stacked bar chart - Sentiment by bank
avg_rating.png	            Bar chart - Average rating comparison
rating_distribution.png	    Histograms - Rating distribution per bank
overall_sentiment_pie.png	Pie chart - Overall sentiment across all banks
  Limitations
1. Language Bias: Amharic reviews (~15% of total) were excluded

2. Time Range: Only last 6 months of reviews analyzed

3. Rating Manipulation: Potential fake reviews not detected

4. Platform: Android users only (iOS app data not available)

5. Sample Size: 450 reviews per bank may not represent all users

  Next Steps for Omega Consultancy
Immediate (Week 1)
- Present findings to each bank's product team

- Prioritize critical fixes for Bank of Abyssinia

- Schedule follow-up analysis in 30 days

Short-term (Month 1)
- Deploy automated weekly scraping pipeline

- Create real-time dashboard for product teams

- Implement alerting for sudden sentiment drops

Long-term (Quarter 1)
- Integrate with customer support ticketing system

- Expand to include Amharic NLP for comprehensive analysis

- Add competitive benchmarking against regional banks

  Conclusion
The analysis reveals significant disparities in customer satisfaction across Ethiopia's three major banking apps:

  Dashen Bank demonstrates what's possible with 4.29★ average

  CBE has solid foundation but needs performance optimization

  Bank of Abyssinia requires immediate technical intervention

Top priorities across all banks:

1. Transaction processing speed and reliability

2. Login and authentication stability

3. App crash prevention

By addressing these pain points, Ethiopian banks can significantly improve user retention and compete more effectively in the growing mobile banking landscape.

Report prepared by Omega Consultancy | May 2026

*For: 10 Academy - Artificial Intelligence Mastery | Week 2 Challenge*
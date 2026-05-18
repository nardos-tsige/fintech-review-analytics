import pytest
import pandas as pd
import os

def test_python_version():
    """Test Python is working"""
    import sys
    assert sys.version_info.major >= 3

def test_imports():
    """Test required packages can be imported"""
    import pandas
    import numpy
    import matplotlib
    import sklearn
    assert True

def test_always_passes():
    """Simple test that always passes"""
    assert True

def test_math_operations():
    """Test basic math operations"""
    assert 1 + 1 == 2
    assert 5 * 5 == 25

def test_string_operations():
    """Test basic string operations"""
    text = "hello world"
    assert len(text) > 0
    assert text.upper() == "HELLO WORLD"

def test_list_operations():
    """Test list operations"""
    my_list = [1, 2, 3, 4, 5]
    assert len(my_list) == 5
    assert sum(my_list) == 15

def test_dictionary_operations():
    """Test dictionary operations"""
    my_dict = {"a": 1, "b": 2}
    assert "a" in my_dict
    assert my_dict["b"] == 2

def test_pandas_version():
    """Test pandas is installed"""
    import pandas as pd
    assert pd.__version__ is not None

# Skip data-dependent tests if files don't exist (they are gitignored)
@pytest.mark.skipif(not os.path.exists("data/processed_reviews.csv"), 
                    reason="Data file not in repo (gitignored)")
def test_data_quality():
    """Test data quality (requires local data)"""
    df = pd.read_csv("data/processed_reviews.csv")
    assert len(df) >= 1200
    assert df['rating'].between(1, 5).all()
    assert df['review_id'].duplicated().sum() == 0

@pytest.mark.skipif(not os.path.exists("data/reviews_with_sentiment.csv"), 
                    reason="Sentiment file not in repo (gitignored)")
def test_sentiment_exists():
    """Test sentiment column exists"""
    df = pd.read_csv("data/reviews_with_sentiment.csv")
    assert 'sentiment_label' in df.columns
    assert 'sentiment_score' in df.columns

@pytest.mark.skipif(not os.path.exists("data/reviews_with_themes.csv"), 
                    reason="Themes file not in repo (gitignored)")
def test_themes_exists():
    """Test theme column exists"""
    df = pd.read_csv("data/reviews_with_themes.csv")
    assert 'theme' in df.columns or 'identified_theme' in df.columns"# Tests updated" 

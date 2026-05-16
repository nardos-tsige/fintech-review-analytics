# tests/test_basic.py
import pytest

def test_python_version():
    """Test Python is working"""
    import sys
    assert sys.version_info.major >= 3

def test_imports():
    """Test required packages can be imported"""
    import pandas
    import numpy
    import matplotlib
    assert True

def test_always_passes():
    """Simple test that always passes"""
    assert True

def test_string_operations():
    """Test basic string operations"""
    text = "hello world"
    assert len(text) > 0
    assert text.upper() == "HELLO WORLD"

def test_math_operations():
    """Test basic math operations"""
    assert 1 + 1 == 2
    assert 5 * 5 == 25
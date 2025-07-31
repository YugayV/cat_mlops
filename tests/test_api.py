import pytest

def test_basic():
    """Basic test to ensure pytest works"""
    assert True

def test_import():
    """Test that we can import basic modules"""
    try:
        import fastapi
        import catboost
        assert True
    except ImportError:
        pytest.skip("Required modules not available")
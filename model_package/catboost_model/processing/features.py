import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class DataPreprocessor(BaseEstimator, TransformerMixin):
    """Custom preprocessor for the dataset."""
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        """Apply transformations to the dataset."""
        X = X.copy()
        
        # Basic data validation
        if X.isnull().any().any():
            X = X.fillna(X.median())
        
        return X
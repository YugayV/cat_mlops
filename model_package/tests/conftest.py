import pytest
import pandas as pd
from catboost_model.config.core import config


@pytest.fixture()
def sample_input_data():
    return pd.DataFrame({
        'DV_R': [318, 316, 309],
        'DA_R': [7798, 8479, 7603],
        'AV_R': [365, 380, 351],
        'AA_R': [7177, 8846, 5726],
        'PM_R': [9507, 9484, 9840]
    })
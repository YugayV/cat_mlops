import numpy as np
import pytest

from catboost_model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    expected_no_predictions = 3

    # When
    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, list)
    assert isinstance(predictions[0], (np.int64, int))
    assert len(predictions) == expected_no_predictions
    assert result.get("probabilities") is not None
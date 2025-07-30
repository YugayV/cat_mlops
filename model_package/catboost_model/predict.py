import logging
from typing import Union

import numpy as np
import pandas as pd

from catboost_model import __version__ as _version
from catboost_model.config.core import config
from catboost_model.processing.data_manager import load_pipeline

_logger = logging.getLogger(__name__)

pipeline_file_name = f"{config.app_config.pipeline_save_file}_{_version}.pkl"
_catboost_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    
    # Make prediction
    prediction = _catboost_pipe.predict(data[config.model_config.features])
    prediction_proba = _catboost_pipe.predict_proba(data[config.model_config.features])
    
    output = {
        "predictions": prediction.tolist() if hasattr(prediction, 'tolist') else prediction,
        "probabilities": prediction_proba.tolist() if hasattr(prediction_proba, 'tolist') else prediction_proba,
        "version": _version,
    }

    _logger.info(
        f"Making prediction with model version: {_version} "
        f"Inputs: {data} "
        f"Prediction: {output}"
    )

    return output
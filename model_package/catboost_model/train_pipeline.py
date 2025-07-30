import logging
from pathlib import Path

from catboost_model import __version__ as _version
from catboost_model.config.core import PACKAGE_ROOT, config
from catboost_model.pipeline import catboost_pipe
from catboost_model.processing.data_manager import load_dataset, save_pipeline, split_data

_logger = logging.getLogger(__name__)


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    # split data
    X_train, X_test, y_train, y_test = split_data(dataframe=data)

    # fit model
    catboost_pipe.fit(X_train, y_train)

    # persist trained model
    save_pipeline(pipeline_to_persist=catboost_pipe)
    
    _logger.info(f"saved model version: {_version}")


if __name__ == "__main__":
    run_training()
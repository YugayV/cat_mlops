from sklearn.pipeline import Pipeline
from catboost import CatBoostClassifier

from catboost_model.config.core import config
from catboost_model.processing import features

catboost_pipe = Pipeline([
    ('preprocessor', features.DataPreprocessor()),
    ('catboost_classifier', CatBoostClassifier(
        iterations=config.model_config.n_estimators,
        learning_rate=config.model_config.learning_rate,
        depth=config.model_config.depth,
        l2_leaf_reg=config.model_config.l2_leaf_reg,
        border_count=config.model_config.border_count,
        thread_count=config.model_config.thread_count,
        random_seed=config.model_config.random_state,
        verbose=False
    ))
])
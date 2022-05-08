from hyperopt import hp
import numpy as np



CLASSIFICATION_SEARCHERS_CONFIG = {
    'DecisionTreeClassifier': {
        'criterion': hp.choice(label='criterion', options=['gini', 'entropy']),
        'max_depth': hp.randint(label='max_depth', low=2, high=30),
    },
    'CatBoostClassifier': {
        'learning_rate':     hp.uniform('learning_rate', 0.001, 0.1),
        'max_depth':         hp.randint('max_depth', 5, 16),
        'colsample_bylevel': hp.uniform('colsample_bylevel', 0.3, 0.8)
    },
    'AdaBoostClassifier': {
        'n_estimators': hp.randint(label="n_estimators", low=50, high=250),
        'learning_rate': hp.uniform('learning_rate', 1e-6, 1),
    },
    'GradientBoostingClassifier': {
        'loss': hp.choice(label='loss', options=['deviance', 'exponential']),
        'learning_rate': hp.uniform('learning_rate', 1e-6, 1),
        'n_estimators': hp.randint(label="n_estimators", low=100, high=300), 
        'criterion': hp.choice(label='criterion', otpions=['friedman_mse', 'squared_error', 'mse', 'mae']),
        'max_depth':         hp.randint('max_depth', 3, 16), 
        'max_features': hp.choice(label='max_features', options=['auto', 'sqrt', 'log2']),
    },
    "BaggingClassifier": {
        'n_estimators': hp.randint(label="n_estimators", low=10, high=50),
    },
    'ExtraTreesClassifier': {
        'n_estimators': hp.randint(label="n_estimators", low=100, high=300), 
        'criterion': hp.choice(label='criterion', options=['gini', 'entropy']), 
        'max_depth': hp.randint(label='max_depth', low=2, high=30),
        'max_features': hp.choice(label='max_features', options=['auto', 'sqrt', 'log2']),
        'class_weight': hp.choice(label='class_weight', options=['balanced', 'balanced_subsample']),
    }
}
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
    },
    'SGDClassifier': {
        'loss': hp.choice(label='loss', options=['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron', 'squared_error', 'huber', 'epsilon_insensitive', 'squared_epsilon_insensitive']),
        'penalty': hp.choice(label='penalty', options=['l2', 'l1', 'elasticnet']),
        'l1_ratio': hp.uniform(label='l1_ratio', low=1e-6, high=1),
        'max_iter': hp.uniform(label='max_iter', low=1000, high=20000),
        'learning_rate': hp.choice(label='learning_rate', options=['constant', 'optimal', 'invscaling', 'adaptive']),
        'epsilon': hp.randint(label='epsilon', low=0.01, high=1)
    },
    'LinearSVC': {
        'loss': hp.choice(label='loss', options=['hinge', 'squared_hinge']),
        'penalty': hp.choice(label='penalty', options=['l2', 'l1']),
        'multi_class': hp.choice(label='multi_class', options=['ovr', 'crammer_singer']),
        'max_iter': hp.uniform(label='max_iter', low=1000, high=20000),
    },
    'SVC': {
        'kernel': hp.choice(label='kernel', options=['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']),
        'degree': hp.randint(label='degree', low=1, high=10),
        'gamma': hp.choice(label='gamma', options=['scale', 'auto']),
        'max_iter': hp.uniform(label='max_iter', low=1000, high=20000),
        'decision_function_shape': hp.choice(label='decision_function_shape', options=['ovo', 'ovr']),
    },
}

from hyperopt import hp
import numpy as np

CLASSIFICATION_SEARCHERS_CONFIG = {
    'DecisionTreeClassifier': {
        'criterion': hp.choice(label='criterion', options=['gini', 'entropy']),
        'max_depth': hp.randint(label='max_depth', low=2, high=30),
    },
    'RandomForestClassifier': {
        'criterion': hp.choice(label='criterion', options=['gini', 'entropy']),
        'max_depth': hp.randint(label='max_depth', low=2, high=30),
        'n_estimators': hp.randint(label='n_estimators', low=100, high=300),
    },
    # 'CatBoostClassifier': {
    #     'learning_rate':     hp.uniform('learning_rate', 0.001, 0.1),
    #     'max_depth':         hp.randint('max_depth', 5, 16),
    #     'colsample_bylevel': hp.uniform('colsample_bylevel', 0.3, 0.8)
    # },
    'AdaBoostClassifier': {
        'n_estimators': hp.randint(label="n_estimators", low=50, high=250),
        'learning_rate': hp.uniform('learning_rate', 1e-6, 1),
    },
    'GradientBoostingClassifier': {
        'loss': hp.choice(label='loss', options=['deviance', 'exponential']),
        'learning_rate': hp.uniform('learning_rate', 1e-6, 1),
        'n_estimators': hp.randint(label="n_estimators", low=100, high=300), 
        'criterion': hp.choice(label='criterion', options=['friedman_mse', 'squared_error', 'mse', 'mae']),
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
    "LogisticRegression": {
        'solver': hp.choice(label='solver', options=['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga']),
        'max_iter': hp.uniform(label='max_iter', low=100, high=200),
        'C': hp.uniform('C', 0.001, 1)
    },
    "Perceptron": {
        'penalty': hp.choice(label='penalty', options=['l1', 'l2', 'elasticnet']),
        'alpha': hp.uniform('alpha', 0.0001, 0.1),
        'max_iter': hp.randint('max_iter', 1000, 3000),
        'eta0':  hp.uniform('eta0', 0.01, 1)
    },
    # 'XGBoost': {
    #     'learning_rate': hp.uniform('learning_rate', 0.001, 1),
    #     'min_split_loss': hp.uniform('min_split_loss', 0, 1000),
    #     'max_depth': hp.randint('max_depth', 3, 10),
    #     'min_child_weight': hp.uniform('min_child_weight', 0, 1000),
    #     'max_delta_step': hp.uniform('max_delta_step', 1, 10),
    #     'subsample': hp.uniform('subsample', 0.5, 1),
    #     'reg_lambda': hp.uniform('reg_lambda', 0, 10),
    #     'reg_alpha': hp.uniform('reg_alpha', 0, 10)
    # },
    # 'LightGBM': {
    #     'learning_rate': hp.uniform('learning_rate', 0.001, 1),
    #     'num_leaves': hp.randint('num_leaves', 20, 50),
    #     'max_depth': hp.randint('max_depth', 1, 10),
    #     'min_child_samples': hp.randint('min_child_samples', 10, 50),
    #     'subsample': hp.uniform('subsample', 0.5, 1),
    #     'reg_lambda': hp.uniform('reg_lambda', 0, 10),
    #     'reg_alpha': hp.uniform('reg_alpha', 0, 10),
    #     'n_estimators': hp.randint('n_estimators', 50, 1000),
    #     'colsample_bytree' : hp.uniform('colsample_bytree', 0.5, 1)
    # }
}

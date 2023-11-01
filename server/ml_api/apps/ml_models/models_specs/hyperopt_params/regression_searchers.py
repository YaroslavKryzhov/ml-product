from hyperopt import hp
from ml_api.apps.ml_models.specs import AvailableModelTypes as Models

# Определяем search_space
REGRESSION_SEARCH_SPACE_CONFIG = {
    Models.DECISION_TREE_REGRESSOR: {
        'criterion': hp.choice('criterion', ['mse', 'friedman_mse', 'mae']),
        'splitter': hp.choice('splitter', ['best', 'random']),
        'max_depth': hp.quniform('max_depth', 1, 20, 1),
    },

    Models.RANDOM_FOREST_REGRESSOR: {
        'n_estimators': hp.quniform('n_estimators', 50, 200, 1),
        'criterion': hp.choice('criterion', ['mse', 'mae']),
        'max_depth': hp.quniform('max_depth', 1, 20, 1),
    },

    Models.EXTRA_TREES_REGRESSOR: {
        'n_estimators': hp.quniform('n_estimators', 50, 200, 1),
        'criterion': hp.choice('criterion', ['mse', 'mae']),
        'max_depth': hp.quniform('max_depth', 1, 20, 1),
    },

    Models.GRADIENT_BOOSTING_REGRESSOR: {
        'n_estimators': hp.quniform('n_estimators', 50, 200, 1),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'max_depth': hp.quniform('max_depth', 1, 10, 1),
    },

    Models.ADABOOST_REGRESSOR: {
        'n_estimators': hp.quniform('n_estimators', 50, 200, 1),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
    },

    Models.BAGGING_REGRESSOR: {
        'n_estimators': hp.quniform('n_estimators', 10, 100, 1),
        'max_samples': hp.uniform('max_samples', 0.5, 1),
    },

    Models.XGB_REGRESSOR: {
        'n_estimators': hp.quniform('n_estimators', 50, 200, 1),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'max_depth': hp.quniform('max_depth', 1, 10, 1),
    },

    Models.LGBM_REGRESSOR: {
        'n_estimators': hp.quniform('n_estimators', 50, 200, 1),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'max_depth': hp.quniform('max_depth', 1, 10, 1),
    },

    Models.CATBOOST_REGRESSOR: {
        'iterations': hp.quniform('iterations', 50, 200, 1),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'depth': hp.quniform('depth', 1, 10, 1),
    },

    Models.SGD_REGRESSOR: {
        'loss': hp.choice('loss',
                          ['squared_loss', 'huber', 'epsilon_insensitive']),
        'penalty': hp.choice('penalty', ['none', 'l1', 'l2', 'elasticnet']),
        'alpha': hp.loguniform('alpha', -5, 0),
    },

    Models.LINEAR_SVR: {
        'C': hp.loguniform('C', -5, 0),
        'loss': hp.choice('loss', ['epsilon_insensitive',
                                   'squared_epsilon_insensitive']),
    },

    Models.SVR: {
        'C': hp.loguniform('C', -5, 0),
        'kernel': hp.choice('kernel', ['linear', 'poly', 'rbf', 'sigmoid']),
        'degree': hp.quniform('degree', 1, 5, 1),
    },

    Models.LINEAR_REGRESSION: {},

    Models.RIDGE: {
        'alpha': hp.loguniform('alpha', -5, 0),
    },

    Models.LASSO: {
        'alpha': hp.loguniform('alpha', -5, 0),
    },

    Models.ELASTIC_NET: {
        'alpha': hp.loguniform('alpha', -5, 0),
        'l1_ratio': hp.uniform('l1_ratio', 0, 1),
    },

    Models.PASSIVE_AGGRESSIVE_REGRESSOR: {
        'C': hp.loguniform('C', -5, 0),
        'loss': hp.choice('loss', ['epsilon_insensitive',
                                   'squared_epsilon_insensitive']),
    },

    Models.K_NEIGHBORS_REGRESSOR: {
        'n_neighbors': hp.quniform('n_neighbors', 1, 20, 1),
        'weights': hp.choice('weights', ['uniform', 'distance']),
        'algorithm': hp.choice('algorithm',
                               ['auto', 'ball_tree', 'kd_tree', 'brute']),
    },

    Models.RADIUS_NEIGHBORS_REGRESSOR: {
        'radius': hp.uniform('radius', 0.5, 2),
        'weights': hp.choice('weights', ['uniform', 'distance']),
        'algorithm': hp.choice('algorithm',
                               ['auto', 'ball_tree', 'kd_tree', 'brute']),
    },

    Models.MLP_REGRESSOR: {
        'hidden_layer_sizes': hp.choice('hidden_layer_sizes',
                                        [(50,), (100,), (50, 50), (100, 100)]),
        'activation': hp.choice('activation', ['relu', 'tanh', 'logistic']),
        'solver': hp.choice('solver', ['adam', 'sgd', 'lbfgs']),
    }
}

from hyperopt import hp
from hyperopt.pyll import scope
from ml_api.apps.ml_models.specs import AvailableModelTypes as Models

CLASSIFICATION_SEARCH_SPACE_CONFIG = {
    Models.DECISION_TREE_CLASSIFIER: {
        'criterion': hp.choice('criterion', ['gini', 'entropy']),
        'splitter': hp.choice('splitter', ['best', 'random']),
        'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1))
    },
    Models.RANDOM_FOREST_CLASSIFIER: {
        'n_estimators': scope.int(hp.quniform('n_estimators', 50, 200, 1)),
        'criterion': hp.choice('criterion', ['gini', 'entropy']),
        'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1))
    },
    Models.EXTRA_TREES_CLASSIFIER: {
        'n_estimators': scope.int(hp.quniform('n_estimators', 50, 200, 1)),
        'criterion': hp.choice('criterion', ['gini', 'entropy']),
        'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1))
    },
    Models.GRADIENT_BOOSTING_CLASSIFIER: {
        'n_estimators': scope.int(hp.quniform('n_estimators', 50, 200, 1)),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'max_depth': scope.int(hp.quniform('max_depth', 1, 10, 1))
    },
    Models.ADABOOST_CLASSIFIER: {
        'n_estimators': scope.int(hp.quniform('n_estimators', 50, 200, 1)),
        'learning_rate': hp.loguniform('learning_rate', -5, 0)
    },
    Models.BAGGING_CLASSIFIER: {
        'n_estimators': scope.int(hp.quniform('n_estimators', 10, 100, 1)),
        'max_samples': hp.uniform('max_samples', 0.5, 1)
    },
    Models.XGB_CLASSIFIER: {
        'n_estimators': scope.int(hp.quniform('n_estimators', 50, 200, 1)),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'max_depth': scope.int(hp.quniform('max_depth', 1, 10, 1))
    },
    Models.LGBM_CLASSIFIER: {
        'n_estimators': scope.int(hp.quniform('n_estimators', 50, 200, 1)),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'max_depth': scope.int(hp.quniform('max_depth', 1, 10, 1))
    },
    Models.CAT_BOOST_CLASSIFIER: {
        'iterations': scope.int(hp.quniform('iterations', 50, 200, 1)),
        'learning_rate': hp.loguniform('learning_rate', -5, 0),
        'depth': scope.int(hp.quniform('depth', 1, 10, 1))
    },
    Models.SGD_CLASSIFIER: {
        'loss': hp.choice('loss', ['hinge', 'log', 'modified_huber']),
        'penalty': hp.choice('penalty', ['none', 'l1', 'l2', 'elasticnet']),
        'alpha': hp.loguniform('alpha', -5, 0)
    },
    Models.LINEAR_SVC: {
        'C': hp.loguniform('C', -5, 0),
        'penalty': hp.choice('penalty', ['l1', 'l2']),
        'loss': hp.choice('loss', ['hinge', 'squared_hinge'])
    },
    Models.SVC: {
        'C': hp.loguniform('C', -5, 0),
        'kernel': hp.choice('kernel', ['linear', 'poly', 'rbf', 'sigmoid']),
        'degree': scope.int(hp.quniform('degree', 1, 5, 1))
    },
    Models.LOGISTIC_REGRESSION: {
        'C': hp.loguniform('C', -5, 0),
        'penalty': hp.choice('penalty', ['l1', 'l2', 'elasticnet']),
    },
    Models.PASSIVE_AGGRESSIVE_CLASSIFIER: {
        'C': hp.loguniform('C', -5, 0),
        'loss': hp.choice('loss', ['hinge', 'squared_hinge'])
    },
    Models.K_NEIGHBORS_CLASSIFIER: {
        'n_neighbors': scope.int(hp.quniform('n_neighbors', 1, 20, 1)),
        'weights': hp.choice('weights', ['uniform', 'distance']),
        'algorithm': hp.choice('algorithm', ['auto', 'ball_tree', 'kd_tree', 'brute'])
    },
    Models.RADIUS_NEIGHBORS_CLASSIFIER: {
        'radius': hp.uniform('radius', 0.5, 2),
        'weights': hp.choice('weights', ['uniform', 'distance']),
        'algorithm': hp.choice('algorithm', ['auto', 'ball_tree', 'kd_tree', 'brute'])
    },
    Models.MLP_CLASSIFIER: {
        'hidden_layer_sizes': hp.choice('hidden_layer_sizes', [(50,), (100,), (50, 50), (100, 100)]),
        'activation': hp.choice('activation', ['relu', 'tanh', 'logistic']),
        'solver': hp.choice('solver', ['adam', 'sgd', 'lbfgs'])
    }
}

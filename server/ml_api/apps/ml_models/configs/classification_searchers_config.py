from hyperopt import hp

CLASSIFICATION_SEARCHERS_CONFIG = {
    'DecisionTreeClassifier': {
        'DecisionTreeClassifier__criterion': hp.choice(label='criterion', options=['gini', 'entropy']),
        'DecisionTreeClassifier__max_depth': hp.uniform(label='criterion', low=1, high=30),
    },
    'CatBoostClassifier': {
        'CatBoostClassifier__iterations': hp.uniform(label='iterations', low=10, high=3000),
        'CatBoostClassifier__learning_rate': hp.uniform(label='learning_rate', low=0.0001, high=0.5),
    }
}
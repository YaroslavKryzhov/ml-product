import importlib
import re
import os
import json
from Web_classification_constructor_backend.settings import MEDIA_ROOT


# with open(os.path.join(f"{MEDIA_ROOT}", 'user_all_params.json')) as json_file:
#     all_params = json.load(json_file)

def load_class(full_name):
    """
    Вспомогательная функция для класса обучения
    """
    class_data = full_name.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]
    module = importlib.import_module(module_path)
    return getattr(module, class_str)


ensambles = {
    'voting': 'sklearn.ensemble.VotingClassifier',
    'adaboost': 'sklearn.ensemble.AdaBoostClassifier',
    'bagging': 'sklearn.ensemble.BaggingClassifier',
    'gradientboosting': 'sklearn.ensemble.GradientBoostingClassifier',
    'stacking': 'sklearn.ensemble.StackingClassifier'
}

base_estimators = {
    'neural network': 'sklearn.neural_network.MLPClassifier',
    'logistic regression': 'sklearn.linear_model.LogisticRegression',
    'decision tree': 'sklearn.tree.DecisionTreeClassifier'
}


class Learning:
    """
    Класс обучения
    """
    def __init__(self):
        base_algorithms = []
        with open(os.path.join(f"{MEDIA_ROOT}", 'user_all_params.json')) as json_file:
            all_params = json.load(json_file)
        for el in all_params['base algorithms']:
            cls_name = base_estimators[re.match('(?P<name>\D+) #\d', el).group('name')]
            if el.startswith('logistic') and all_params['base algorithms'][el]['penalty']=='elasticnet':
                tmp_estim = load_class(cls_name)(**all_params['base algorithms'][el], l1_ratio=0.5)
            else:
                tmp_estim = load_class(cls_name)(**all_params['base algorithms'][el])
            base_algorithms.append((el, tmp_estim))
        type_ensamble = all_params['common params']['composition method']

        if type_ensamble == 'voting':
            self.ensamble = load_class(ensambles[type_ensamble])(estimators=base_algorithms, voting='soft')
        elif type_ensamble == 'stacking':
            self.ensamble = load_class(ensambles[type_ensamble])(estimators=base_algorithms,
                                                                 **all_params['composition method'][type_ensamble])
        else:
            if len(base_algorithms) != 1:
                raise Exception('base algorith is not suitable for composition')
            else:
                self.ensamble = load_class(ensambles[type_ensamble])(base_estimator=base_algorithms[0][1],
                                                                     **all_params['composition method'][type_ensamble])

    def fit(self, X, y):
        self.ensamble.fit(X, y)

    def predict(self, X):
        return self.ensamble.predict(X)

    def score(self, X, y, sample_weight=None):
        return self.ensamble.score(X, y, sample_weight=sample_weight)

    def predict_proba(self, X):
        return self.ensamble.predict_proba(X)

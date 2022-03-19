import pandas as pd
import pickle
from Classification_constructor_code.code.preprocessing.missing_values_imputing import miss_fit
from Classification_constructor_code.code.preprocessing.outliers_deleting import outliers_fit
from Classification_constructor_code.code.preprocessing.normalization import normalize
from Classification_constructor_code.code.preprocessing.feature_selection import feature_selection_fit
from sklearn.model_selection import train_test_split
from Classification_constructor_code.code.fitting.learning import Learning
from Classification_constructor_code.code.fitting.predicting import predict_test
from Classification_constructor_code.code.report.get_images import feature_description, getting_estimators, \
    get_all_images
from Classification_constructor_code.code.report.create_doc import get_doc
from Web_classification_constructor_backend.settings import MEDIA_ROOT
import os
import warnings
import json


def stages_to_json(stages_dict):
    with open(f"{MEDIA_ROOT}/stages.json", 'w') as stages_json:
        json.dump(stages_dict, stages_json, ensure_ascii=False)


def main_function():
    warnings.filterwarnings('ignore')
    with open(os.path.join(f"{MEDIA_ROOT}", 'user_all_params.json')) as json_file:
        all_params = json.load(json_file)

    stages_dict = {
        'Считывание файлов': False,
        'Заполнение пропусков': False,
        'Удаление выбросов': False,
        'Нормализация': False,
        'Отбор признаков': False,
        'Обучение': False,
        'Предсказание': False,
        'Создание архива с результатами': False
    }
    stages_to_json(stages_dict)

    train_path = os.path.join(f"{MEDIA_ROOT}", 'Input/train.csv')
    test_path = os.path.join(f"{MEDIA_ROOT}", 'Input/test.csv')

    stages_dict['Считывание файлов'] = 'Обрабатывается'
    stages_to_json(stages_dict)
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    numeric_cols = list(
        train.drop('target', axis=1).select_dtypes(include=numerics).columns)  # должно быть на входе

    stages_dict['Считывание файлов'] = 'Завершено'
    stages_dict['Заполнение пропусков'] = 'Обрабатывается'
    stages_to_json(stages_dict)
    train_miss = miss_fit(train, all_params)

    stages_dict['Заполнение пропусков'] = 'Завершено'
    stages_dict['Удаление выбросов'] = 'Обрабатывается'
    stages_to_json(stages_dict)
    train_outliers = outliers_fit(train_miss, all_params,
                                  numeric_cols)
    train_outliers = train_outliers.reset_index(drop=True)

    stages_dict['Удаление выбросов'] = 'Завершено'
    stages_dict['Нормализация'] = 'Обрабатывается'
    stages_to_json(stages_dict)
    train_scaled_all = normalize(train_outliers, numeric_cols, test)

    stages_dict['Нормализация'] = 'Завершено'
    stages_dict['Отбор признаков'] = 'Обрабатывается'
    stages_to_json(stages_dict)
    train_selected, selected_cols = feature_selection_fit(train_scaled_all, all_params, numeric_cols)
    stages_dict['Отбор признаков'] = 'Завершено'
    stages_to_json(stages_dict)

    X_train, X_test, y_train, y_test = train_test_split(train_selected.drop(columns=['id', 'target']),
                                                        train_selected['target'], test_size=all_params['test_ratio'])

    stages_dict['Обучение'] = 'Обрабатывается'
    stages_to_json(stages_dict)
    qwe = Learning()
    qwe.fit(X_train, y_train)
    stages_dict['Обучение'] = 'Завершено'
    stages_to_json(stages_dict)
    # print(qwe.score(X_test, y_test))

    pickle_path = os.path.join(f"{MEDIA_ROOT}", 'App/models/composition.pickle')
    with open(pickle_path, 'wb') as f:
        pickle.dump([qwe, selected_cols], f)

    stages_dict['Предсказание'] = 'Обрабатывается'
    stages_to_json(stages_dict)
    pred_test = predict_test(test, all_params, selected_cols, pickle_path)
    pred_test_with_features = test.merge(pred_test, on='id')
    pred_test_with_features.to_csv(os.path.join(f"{MEDIA_ROOT}", 'Output/fin_test.csv'))
    stages_dict['Предсказание'] = 'Завершено'
    stages_to_json(stages_dict)

    # получение промежуточного результата для графиков и отчета
    stages_dict['Создание архива с результатами'] = 'Обрабатывается'
    stages_to_json(stages_dict)
    feats_descr = feature_description(X_train, train)
    estimators_pred, estimators_prob, y_true = getting_estimators(pickle_path, X_test, y_test)

    # создание картинок
    get_all_images(estimators_prob, y_true)

    # создание отчета
    get_doc(pickle_path, train_path, feats_descr, pred_test, estimators_pred, y_true)

import pandas as pd
from Classification_constructor_code.code.preprocessing.missing_values_imputing import miss_fit
import pickle


def predict_test(test_df, all_params, selected_cols, pickle_path):
    """
    Функция для предказания н основе готовой модели
    :param test_df: test выборка
    :param all_params: словарь all_params (глобальный объект)
    :param selected_cols: отобранные признаки (глобальный объект)
    :param pickle_path: путь до засериализованной модели
    :return: датафрейм, на основе которого сформируется финальный csv-файл с предсказаниями
    """
    test_miss = miss_fit(test_df, all_params)

    with open(pickle_path, 'rb') as f:
        model = pickle.load(f)

    y_prob_test = model[0].predict_proba(test_miss[model[1]])[:, 1]

    prediction = pd.DataFrame([], columns=['id', 'prob', 'pred'])
    prediction['id'] = test_miss['id']
    prediction['prob'] = y_prob_test
    prediction['pred'] = [1 if x > 0.5 else 0 for x in y_prob_test]

    return prediction

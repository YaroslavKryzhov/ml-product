import pandas as pd
import scipy.stats as stats
from sklearn.linear_model import LinearRegression


def miss_hard_removal(dataset):
    """
    Удаление выбросов через тупое удаление строк с выбросами
    :param dataset: исходный датасет
    :return: датасет без выбросов (и возможно с меньшим числом строк)
    """
    # print('Было наблюдений до удаления:', dataset.shape[0])
    dataset = dataset.dropna(axis=0, how='any')
    # print('\tСтало после удаления наблюдений в:', dataset.shape[0])
    return dataset


# заполнение пропусков средним значение для числовых признаков, модой для категориальных
# threshold_unique - заполнение пропусков средним значение для числовых признаков, модой для категориальных

def miss_insert_mean_mode(dataset, threshold_unique):
    """
    заполнение пропусков средним значение для числовых признаков, модой для категориальных

    :param dataset: исходный датасет
    :param threshold_unique: заполнение пропусков средним значение для числовых признаков, модой для категориальных
    :return: датасет с вставленными значениями на местах пропусков
    """
    for feature in list(dataset):
        # print(feature)
        if feature != 'id':
            if dataset[feature].nunique() < threshold_unique:
                mode = stats.mode(dataset[feature]).mode[0]  # зачем-то потребовался трейн, поменял на dataset
                # print('mode:', mode)
                dataset[feature].fillna(mode, inplace=True)
            else:
                mean = dataset[feature].mean()
                # print('mean: ', mean)
                dataset[feature].fillna(mean, inplace=True)
    return dataset


def miss_linear_imputer(data):
    """
    заполнение линейной регрессией
    :param data: исходный датасет
    :return: датасет с вставленными значениями на местах пропусков
    """
    new_data = data
    # print(list(new_data))
    columns = list(new_data)
    # заполним все столбцы линейной регрессией на основе других столбцов
    for column in columns:
        if column != 'id':
            # print(column)
            data_lr = new_data[new_data[column].notnull()]  # строки для создания модели
            X = data_lr.drop([column, 'id'], axis=1)
            X = X.fillna(X.mean())
            y = data_lr[column]
            data_input = new_data[new_data[column].isnull()]  # строки с пропуском значения, их заполняем
            X_input = data_input.drop([column, 'id'], axis=1)
            X_input = X_input.fillna(0)

            if X_input.shape[0] > 0:  # если нужно заполнить значения, то
                reg = LinearRegression().fit(X, y)
                y_pred = pd.DataFrame(reg.predict(X_input))
                ind = data_input.index
                y_pred = y_pred.set_index(ind)
                data_input[column] = y_pred
                data_output = data_lr.merge(data_input, how='outer')
                new_data = data_output
    return data_output


def miss_fit(dataset, all_params):
    """
    Главная функция по заполнению пропусков, дергает остальные
    :param dataset: датасет с пропусками
    :param all_params: словарь all_params
    :return: датасет без пропусков
    """
    method = all_params['common params']['filling gaps method']
    # print(method)
    if 'HardRemoval' in method:
        dataset = miss_hard_removal(dataset)
    elif 'InsertMeanMode' in method:
        dataset = miss_insert_mean_mode(dataset, all_params['filling gaps method'][method]['threshold'])
    elif 'LinearImputer' in method:
        dataset = miss_linear_imputer(dataset)
    return dataset

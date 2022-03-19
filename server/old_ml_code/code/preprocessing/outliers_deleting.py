from scipy.stats import norm, kstest
import scipy.stats as stats
import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor


def check_norm_dist(dataset, alpha, numeric_cols):
    dataset = dataset[numeric_cols]
    for columns in dataset.columns:
        loc, scale = norm.fit(dataset[columns])
        n = norm(loc=loc, scale=scale)
        statistica, pvalue = kstest(dataset[columns], n.cdf)
        if pvalue < alpha:
            return False
    return True


def outlier_three_sigma(df):
    return df[(df - df.mean()).abs() > 3 * df.std()].dropna(axis=0, how='any').index


# alpha - это критерий значимости для критического значения Граббса
def outlier_grubbs(df, alpha, numeric_cols):
    dataset = df.copy()
    outlier = []
    # проверяем данные на нормальное распределение
    if (not check_norm_dist(dataset, alpha, numeric_cols)):
        print('Гипотеза о нормальности распределения данных отвергнута. Невозможно применить критерий.')
        return outlier
    size = len(dataset)
    # расчёт критического значения
    t_dist = stats.t.ppf(1 - alpha / (2 * size), size - 2)
    numerator = (size - 1) * np.sqrt(np.square(t_dist))
    denominator = np.sqrt(size) * np.sqrt(size - 2 + np.square(t_dist))
    critical_value = numerator / denominator
    for column in dataset:
        grub = pd.DataFrame((map(lambda x: abs((x - dataset[column].mean())) / dataset[column].std(), dataset[column])))
        if grub.max()[0] > critical_value:
            outlier.append(grub.idxmax()[0])
    return outlier


def outlier_interquartile_distance(df, low_quantile, up_quantile, coef):
    dataset = df.copy()
    quantile = dataset.quantile([low_quantile, up_quantile])

    for column in dataset:
        low_lim = quantile[column][low_quantile]
        up_lim = quantile[column][up_quantile]
        dataset = dataset.loc[dataset[column] >= low_lim - coef * (up_lim - low_lim)]. \
            loc[dataset[column] <= up_lim + coef * (up_lim - low_lim)]
    return df.drop(dataset.index).index


def outliers_IsolationForest(df, estimate, contamination):
    dataset = df.copy()
    IF = IsolationForest(n_estimators=estimate, contamination=contamination)
    df_with_forest = dataset.join(pd.DataFrame(IF.fit_predict(dataset),
                                               index=dataset.index, columns=['isolation_forest']), how='left')
    return df_with_forest.loc[df_with_forest['isolation_forest'] != 1].index


def outliers_EllipticEnvelope(df, contamination):
    dataset = df.copy()
    clf = EllipticEnvelope(contamination=contamination)

    df_with_ellip = dataset.join(pd.DataFrame(clf.fit_predict(dataset),
                                              index=dataset.index, columns=['elliptic']), how='left')

    return df_with_ellip.loc[df_with_ellip['elliptic'] != 1].index


def outliers_OneClassSVM(df, iters):
    dataset = df.copy()
    OCSVM = OneClassSVM(kernel='rbf', gamma='auto', max_iter=iters)
    df_with_svm = dataset.join(pd.DataFrame(OCSVM.fit_predict(dataset),
                                            index=dataset.index, columns=['svm']), how='left')

    return df_with_svm.loc[df_with_svm['svm'] != 1].index


def outliers_Approximate(df, deviation):
    M = df.copy()
    u, s, vh = np.linalg.svd(M, full_matrices=True)
    Mk_rank = np.linalg.matrix_rank(M) - deviation

    Uk, Sk, VHk = u[:, :Mk_rank], np.diag(s)[:Mk_rank, :Mk_rank], vh[:Mk_rank, :]
    Mk = pd.DataFrame(np.dot(np.dot(Uk, Sk), VHk), index=M.index, columns=M.columns)
    delta = abs(Mk - M)

    return delta.idxmax()


def outliers_Localfactor(df, neigh, contamination, algorithm):
    dataset = df.copy()
    LOF = LocalOutlierFactor(n_neighbors=neigh, p=2, algorithm=algorithm, metric_params=None,
                             contamination=contamination)
    df_with_lof = dataset.join(pd.DataFrame(LOF.fit_predict(dataset),
                                            index=dataset.index, columns=['lof']), how='left')
    return df_with_lof.loc[df_with_lof['lof'] != 1].index


def outliers_fit(dataset, all_params, numeric_cols):
    """
    Главная функция в удалении выбромов, к остальным ничего напишу, так как не все знаю
    :param dataset: датафрейм без пропусков
    :param all_params: словарь all_params
    :param numeric_cols: глобальный объект, мб не гужен
    :return: датафрейм без пропусков и выбросов
    """
    df = dataset.copy()
    df_num = df[numeric_cols]
    df_id = df[['target', 'id']]
    #     print(f'Объектов до метода: {df.shape}')

    method = all_params['common params']['deleting anomalies method']
    #     print(f'Метод исключения выбросов: {method}')

    if method == 'ThreeSigma':
        outlier = outlier_three_sigma(df_num)
    elif method == 'Grubbs':
        outlier = outlier_grubbs(df_num, all_params['deleting anomalies method'][method]['alpha'], numeric_cols)
    elif method == 'Interquartile':
        outlier = outlier_interquartile_distance(df_num, all_params['deleting anomalies method'][method]['low_quant'],
                                                 all_params['deleting anomalies method'][method]['up_quant'],
                                                 all_params['deleting anomalies method'][method]['coef'])
    elif method == 'IsolationForest':
        outlier = outliers_IsolationForest(df_num, all_params['deleting anomalies method'][method]['n_estimators'],
                                           all_params['deleting anomalies method'][method]['contamination'])
    elif method == 'Elliptic':
        outlier = outliers_EllipticEnvelope(df_num, all_params['deleting anomalies method'][method]['contamination'])
    elif method == 'SVM':
        outlier = outliers_OneClassSVM(df_num, all_params['deleting anomalies method'][method]['iters'])
    elif method == 'Approximate':
        outlier = outliers_Approximate(df_num, all_params['deleting anomalies method'][method]['deviation'])
    elif method == 'LocalFactor':
        outlier = outliers_Localfactor(df_num, all_params['deleting anomalies method'][method]['neigh'],
                                       all_params['deleting anomalies method'][method]['contamination'],
                                       all_params['deleting anomalies method'][method]['algorithm'])

    df_num, df_id = df_num.drop(outlier), df_id.drop(outlier)
    df = df_num.join(df_id, how='left')

    #     print(f'Объектов после: {df.shape}')
    return df

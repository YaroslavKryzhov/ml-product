from sklearn.feature_selection import VarianceThreshold, SelectKBest, SelectPercentile, SelectFpr, SelectFdr, SelectFwe, \
    GenericUnivariateSelect, RFE, SelectFromModel
from sklearn.linear_model import LogisticRegression
from Web_classification_constructor_backend.settings import MEDIA_ROOT
import pickle
import os


def feature_selection_fit(df, all_params, features):
    """

    :param df: датафрейм (уже без пропусков и выбросов и нормализованный)
    :param all_params: словарь all_params
    :param features: все фичи (по сути то же, что и numeric cols)
    :return: готовый датафрейм + список выбранных признаков
    """
    selection_type = all_params['common params']['feature selection method']
    #     print(selection_type)

    if selection_type == 'VarianceThreshold':
        selector = VarianceThreshold(threshold=all_params['feature selection method'][selection_type]['threshold'])
        selector.fit(df[features])

    elif selection_type == 'SelectKBest':
        k = all_params['feature selection method'][selection_type]['k']
        if k > df[features].shape[1]:
            k = df[features].shape[1]
        selector = SelectKBest(k=k)
        selector.fit(df[features], df['target'])

    elif selection_type == 'SelectPercentile':
        selector = SelectPercentile(percentile=all_params['feature selection method'][selection_type]['percentile'])
        selector.fit(df[features], df['target'])

    elif selection_type == 'SelectFpr':
        selector = SelectFpr(alpha=all_params['feature selection method'][selection_type]['alpha'])
        selector.fit(df[features], df['target'])

    elif selection_type == 'SelectFdr':
        selector = SelectFdr(alpha=all_params['feature selection method'][selection_type]['alpha'])
        selector.fit(df[features], df['target'])

    elif selection_type == 'SelectFwe':
        selector = SelectFwe(alpha=all_params['feature selection method'][selection_type]['alpha'])
        selector.fit(df[features], df['target'])

    elif selection_type == 'GenericUnivariateSelect':
        mode = all_params['feature selection method'][selection_type]['mode']
        param = all_params['feature selection method'][selection_type]['param']

        if mode == 'k_best':  # возможно, еще для каких-то вариантов mode будет значение int
            param = int(param)

        selector = GenericUnivariateSelect(mode=mode, param=param)
        selector.fit(df[features], df['target'])

    elif selection_type == 'RFE':
        lr = LogisticRegression()  # пока в качестве estimator оставим лог.регрессию (дальше решим)
        selector = RFE(estimator=lr,
                       n_features_to_select=all_params['feature selection method'][selection_type][
                           'n_features_to_select'],
                       step=all_params['feature selection method'][selection_type]['step'])
        selector.fit(df[features], df['target'])

    elif selection_type == 'SelectFromModel':
        lr = LogisticRegression()  # пока в качестве estimator оставим лог.регрессию (дальше решим)
        selector = SelectFromModel(estimator=lr,
                                   threshold=all_params['feature selection method'][selection_type]['threshold'],
                                   # пока даем возможность только выбрать из списка (а не float)
                                   norm_order=all_params['feature selection method'][selection_type]['norm_order'],
                                   max_features=all_params['feature selection method'][selection_type]['max_features'])
        selector.fit(df[features], df['target'])

    with open(os.path.join(f"{MEDIA_ROOT}",  'App/models/feature_selector.pickle'), 'wb+') as f:
        pickle.dump(selector, f)

    new_cols = [x[0] for x in zip(features, selector.get_support()) if x[1] == True]
    #     print(new_cols+['id','target'])

    selected = df.loc[:, new_cols + ['id', 'target']]

    return selected, new_cols

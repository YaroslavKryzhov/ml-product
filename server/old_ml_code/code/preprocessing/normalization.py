from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd


def normalize(train_outliers, numeric_cols, test):
    """

    :param train_outliers: датафрейм (без пропусков и выбросов)
    :param numeric_cols: глобальный объект (мб не нужен)
    :param test: тестовый датафрейм, его тоже надо нормализовать
    :return: нормализованный датафрейм
    """
    df_id = train_outliers[['target', 'id']]

    # перед отбором надо нормализовать
    sc = StandardScaler()
    sc.fit(train_outliers.drop(columns=['target', 'id']))
    train_scaled = sc.transform(train_outliers.drop(columns=['target', 'id']))
    test[numeric_cols] = sc.transform(test[numeric_cols])

    train_scaled_df = pd.DataFrame(train_scaled, columns=numeric_cols)

    train_scaled_all = pd.concat([train_scaled_df, df_id], axis=1)
    return train_scaled_all

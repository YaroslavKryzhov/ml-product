import pandas as pd

from ml_api.apps.dataframes import schemas


def _get_dataframe_with_pagination(df, page, rows_on_page):
    length = len(df)
    pages_count = (length - 1) // rows_on_page + 1
    start_index = (page - 1) * rows_on_page
    stop_index = page * rows_on_page
    if stop_index < length:
        return {
            'total': pages_count,
            'records': df.iloc[start_index:stop_index]
            .fillna("")
            .to_dict('list'),
        }
    elif start_index < length:
        return {
            'total': pages_count,
            'records': df.iloc[start_index:]
            .fillna("")
            .to_dict('list'),
        }
    else:
        return {
            'total': pages_count,
            'records': pd.DataFrame().fillna("").to_dict('list'),
        }


def _get_numeric_column_statistics(df: pd.DataFrame, column_name: str, bins: int
                                   ) -> schemas.ColumnDescription:
    ints = (
        df[column_name].value_counts(bins=bins).sort_index().reset_index()
    )
    ints['start'] = ints['index'].apply(lambda x: x.left)
    ints['end'] = ints['index'].apply(lambda x: x.right)
    ints.drop('index', axis=1, inplace=True)
    ints.columns = ['value', 'left', 'right']
    data = list(ints.to_dict('index').values())
    not_null_count = df[column_name].notna().sum()
    null_count = df[column_name].isna().sum()
    data_type = str(df[column_name].dtype)
    column_stats = _get_numeric_column_statistic_params(df[column_name])
    return schemas.ColumnDescription(
        name=column_name,
        type='numeric',
        data_type=data_type,
        not_null_count=not_null_count,
        null_count=null_count,
        data=data,
        column_stats=column_stats
    )


def _get_categorical_column_statistics(
        df: pd.DataFrame, column_name: str) -> schemas.ColumnDescription:
    ints = df[column_name].value_counts(normalize=True).reset_index()
    ints.columns = ['name', 'value']
    data = list(ints.to_dict('index').values())
    not_null_count = df[column_name].notna().sum()
    null_count = df[column_name].isna().sum()
    data_type = str(df[column_name].dtype)
    column_stats = _get_categorical_column_statistic_params(df[column_name])
    return schemas.ColumnDescription(
        name=column_name,
        type='categorical',
        data_type=data_type,
        not_null_count=not_null_count,
        null_count=null_count,
        data=data,
        column_stats=column_stats
    )


def _get_numeric_column_statistic_params(column: pd.Series) -> schemas.NumericColumnDescription:
    result = column.describe()
    result.index = [
        "count",
        "mean",
        "std",
        "min",
        "first_percentile",
        "second_percentile",
        "third_percentile",
        "max",
    ]
    return schemas.NumericColumnDescription(**result.to_dict())


def _get_categorical_column_statistic_params(column: pd.Series) -> schemas.NumericColumnDescription:
    result = {'nunique': column.nunique(),
              'most_frequent': column.value_counts().iloc[:5].to_dict()}
    return schemas.CategoricalColumnDescription(**result)


def _convert_column_to_categorical(series: pd.Series) -> pd.Series:
    series = series.astype(str)
    return series


def _convert_column_to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series)

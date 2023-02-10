from typing import List
import pandas as pd

from ml_api.apps.dataframes.controller.schemas import ColumnDescription, DataFrameDescription, ColumnTypes


def _define_column_types(df: pd.DataFrame) -> ColumnTypes:
    numeric_columns = df.select_dtypes('number').columns.to_list()
    categorical_columns = df.select_dtypes(
        include=['object', 'category']
    ).columns.to_list()
    return ColumnTypes(
            numeric=numeric_columns,
            categorical=categorical_columns
    )


def _get_column_histogram_data(df: pd.DataFrame, column_name: str, bins: int
                               ) -> ColumnDescription:
    ints = (
        df[column_name].value_counts(bins=bins).sort_index().reset_index()
    )
    ints['start'] = ints['index'].apply(lambda x: x.left)
    ints['end'] = ints['index'].apply(lambda x: x.right)
    ints.drop('index', axis=1, inplace=True)
    ints.columns = ['value', 'left', 'right']
    data = list(ints.to_dict('index').values())
    not_null_count = df[column_name].notna().sum()
    data_type = str(df[column_name].dtype)
    return ColumnDescription(
        name=column_name,
        type='numeric',
        not_null_count=not_null_count,
        data_type=data_type,
        data=data,
    )


def _get_column_value_counts_data(df: pd.DataFrame, column_name: str
                                  ) -> ColumnDescription:
    ints = df[column_name].value_counts(normalize=True).reset_index()
    ints.columns = ['name', 'value']
    data = list(ints.to_dict('index').values())
    not_null_count = df[column_name].notna().sum()
    data_type = str(df[column_name].dtype)
    return ColumnDescription(
        name=column_name,
        type='categorical',
        not_null_count=not_null_count,
        data_type=data_type,
        data=data,
    )


def _get_dataframe_statistic_description_data(df: pd.DataFrame
                                              ) -> DataFrameDescription:
    result = df.describe()
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
    return DataFrameDescription(**result.to_dict('index'))

import pandas as pd


def get_predictions_df(features: pd.DataFrame, res_column: pd.Series):
    predictions_df = pd.concat([features.reset_index(drop=True),
                                res_column.reset_index(drop=True)], axis=1)
    return predictions_df
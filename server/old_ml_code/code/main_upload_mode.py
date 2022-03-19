import os
import pickle
import pandas as pd
from Classification_constructor_code.code.preprocessing.missing_values_imputing import miss_linear_imputer
from sklearn.preprocessing import StandardScaler
from Web_classification_constructor_backend.settings import MEDIA_ROOT


def main_function_upload_mode():
    pickle_path = os.path.join(f"{MEDIA_ROOT}", 'Input/model.pickle')
    test_path = os.path.join(f"{MEDIA_ROOT}", 'Input/test.csv')

    try:
        test_df = pd.read_csv(test_path)
        test_miss = miss_linear_imputer(test_df)


        df_id = test_miss[['id']]

        # перед отбором надо нормализовать
        sc = StandardScaler()
        sc.fit(test_miss.drop(columns=['id']))
        test_scaled = sc.transform(test_miss.drop(columns=['id']))

        test_scaled_df = pd.DataFrame(test_scaled, columns=test_miss.drop(columns=['id']).columns)

        test_scaled_all = pd.concat([test_scaled_df, df_id], axis=1)

        with open(pickle_path, 'rb') as f:
            model = pickle.load(f)

        y_prob_test = model[0].predict_proba(test_scaled_all[model[1]])[:, 1]
        prediction = pd.DataFrame([], columns=['id', 'prob', 'pred'])
        prediction['id'] = test_miss['id']

        prediction['prob'] = y_prob_test
        prediction['pred'] = [1 if x > 0.5 else 0 for x in y_prob_test]

        # return prediction

        pred_test_with_features = test_df.merge(prediction, on='id')
        pred_test_with_features.to_csv(os.path.join(f"{MEDIA_ROOT}", 'Output/fin_test_upload_mode.csv'))
    except Exception:
        pass

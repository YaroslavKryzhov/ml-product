from math import sqrt
from typing import Dict, List

from sklearn.metrics import (
    accuracy_score, recall_score, precision_score, f1_score,
    roc_auc_score, roc_curve, mean_squared_error, mean_absolute_error,
    silhouette_score, davies_bouldin_score, auc, mean_absolute_percentage_error
)
from sklearn.preprocessing import label_binarize
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd

from ml_api.apps.ml_models.specs import AvailableTaskTypes
from ml_api.apps.training_reports import model, schemas
from ml_api.apps.training_reports.specs import ReportTypes


class ReportCreatorService:

    def score_regression(self, target,
                         predictions, is_train=False) -> model.Report:
        report_type = ReportTypes.TRAIN if is_train else ReportTypes.VALID
        mse = mean_squared_error(target, predictions)
        mae = mean_absolute_error(target, predictions)
        rmse = sqrt(mse)
        mape = mean_absolute_percentage_error(target, predictions)

        body = schemas.RegressionReport(mse=mse, mae=mae, rmse=rmse,
                                       mape=mape,)
        return model.Report(task_type=AvailableTaskTypes.REGRESSION,
                             report_type=report_type,
                             body=body)

    def score_binary_classification(self, target, predictions, probabilities
                                    , is_train=False) -> model.Report:
        report_type = ReportTypes.TRAIN if is_train else ReportTypes.VALID
        accuracy = accuracy_score(target, predictions)
        try:
            recall = recall_score(target, predictions)
            precision = precision_score(target, predictions)
            f1 = f1_score(target, predictions)
        except ValueError:
            recall = None
            precision = None
            f1 = None
        roc_auc, fpr, tpr = None, None, None
        if probabilities is not None:
            roc_auc = roc_auc_score(target, probabilities)
            try:
                fpr, tpr, _ = roc_curve(target, probabilities)
                fpr = list(fpr)
                tpr = list(tpr)
            except ValueError:
                pass
        body = schemas.BinaryClassificationReport(accuracy=accuracy,
                                                 recall=recall,
                                                 precision=precision,
                                                 f1=f1, roc_auc=roc_auc,
                                                 fpr=fpr, tpr=tpr,)
        return model.Report(task_type=AvailableTaskTypes.CLASSIFICATION,
                             report_type=report_type,
                             body=body)

    def score_multiclass_classification(self, classes, target, predictions,
            probabilities, is_train=False) -> model.Report:
        report_type = ReportTypes.TRAIN if is_train else ReportTypes.VALID
        accuracy = accuracy_score(target, predictions)
        recall = recall_score(target, predictions, average='weighted')
        precision = precision_score(
            target, predictions, average='weighted'
        )
        f1 = f1_score(target, predictions, average='weighted')
        roc_auc_weighted, roc_auc_micro, roc_auc_macro, fpr_micro, fpr_macro, \
        tpr_micro, tpr_macro = None, None, None, None, None, None, None
        if probabilities is not None:
            target_valid = label_binarize(target, classes=classes)
            n_classes = len(classes)
            roc_auc_weighted = roc_auc_score(target_valid, probabilities,
                                             average='weighted',
                                             multi_class='ovr')
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(
                    target_valid[:, i], probabilities[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])
            fpr["micro"], tpr["micro"], _ = roc_curve(
                target_valid.ravel(), probabilities.ravel())
            roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
            # First aggregate all false positive rates
            all_fpr = np.unique(
                np.concatenate([fpr[i] for i in range(n_classes)]))
            # Then interpolate all ROC curves at this points
            mean_tpr = np.zeros_like(all_fpr)
            for i in range(n_classes):
                mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])
            # Finally average it and compute AUC
            mean_tpr /= n_classes
            fpr["macro"] = all_fpr
            tpr["macro"] = mean_tpr
            roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])
            fpr_micro = list(fpr["micro"])
            tpr_micro = list(tpr["micro"])
            fpr_macro = list(fpr["macro"])
            tpr_macro = list(tpr["macro"])
            roc_auc_micro = roc_auc["micro"]
            roc_auc_macro = roc_auc["macro"]

        body = schemas.MulticlassClassificationReport(accuracy=accuracy,
            recall=recall,
            precision=precision,
            f1=f1,
            roc_auc_weighted=roc_auc_weighted,
            roc_auc_micro=roc_auc_micro,
            roc_auc_macro=roc_auc_macro,
            fpr_micro=fpr_micro,
            fpr_macro=fpr_macro,
            tpr_micro=tpr_micro,
            tpr_macro=tpr_macro)

        return model.Report(task_type=AvailableTaskTypes.CLASSIFICATION,
                             report_type=report_type,
                             body=body)

    def score_clustering(self, features, labels, is_train=False
                         ) -> model.Report:
        report_type = ReportTypes.TRAIN if is_train else ReportTypes.VALID

        body = schemas.ClusteringReport(
            silhouette_score=silhouette_score(features, labels),
            davies_bouldin_score=davies_bouldin_score(features, labels),
            two_dim_representation=self._get_two_dim_representation(
                features, labels),
            cluster_means=self._get_cluster_feature_means(features, labels)
        )
        return model.Report(task_type=AvailableTaskTypes.CLUSTERING,
                            report_type=report_type,
                            body=body)

    def score_outlier_detection(self, features, outliers, is_train=False
                                ) -> model.Report:
        report_type = ReportTypes.TRAIN if is_train else ReportTypes.VALID

        body = schemas.OutlierDetectionReport(
            contamination=float(np.sum(outliers)) / len(features),
            two_dim_representation=self._get_two_dim_representation(
                features, outliers))
        return model.Report(task_type=AvailableTaskTypes.OUTLIER_DETECTION,
                             report_type=report_type,
                             body=body)

    def score_dimensionality_reduction(self, explained_variance_ratio, is_train=False
                                       ) -> model.Report:
        report_type = ReportTypes.TRAIN if is_train else ReportTypes.VALID
        body = schemas.DimensionalityReductionReport(
            explained_variance=list(explained_variance_ratio))
        return model.Report(task_type=AvailableTaskTypes.DIMENSIONALITY_REDUCTION,
                             report_type=report_type,
                             body=body)

    def _get_two_dim_representation(self, features, target) -> schemas.TwoDimRepresentation:
        # Двухмерное представление данных для визуализации
        pca = PCA(n_components=2)
        two_dim_representation = pd.DataFrame(
            pca.fit_transform(features), columns=['first_dim', 'second_dim'])
        two_dim_representation = pd.concat(
            [two_dim_representation.reset_index(drop=True),
             target.reset_index(drop=True)], axis=1)
        return schemas.TwoDimRepresentation(**two_dim_representation.to_dict('list'))

    def _get_cluster_feature_means(self, features, labels
                                   ) -> Dict[str, Dict[str, float]]:
        df = pd.DataFrame(features)
        df['_cluster_label'] = labels
        # Расчет средних значений признаков для каждого кластера
        cluster_means = df.groupby('_cluster_label').mean()
        return cluster_means.to_dict('index')

    def get_error_report(self, task_type, error_description):
        body = schemas.ErrorReport(error_description=error_description)
        return model.Report(
            task_type=task_type,
            report_type=ReportTypes.ERROR,
            body=body
        )

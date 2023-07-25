from typing import Union, Any

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, recall_score, \
    precision_score, roc_auc_score, roc_curve, auc
from sklearn.preprocessing import label_binarize
import numpy as np

from ml_api.apps.ml_models import schemas, specs


class TrainCompositionException(Exception):
    pass


class CompositionTrainer:
    def __init__(
            self, task_type, composition, model_id, features, target, test_size
    ):
        self.task_type = task_type
        self.composition = composition
        self.model_id = model_id
        self.features = features
        self.target = target
        self.test_size = test_size

    def validate_model(self) -> (Any, Union[schemas.ClassificationMetrics,
                                      schemas.RegeressionMetrics]):
        if self.task_type == specs.AvailableTaskTypes.CLASSIFICATION:
            if self.target.nunique() == 2:
                return self._process_binary_classification()
            else:
                return self._process_multiclass__classification()
        elif self.task_type == specs.AvailableTaskTypes.REGRESSION:
            return self._process_regression()
        else:
            raise TrainCompositionException(
                f'Unknown task type: {self.task_type}')

    def _train_composition(self):
        f_train, f_valid, t_train, t_valid = train_test_split(
            self.features, self.target, test_size=self.test_size,
            stratify=self.target)
        self.composition.fit(f_train, t_train)
        predictions = self.composition.predict(f_valid)
        try:
            probabilities = self.composition.predict_proba(f_valid)[:, 1]
        except AttributeError:
            # try:
            probabilities = self.composition.decision_function(f_valid)
            # TODO: test for different errors
            # except AttributeError:
            #     probabilities = None
        return predictions, probabilities, t_valid

    def _process_binary_classification(self) -> (Any, schemas.ClassificationMetrics):
        predictions, probabilities, target_valid = self._train_composition()

        accuracy = accuracy_score(target_valid, predictions)
        recall = recall_score(target_valid, predictions)
        precision = precision_score(target_valid, predictions)
        f1 = f1_score(target_valid, predictions)

        # if probabilities is not None:
        roc_auc = roc_auc_score(target_valid, probabilities)
        fpr, tpr, _ = roc_curve(target_valid, probabilities)
        fpr = list(fpr)
        tpr = list(tpr)
        report = schemas.ClassificationMetrics(
            accuracy=accuracy,
            recall=recall,
            precision=precision,
            f1=f1,
            roc_auc=roc_auc,
            fpr=fpr,
            tpr=tpr,
        )
        return self.composition, report

    def _process_multiclass__classification(self) -> (Any, schemas.ClassificationMetrics):
        predictions, probabilities, target_valid = self._train_composition()

        accuracy = accuracy_score(target_valid, predictions)
        recall = recall_score(target_valid, predictions, average='weighted')
        precision = precision_score(
            target_valid, predictions, average='weighted'
        )
        f1 = f1_score(target_valid, predictions, average='weighted')

        roc_auc_weighted = None
        roc_auc_micro = None
        roc_auc_macro = None
        fpr_micro = None
        fpr_macro = None
        tpr_micro = None
        tpr_macro = None

        if probabilities is not None:
            classes = list(self.target.unique())
            target_valid = label_binarize(target_valid, classes=classes)
            n_classes = len(classes)

            roc_auc_weighted = roc_auc_score(
                target_valid,
                probabilities,
                average='weighted',
                multi_class='ovr',
            )

            fpr = dict()
            tpr = dict()
            roc_auc = dict()

            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(
                    target_valid[:, i], probabilities[:, i]
                )
                roc_auc[i] = auc(fpr[i], tpr[i])

            fpr["micro"], tpr["micro"], _ = roc_curve(
                target_valid.ravel(), probabilities.ravel()
            )
            roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

            # First aggregate all false positive rates
            all_fpr = np.unique(
                np.concatenate([fpr[i] for i in range(n_classes)])
            )

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

        report = schemas.ClassificationMetrics(
            accuracy=accuracy,
            recall=recall,
            precision=precision,
            f1=f1,
            roc_auc_weighted=roc_auc_weighted,
            roc_auc_micro=roc_auc_micro,
            roc_auc_macro=roc_auc_macro,
            fpr_micro=fpr_micro,
            fpr_macro=fpr_macro,
            tpr_micro=tpr_micro,
            tpr_macro=tpr_macro,
        )
        return self.composition, report

    def _process_regression(self) -> (Any, schemas.RegeressionMetrics):
        #  TODO: add regression
        raise NotImplementedError

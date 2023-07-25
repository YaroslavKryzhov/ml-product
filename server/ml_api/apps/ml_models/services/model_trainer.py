from ml_api.apps.dataframes.services.dataframe_manager import \
    DataframeManagerService
from ml_api.apps.ml_models import specs, errors
from ml_api.apps.ml_models.models import ModelMetadata


class ModelTrainerService:
    def __init__(self, user_id, model_meta: ModelMetadata, model):
        self._user_id = user_id
        self.model = model
        self.task_type = model_meta.task_type
        self.model_id = model_meta.id
        self.dataframe_id = model_meta.dataframe_id
        self.feature_columns = model_meta.feature_columns
        self.target_column = model_meta.target_column
        self.test_size = model_meta.test_size
        self.dataframe_manager = DataframeManagerService(self._user_id)

    async def train_model(self):
        if self.task_type == specs.AvailableTaskTypes.CLASSIFICATION:
            return self._process_classification()
        elif self.task_type == specs.AvailableTaskTypes.REGRESSION:
            return self._process_regression()
        elif self.task_type == specs.AvailableTaskTypes.CLUSTERING:
            return self._process_clustering()
        elif self.task_type == specs.AvailableTaskTypes.OUTLIER_DETECTION:
            return self._process_outlier_detection()
        elif self.task_type == specs.AvailableTaskTypes.DIMENSIONALITY_REDUCTION:
            return self._process_dimensionality_reduction()
        else:
            raise errors.UnknownTaskTypeError(self.task_type)

    async def _process_classification(self):
        classes_limit = 10
        features, target = self.dataframe_manager.get_feature_target_df(
            dataframe_id=self.dataframe_id)
        num_classes = target.nunique()
        if num_classes < 2:
            raise errors.OneClassClassificationError(self.dataframe_id)
        elif num_classes == 2:
            return self._process_binary_classification()
        elif num_classes <= classes_limit:
            return self._process_multiclass_classification()
        else:
            raise errors.TooManyClassesClassificationError(
                classes_limit, self.dataframe_id)

    def _process_binary_classification(self):

        # fit
        # score
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

    # def _score_binary_classification(self, ): -> to utils

    def _process_multiclass_classification(self) -> (Any, schemas.ClassificationMetrics):
        predictions, probabilities, target_valid = self._fit_model()

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

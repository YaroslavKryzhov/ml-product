import { AppliedMethodTypes, Methods } from "@/utils/enums";

export interface IDataframe {
    "_id": string;
    "parent_id": string | null;
    "filename": string;
    "user_id": string;
    "is_prediction": boolean;
    "feature_columns_types": any;
    "target_feature": string | null;
    "pipeline": any[];
    "feature_importance_report": any | null;
    "created_at": string;
}

export interface ISimpleDataframe {
    id: string;
    filename: string;
    children: ISimpleDataframe[];
}

export const methods: IRawMethod[] = [
    { method_name: 'drop_duplicates', literal: Methods.drop_duplicates, type: AppliedMethodTypes.DROP },
    { method_name: 'drop_na', literal: Methods.drop_na, type: AppliedMethodTypes.DROP },
    // { method_name: 'drop_columns', literal: Methods.drop_columns, type: AppliedMethodTypes.DROP },
    { method_name: 'fill_mean', literal: Methods.fill_mean, type: AppliedMethodTypes.FILL },
    { method_name: 'fill_median', literal: Methods.fill_median, type: AppliedMethodTypes.FILL },
    { method_name: 'fill_most_frequent', literal: Methods.fill_most_frequent, type: AppliedMethodTypes.FILL },
    { method_name: 'fill_custom_value', literal: Methods.fill_custom_value, type: AppliedMethodTypes.FILL },
    { method_name: 'fill_bfill', literal: Methods.fill_bfill, type: AppliedMethodTypes.FILL },
    { method_name: 'fill_ffill', literal: Methods.fill_ffill, type: AppliedMethodTypes.FILL },
    { method_name: 'fill_interpolation', literal: Methods.fill_interpolation, type: AppliedMethodTypes.FILL },
    { method_name: 'fill_linear_imputer', literal: Methods.fill_linear_imputer, type: AppliedMethodTypes.FILL },
    { method_name: 'fill_knn_imputer', literal: Methods.fill_knn_imputer, type: AppliedMethodTypes.FILL },
    // { method_name: 'leave_n_values_encoding', literal: Methods.leave_n_values_encoding, type: AppliedMethodTypes.ENCODE },
    { method_name: 'one_hot_encoding', literal: Methods.one_hot_encoding, type: AppliedMethodTypes.ENCODE },
    { method_name: 'ordinal_encoding', literal: Methods.ordinal_encoding, type: AppliedMethodTypes.ENCODE },
    { method_name: 'standard_scaler', literal: Methods.standard_scaler, type: AppliedMethodTypes.SCALE },
    { method_name: 'min_max_scaler', literal: Methods.min_max_scaler, type: AppliedMethodTypes.SCALE },
    { method_name: 'robust_scaler', literal: Methods.robust_scaler, type: AppliedMethodTypes.SCALE }
];

export interface IRawMethod {
    method_name: string;
    literal: Methods;
    type: AppliedMethodTypes;
}

export interface IColumn {
    "name": string;
    "type": string;
    "data_type": string;
    "not_null_count": number;
    "null_count": number;
    "data": any[];
    "column_stats": {
        "count": number;
        "mean": number;
        "std": number;
        "min": number;
        "first_percentile": number;
        "second_percentile": number;
        "third_percentile": number;
        "max": number;
    }
}

export interface IAppliedMethod extends IRawMethod {
    columns: string[];
}

export interface IModel {
    "_id": string;
    "filename": string;
    "user_id": string;
    "dataframe_id": string;
    "is_composition": boolean;
    "task_type": string;
    "model_params": {
        "model_type": string,
        "params": any
    };
    "params_type": string;
    "feature_columns": string[];
    "target_column": string[];
    "test_size": number;
    "stratify": boolean;
    "status": string;
    "metrics_report_ids": string[];
    "model_prediction_ids": string[];
    "composition_model_ids": string[];
    "created_at": string;
}

export interface IJob {
    "_id": string;
    "user_id": string;
    "type": string;
    "object_type": string;
    "object_id": string;
    "status": string;
    "input_params": {
        "method_params": any[],
        "new_filename": string
    };
    "output_message": string;
    "started_at": string;
    "finished_at": string;
}

export interface IParam {
    default: any;
    title: string;
    type: string; // string, integer

    // string
    enum?: string[];

    // integer
    exclusiveMinimum?: number;
    exclusiveMaximum?: number;
    maximum?: number;
    minimum?: number;
}

export interface IPrediction {
    "_id": string;
    "parent_id": string | null;
    "filename": string;
    "user_id": string;
    "is_prediction": true;
    "feature_columns_types": {
        "numeric": string[],
        "categorical": string[]
    };
    "target_feature": string | null;
    "pipeline": any[];
    "feature_importance_report": any | null;
    "created_at": string;
}
### Feature Selection

```javascript
[
    {
      "method_name": "VarianceThreshold",
      "params": {
        "threshold": 0.1
      }
    },
    {
      "method_name": "SelectKBest",
      "params": {
        "k": 5
      }
    },
    {
      "method_name": "SelectPercentile",
      "params": {
        "percentile": 10
      }
    },
    {
      "method_name": "SelectFpr",
      "params": {
        "alpha": 0.05
      }
    },
    {
      "method_name": "SelectFdr",
      "params": {
        "alpha": 0.05
      }
    },
    {
      "method_name": "SelectFwe",
      "params": {
        "alpha": 0.05
      }
    },
    {
      "method_name": "RecursiveFeatureElimination",
      "params": {
        "n_features_to_select": 5,
        "step": 1,
        "estimator": "logistic_regression"
      }
    },
    {
      "method_name": "SequentialForwardSelection",
      "params": {
        "n_features_to_select": 5,
        "estimator": "random_forest_classifier"
      }
    },
    {
      "method_name": "SequentialBackwardSelection",
      "params": {
        "n_features_to_select": 5,
        "estimator": "logistic_regression"
      }
    },
    {
      "method_name": "SelectFromModel",
      "params": {
        "estimator": "logistic_regression"
      }
    }
  ]
```

### Apply Methods for data_raw.csv

```javascript
[
  {
    "method_name": "fill_mean",
    "columns": [
      "days_employed", "total_income"
    ],
    "params": {}
  },
  {
    "method_name": "one_hot_encoding",
    "columns": [
      "gender"
    ],
    "params": {}
  },
  {
    "method_name": "ordinal_encoding",
    "columns": [
      "education_id", "family_status_id", "income_type"
    ],
    "params": {}
  },
	{
    "method_name": "standard_scaler",
    "columns": [
      "days_employed",
      "dob_years",
      "total_income",
      "gender_M",
      "gender_XNA",
      "education_id",
      "family_status_id",
      "income_type",
      "children"
    ],
    "params": {}
  }
]
```

```javascript
[  
{
    "method_name": "change_columns_type",
    "columns": [
      "children"
    ],
    "params": {"new_type": "numeric"}
  },{
    "method_name": "drop_duplicates",
    "columns": [
      
    ],
    "params": {}
  },{
    "method_name": "drop_na",
    "columns": [
      "dob_years"
    ],
    "params": {}
  },{
    "method_name": "fill_mean",
    "columns": [
      "dob_years"
    ],
    "params": {}
  },{
    "method_name": "fill_median",
    "columns": [
      "dob_years"
    ],
    "params": {}
  },{
    "method_name": "fill_most_frequent",
    "columns": [
      "gender"
    ],
    "params": {}
  },{
    "method_name": "fill_bfill",
    "columns": [
      "dob_years"
    ],
    "params": {}
  },{
    "method_name": "fill_ffill",
    "columns": [
      "dob_years"
    ],
    "params": {}
  },{
    "method_name": "fill_interpolation",
    "columns": [
      "dob_years"
    ],
    "params": {}
  },{
    "method_name": "fill_linear_imputer",
    "columns": [
      "dob_years"
    ],
    "params": {}
  },{
    "method_name": "fill_knn_imputer",
    "columns": [
      "dob_years"
    ],
    "params": {}
  },
  {
    "method_name": "fill_custom_value",
    "columns": [
      "days_employed", "total_income"
    ],
    "params": {"values_to_fill":[0, 0]}
  },
  {
    "method_name": "leave_n_values_encoding",
    "columns": [
      "gender"
    ],
    "params": {"values_to_keep": [["F"]]}
  },
  {
    "method_name": "one_hot_encoding",
    "columns": [
      "gender", "income_type"
    ],
    "params": {}
  },
  {
    "method_name": "ordinal_encoding",
    "columns": [
      "education_id", "family_status_id"
    ],
    "params": {}
  }, 
  {
    "method_name": "standard_scaler",
    "columns": [
      "days_employed",
        "dob_years",
        "total_income",
        "children"
    ],
    "params": {}
  },
  {
    "method_name": "min_max_scaler",
    "columns": [
      "gender_Others",
        "income_type_в декрете",
        "income_type_госслужащий",
        "income_type_компаньон",
        "income_type_пенсионер"
    ],
    "params": {}
  },
{
    "method_name": "robust_scaler",
    "columns": [
       "income_type_предприниматель",
        "income_type_сотрудник",
        "income_type_студент",
        "education_id",
        "family_status_id"
    ],
    "params": {}
  }
]
```

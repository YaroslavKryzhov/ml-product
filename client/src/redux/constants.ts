export const HOST = "localhost:6060";
export const BASE_API = `http://${HOST}/api/v1`;

export const ROUTES = {
  AUTH: {
    BASE: BASE_API + "/auth",
    LOGIN: "jwt/login",
    REGISTER: "register",
    LOGOUT: "jwt/logout",
  },
  DOCUMENTS: {
    BASE: BASE_API + "/dataframe",
    SHOW: "/df",
    INFO: "/",
    DF_INFO: "/df/statistics",
    DESCRIBE: "/df/describe",
    DOWNLOAD: "/download",
    PIPE: "/pipeline",
    ALL: "/all",
    RENAME: "/rename",
    COLUMNS: "/df/columns",
    APPLY_METHOD: "/edit/apply_method",
    SET_CATEGORICAL: "/edit/apply_method",
    SELECT_TARGET: "/edit/target",
    MARK_CATEGORICAL: "/edit/to_categorical",
    MARK_NUMERIC: "/edit/to_numeric",
    COPY_PIPELINE: "/edit/copy_pipeline",
    DELETE_COLUMN: "/edit/column",
  },
  COMPOSITIONS: {
    BASE: BASE_API + "/composition",
    TRAIN: "/train",
    PREDICT: "/predict",
    DOWNLOAD: "/download",
    RENAME: "/rename",
    ALL: "/all",
    INFO: "/info",
  },
};

export const COPY_PIPELINE_ID = "copy_pipe";

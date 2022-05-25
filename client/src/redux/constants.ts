export const HOST = "http://localhost:8006";
export const BASE_API = HOST;

export const ROUTES = {
  AUTH: {
    BASE: BASE_API + "/auth",
    LOGIN: "jwt/login",
    REGISTER: "register",
    LOGOUT: "jwt/logout",
  },
  DOCUMENTS: {
    BASE: BASE_API + "/document",
    SHOW: "/df",
    INFO: "/info",
    STATS_INFO: "/df/stats/info",
    STATS_COLUMNS: "/df/stats/columns",
    DESCRIBE: "/df/stats/describe",
    DOWNLOAD: "/download",
    PIPE: "/pipeline",
    ALL: "/all",
    RENAME: "/rename",
    COLUMNS: "/df/columns",
    COLUMN_MARKS: "/process/column_marks",
    APPLY_METHOD: "/process/apply",
  },
};

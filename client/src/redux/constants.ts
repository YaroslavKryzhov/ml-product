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
    INFO: "/info",
    STATS_INFO: "/stats/info",
    DESCRIBE: "/stats/describe",
    DOWNLOAD: "/download",
    PIPE: "/pipeline",
    ALL: "/all",
    RENAME: "/rename",
    COLUMNS: "/columns",
    COLUMN_MARKS: "/column_marks",
    APPLY_METHOD: "/process/apply",
  },
};

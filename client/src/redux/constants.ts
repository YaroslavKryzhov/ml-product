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
    DOWNLOAD: "/download",
    PIPE: "/pipeline",
    ALL: "/all",
    RENAME: "/rename",
    COLUMNS: "/column_marks",
  },
};

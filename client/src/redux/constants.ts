export const HOST = "http://localhost:3000";
export const BASE_API = HOST + "/api";

export const ROUTES = {
  AUTH: {
    BASE: BASE_API + "/auth",
    LOGIN: "jwt/login",
    REGISTER: "jwt/register",
    LOGOUT: "jwt/logout",
  },
};

import jwt from "jsonwebtoken";
import { logout } from "../reducers/main";
import { DecodedToken } from "../reducers/types";
import { store } from "../store";

window.addEventListener("DOMContentLoaded", () => {
  const alreadyToken = localStorage.authToken;

  if (alreadyToken) {
    const decoded = jwt.decode(alreadyToken) as DecodedToken;

    if (isFinite(decoded.exp) && Date.now() > decoded.exp) {
      store.dispatch(logout());
    }
  }
});

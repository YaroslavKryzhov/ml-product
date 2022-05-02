import jwt_decode from "jwt-decode";
import {
  changeAppPage,
  changeIsBlockingLoader,
  logout,
} from "../reducers/main";
import { AppPage, DecodedToken } from "../reducers/types";
import { store } from "../store";

window.addEventListener("DOMContentLoaded", () => {
  const alreadyToken = localStorage.authToken;
  if (alreadyToken) {
    const decoded = jwt_decode(alreadyToken) as DecodedToken;

    if (isFinite(decoded.exp) && Date.now() > decoded.exp * 1000) {
      store.dispatch(logout());
    } else {
      store.dispatch(changeAppPage(AppPage.Workplace));
    }
  }

  store.dispatch(changeIsBlockingLoader(false));
});

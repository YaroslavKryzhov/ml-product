import jwt_decode from "jwt-decode";
import { changeIsBlockingLoader } from "../reducers/main";
import {
  AppPage,
  AuthPage,
  DecodedToken,
  DocumentPage,
  WorkPage,
} from "../reducers/types";
import { store } from "../store";
import { browserHistory, pathify } from "ducks/hooks";

const redirectAuth = () => {
  localStorage.authToken = "";
  browserHistory.push(pathify([AppPage.Authentication, AuthPage.auth]));
};

window.addEventListener("DOMContentLoaded", () => {
  const alreadyToken = localStorage.authToken;
  if (alreadyToken) {
    const decoded = jwt_decode(alreadyToken) as DecodedToken;
    if (isFinite(decoded.exp) && Date.now() > decoded.exp * 1000) {
      redirectAuth();
    } else {
      if (
        browserHistory.location.pathname.includes(AppPage.Authentication) ||
        browserHistory.location.pathname === "/"
      )
        browserHistory.push(
          pathify([AppPage.Workplace, WorkPage.Documents, DocumentPage.List])
        );
    }
  } else {
    redirectAuth();
  }

  store.dispatch(changeIsBlockingLoader(false));
});

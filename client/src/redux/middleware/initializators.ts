import jwt_decode from "jwt-decode";
import { changeIsBlockingLoader } from "../reducers/main";
import { AppPage, DecodedToken } from "../reducers/types";
import { store } from "../store";
import { browserHistory } from "ducks/hooks";

const redirectAuth = () => {
  localStorage.authToken = "";
  browserHistory.push(`/${AppPage.Authentication}`);
};

window.addEventListener("DOMContentLoaded", () => {
  const alreadyToken = localStorage.authToken;
  if (alreadyToken) {
    const decoded = jwt_decode(alreadyToken) as DecodedToken;
    if (isFinite(decoded.exp) && Date.now() > decoded.exp * 1000) {
      redirectAuth();
    } else {
      browserHistory.push(`/${AppPage.Workplace}`);
    }
  } else {
    if (
      !["/", `/${AppPage.Authentication}`].includes(window.location.pathname)
    ) {
      redirectAuth();
    }
  }

  store.dispatch(changeIsBlockingLoader(false));
});

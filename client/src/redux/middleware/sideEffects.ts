import { AnyAction, Middleware } from "@reduxjs/toolkit";
import { browserHistory, Matcher, pathify } from "ducks/hooks";
import { resetDocumentsState } from "ducks/reducers/documents";
import { AppPage, WorkPage } from "ducks/reducers/types";
import { store } from "ducks/store";
import "./initializators";

export const sideEffectsMiddleware: Middleware =
  () => (next) => (action: AnyAction) => {
    // before state change
    switch (action.type) {
      case null:
        break;
    }

    next(action);

    // after state change
    switch (action.type) {
      case null:
        break;
    }
  };

browserHistory.listen((hist) => {
  if (
    hist.location.pathname.match(
      pathify([AppPage.Workplace, WorkPage.Documents], {
        matcher: Matcher.start,
      })
    )
  ) {
    store.dispatch(resetDocumentsState());
  }
});

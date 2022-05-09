import { AnyAction, Middleware } from "@reduxjs/toolkit";
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

import { Matcher, pathify } from "ducks/hooks";
import { CompositionPage } from "ducks/reducers/types";
import React from "react";
import { CompositionsList } from "./List";
import { Route, Routes } from "react-router";
import { CompositionSingle } from "./Single";

export const Compositions: React.FC = () => (
  <Routes>
    <Route
      path={pathify([CompositionPage.List], {
        matcher: Matcher.start,
      })}
      element={<CompositionsList />}
    />
    <Route
      path={pathify([CompositionPage.List, ":compositionName"])}
      element={<CompositionSingle />}
    />
  </Routes>
);

import { Matcher, pathify } from "ducks/hooks";
import { DocumentPage } from "ducks/reducers/types";
import React from "react";
import { DocumentsList } from "./List";
import { DocumentSingle } from "./Single";
import { Route, Routes } from "react-router";

export const Documents: React.FC = () => (
  <Routes>
    <Route
      path={pathify([DocumentPage.List], {
        matcher: Matcher.start,
      })}
      element={<DocumentsList />}
    />
    <Route
      path={pathify([DocumentPage.List, ":docId"])}
      element={<DocumentSingle />}
    />
  </Routes>
);

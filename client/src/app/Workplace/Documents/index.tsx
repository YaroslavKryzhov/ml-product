import { useSESelector } from "ducks/hooks";
import { DocumentPage } from "ducks/reducers/types";
import { always, cond, equals, T } from "ramda";
import React from "react";
import { DocumentsList } from "./List";
import { DocumentSingle } from "./Single";

export const Documents: React.FC = () => {
  const { page } = useSESelector((state) => state.documents);

  return cond<DocumentPage[], JSX.Element>([
    [equals<DocumentPage>(DocumentPage.List), always(<DocumentsList />)],
    [equals<DocumentPage>(DocumentPage.Single), always(<DocumentSingle />)],
    [T, always(<DocumentsList />)],
  ])(page);
};

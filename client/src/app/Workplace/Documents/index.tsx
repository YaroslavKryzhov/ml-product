import { useSESelector } from "ducks/hooks";
import { DocumentPage } from "ducks/reducers/types";
import { always, cond, equals, T } from "ramda";
import React from "react";
import { DocumentsList } from "./List";

export const Documents: React.FC = () => {
  const { page } = useSESelector((state) => state.documents);

  return cond<DocumentPage[], JSX.Element>([
    [equals<DocumentPage>(DocumentPage.List), always(<DocumentsList />)],
    [T, always(<DocumentsList />)],
  ])(page);
};

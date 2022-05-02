import React from "react";
import { always, cond, equals, T } from "ramda";
import { AuthPage } from "ducks/reducers/types";
import { useSESelector } from "ducks/hooks";
import { Auth } from "./Auth";
import { Register } from "./Register";

export const Authentication: React.FC = () => {
  const { page } = useSESelector((state) => state.auth);

  return cond<AuthPage[], JSX.Element>([
    [equals<AuthPage>(AuthPage.auth), always(<Auth />)],
    [equals<AuthPage>(AuthPage.register), always(<Register />)],
    [T, always(<Auth />)],
  ])(page);
};

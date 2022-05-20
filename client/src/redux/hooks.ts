import {
  shallowEqual,
  TypedUseSelectorHook,
  useDispatch,
  useSelector,
} from "react-redux";
import type { RootState, AppDispatch } from "./store";
import { createBrowserHistory } from "history";

// Use throughout your app instead of plain `useDispatch` and `useSelector`
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
export const useSESelector = <T extends unknown>(
  selector: (state: RootState) => T
): T => {
  return useSelector(selector, shallowEqual);
};

export const browserHistory = createBrowserHistory();

export enum Matcher {
  start = "start",
  end = "end",
  contains = "contains",
}

export const pathify = (
  slices: string[],
  opts?: { matcher?: Matcher; relative?: boolean; changeLast?: boolean }
) =>
  (opts && opts.relative ? "." : "") +
  (opts && opts.changeLast ? ".." : "") +
  (opts &&
  opts.matcher &&
  [Matcher.contains, Matcher.end].includes(opts.matcher)
    ? "*/"
    : "/") +
  slices.join("/") +
  (opts &&
  opts.matcher &&
  [Matcher.contains, Matcher.start].includes(opts.matcher)
    ? "/*"
    : "");

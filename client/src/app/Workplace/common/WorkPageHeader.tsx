import { Breadcrumbs, Divider, Typography } from "@mui/material";
import React from "react";
import HomeIcon from "@mui/icons-material/Home";
import { StyledBreadcrumb } from "./styled";
import { pathify } from "ducks/hooks";
import {
  AppPage,
  CompositionPage,
  DocumentPage,
  WorkPage,
} from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { always } from "ramda";
import { useNavigate, useLocation, useParams } from "react-router-dom";
import { EntityHeader } from "./EntityHeader";

const goHome = (navigate: ReturnType<typeof useNavigate>) => {
  navigate(pathify([AppPage.Workplace, WorkPage.Documents, DocumentPage.List]));
};

const goCompositions = (navigate: ReturnType<typeof useNavigate>) => {
  pathify([AppPage.Workplace, WorkPage.Compositions, CompositionPage.List]);
};

const pathItem = (label: () => string, action: () => void) => ({
  label,
  action,
});

const definePathMap = (
  navigate: ReturnType<typeof useNavigate>,
  { docName, compositionName }: { docName?: string; compositionName?: string }
) => ({
  [AppPage.Workplace]: pathItem(always("Домой"), () => goHome(navigate)),
  [WorkPage.Documents]: pathItem(always("Данные"), () => goHome(navigate)),
  [WorkPage.Compositions]: pathItem(always("Композиции"), () =>
    goCompositions(navigate)
  ),
  [CompositionPage.List]: pathItem(always("Все"), () =>
    goCompositions(navigate)
  ),
  [CompositionPage.Single]: pathItem(
    () => compositionName || "",
    () => {
      navigate(
        pathify([
          AppPage.Workplace,
          WorkPage.Compositions,
          CompositionPage.Single,
          compositionName || "",
        ])
      );
    }
  ),
  [CompositionPage.Single]: pathItem(
    () => "New",
    () => {
      navigate(
        pathify([
          AppPage.Workplace,
          WorkPage.Compositions,
          CompositionPage.Create,
        ])
      );
    }
  ),
  [DocumentPage.List]: pathItem(always("Все"), () => goHome(navigate)),
  [DocumentPage.Single]: pathItem(
    () => docName || "",
    () => {
      navigate(
        pathify([
          AppPage.Workplace,
          WorkPage.Documents,
          DocumentPage.List,
          docName || "",
        ])
      );
    }
  ),
});

export const WorkPageHeader: React.FC = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const { docName, compositionName } = useParams();
  const PathMap = definePathMap(navigate, { docName, compositionName });

  const path: (keyof typeof PathMap)[] = pathname
    .split("/")
    .filter((x) => Object.keys(PathMap).includes(x))
    .concat(docName ? DocumentPage.Single : [])
    .concat(compositionName ? CompositionPage.Single : []) as any[];

  return (
    <>
      <Typography sx={{ mb: theme.spacing(1) }} variant="h5">
        {docName && "Данные"}
        {compositionName && "Композиции"}
        {(docName || compositionName) && (
          <EntityHeader initName={docName || compositionName} />
        )}
      </Typography>
      <Breadcrumbs sx={{ mb: theme.spacing(2) }}>
        {path.map((x) => (
          <StyledBreadcrumb
            key={x}
            color="secondary"
            label={PathMap[x]?.label()}
            icon={
              x === AppPage.Workplace ? (
                <HomeIcon fontSize="small" />
              ) : undefined
            }
            onClick={PathMap[x]?.action}
          />
        ))}
      </Breadcrumbs>
      <Divider sx={{ mb: theme.spacing(3) }} />
    </>
  );
};

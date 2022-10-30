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
import { CompositionsEntityHeader } from "../Compositions/CompositionsEntityHeader";
import { DocsEntityHeader } from "../Documents/DocsEntityHeader";

import { first } from "lodash";
import { useAllCompositionsQuery } from "ducks/reducers/api/compositions.api";

const goHome = (navigate: ReturnType<typeof useNavigate>) => {
  navigate(pathify([AppPage.Workplace, WorkPage.Documents, DocumentPage.List]));
};

const goCompositions = (navigate: ReturnType<typeof useNavigate>) => {
  navigate(
    pathify([AppPage.Workplace, WorkPage.Compositions, CompositionPage.List])
  );
};

const pathItem = (label: () => string, action: () => void) => ({
  label,
  action,
});

const definePathMap = (
  navigate: ReturnType<typeof useNavigate>,
  {
    docName,
    compositionName,
    workPage,
  }: { docName?: string; compositionName?: string; workPage?: string }
) => ({
  [AppPage.Workplace]: pathItem(always("Домой"), () => goHome(navigate)),
  [WorkPage.Compositions]: pathItem(always("Композиции"), () =>
    goCompositions(navigate)
  ),
  [WorkPage.Documents]: pathItem(always("Данные"), () => goHome(navigate)),
  ...(workPage === WorkPage.Documents
    ? {
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
      }
    : {
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
        [CompositionPage.Create]: pathItem(
          () => "Новая",
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
      }),
});

export const WorkPageHeader: React.FC = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const { docName, compositionName } = useParams();

  const workPage = first(
    pathname.match(new RegExp(`(?<=${AppPage.Workplace}/)[^/]*`))
  );
  const compositionPage = first(
    pathname.match(
      new RegExp(`(?<=${AppPage.Workplace}/${WorkPage.Compositions}/)[^/]*`)
    )
  );

  const { data: allCompositions } = useAllCompositionsQuery(undefined, {
    skip: compositionPage !== CompositionPage.Create,
  });

  const docPage = first(
    pathname.match(
      new RegExp(`(?<=${AppPage.Workplace}/${WorkPage.Documents}/)[^/]*`)
    )
  );
  const PathMap = definePathMap(navigate, {
    docName,
    compositionName,
    workPage,
  });

  const path: (keyof typeof PathMap)[] = pathname
    .split("/")
    .filter((x) => Object.keys(PathMap).includes(x))
    .concat(docName ? DocumentPage.Single : [])
    .concat(compositionName ? CompositionPage.Single : []) as any[];

  return (
    <>
      <Typography sx={{ mb: theme.spacing(1) }} variant="h5">
        {docPage === DocumentPage.Single && "Данные"}
        {compositionPage === CompositionPage.Single && "Композиции"}
        {docName && (
          <DocsEntityHeader worplacePage={workPage} initName={docName} />
        )}

        {(compositionName || compositionPage === CompositionPage.Create) && (
          <CompositionsEntityHeader
            worplacePage={workPage}
            initName={
              compositionName ||
              `Новая композиция (${allCompositions?.length || 0 + 1})`
            }
          />
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

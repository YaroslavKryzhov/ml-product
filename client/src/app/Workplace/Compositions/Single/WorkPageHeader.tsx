import { Breadcrumbs, Divider, Typography } from "@mui/material";
import React from "react";
import HomeIcon from "@mui/icons-material/Home";
import { StyledBreadcrumb } from "../../common/styled";
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
import { CompositionsEntityHeader } from "../CompositionsEntityHeader";

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

const pathItem = (label: () => string, action?: () => void) => ({
  label,
  action,
});

const definePathMap = (
  navigate: ReturnType<typeof useNavigate>,
  { compositionName }: { compositionName?: string; workPage?: string }
) => ({
  [AppPage.Workplace]: pathItem(always("Домой"), () => goHome(navigate)),
  [WorkPage.Compositions]: pathItem(always("Композиции"), () =>
    goCompositions(navigate)
  ),

  [CompositionPage.List]: pathItem(always("Все"), () =>
    goCompositions(navigate)
  ),
  [CompositionPage.Single]: pathItem(() => compositionName || ""),
  [CompositionPage.Create]: pathItem(() => "Новая"),
});

export const WorkPageHeader: React.FC = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const { compositionId } = useParams();

  const workPage = first(
    pathname.match(new RegExp(`(?<=${AppPage.Workplace}/)[^/]*`))
  );
  const compositionPage = first(
    pathname.match(
      new RegExp(`(?<=${AppPage.Workplace}/${WorkPage.Compositions}/)[^/]*`)
    )
  );

  const { data: allCompositions } = useAllCompositionsQuery();

  const compositionName = allCompositions?.find(
    (x) => x.id === compositionId
  )?.filename;

  const PathMap = definePathMap(navigate, {
    compositionName,
    workPage,
  });

  const path: (keyof typeof PathMap)[] = pathname
    .split("/")
    .filter((x) => Object.keys(PathMap).includes(x))
    .concat(compositionName ? CompositionPage.Single : []) as any[];

  return (
    <>
      <Typography sx={{ mb: theme.spacing(1) }} variant="h5">
        {compositionPage === CompositionPage.Single && "Композиции"}

        {(compositionName || compositionPage === CompositionPage.Create) && (
          <CompositionsEntityHeader
            worplacePage={workPage}
            initName={
              compositionName ||
              `Новая композиция (${(allCompositions?.length || 0) + 1})`
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

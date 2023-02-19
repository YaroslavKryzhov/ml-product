import { Breadcrumbs, Divider, Typography } from "@mui/material";
import React from "react";
import HomeIcon from "@mui/icons-material/Home";
import { pathify } from "ducks/hooks";
import { AppPage, DocumentPage, WorkPage } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { always } from "ramda";
import { useNavigate, useLocation, useParams } from "react-router-dom";

import { first } from "lodash";
import { StyledBreadcrumb } from "app/Workplace/common/styled";
import { DocsEntityHeader } from "../DocsEntityHeader";
import { useInfoDocumentQuery } from "ducks/reducers/api/documents.api";

const goHome = (navigate: ReturnType<typeof useNavigate>) => {
  navigate(pathify([AppPage.Workplace, WorkPage.Documents, DocumentPage.List]));
};

const pathItem = (label: () => string, action: () => void) => ({
  label,
  action,
});

const definePathMap = (
  navigate: ReturnType<typeof useNavigate>,
  { docId, filename }: { docId?: string; filename?: string }
) => ({
  [AppPage.Workplace]: pathItem(always("Домой"), () => goHome(navigate)),
  [WorkPage.Documents]: pathItem(always("Данные"), () => goHome(navigate)),
  [DocumentPage.List]: pathItem(always("Все"), () => goHome(navigate)),
  [DocumentPage.Single]: pathItem(
    () => filename || "",
    () => {
      navigate(
        pathify([
          AppPage.Workplace,
          WorkPage.Documents,
          DocumentPage.List,
          docId || "",
        ])
      );
    }
  ),
});

export const WorkPageHeader: React.FC = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const { docId } = useParams();

  const { data: documentData } = useInfoDocumentQuery(docId!);

  const workPage = first(
    pathname.match(new RegExp(`(?<=${AppPage.Workplace}/)[^/]*`))
  );

  const docPage = first(
    pathname.match(
      new RegExp(`(?<=${AppPage.Workplace}/${WorkPage.Documents}/)[^/]*`)
    )
  );
  const PathMap = definePathMap(navigate, {
    docId,
    filename: documentData?.filename,
  });

  const path: (keyof typeof PathMap)[] = pathname
    .split("/")
    .filter((x) => Object.keys(PathMap).includes(x))
    .concat(docId ? DocumentPage.Single : []) as any[];

  return (
    <>
      <Typography sx={{ mb: theme.spacing(1) }} variant="h5">
        {docPage === DocumentPage.Single && "Данные"}
        {docId && <DocsEntityHeader worplacePage={workPage} docId={docId} />}
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

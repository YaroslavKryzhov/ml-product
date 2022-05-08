import { Breadcrumbs, Divider, Typography } from "@mui/material";
import React from "react";
import HomeIcon from "@mui/icons-material/Home";
import { StyledBreadcrumb } from "./styled";
import { useSESelector } from "ducks/hooks";
import { DocumentPage, WorkPage } from "ducks/reducers/types";
import { changeWorkPage } from "ducks/reducers/main";
import { changeDocumentPage } from "ducks/reducers/documents";
import { theme } from "globalStyle/theme";
import { store } from "ducks/store";
import { always } from "ramda";

const goHome = () => {
  store.dispatch(changeWorkPage(WorkPage.Documents));
  store.dispatch(changeDocumentPage(DocumentPage.List));
};

const pathItem = (label: () => string, action: () => void) => ({
  label,
  action,
});

const PathMap = {
  base: pathItem(always("Домой"), goHome),
  [WorkPage.Documents]: pathItem(always("Документы"), goHome),
  [DocumentPage.List]: pathItem(always("Все"), goHome),
  [DocumentPage.Single]: pathItem(
    () => "ToDO" || "Документ",
    () => {
      store.dispatch(changeWorkPage(WorkPage.Documents));
      store.dispatch(changeDocumentPage(DocumentPage.Single));
    }
  ),
};

export const WorkPageHeader: React.FC = () => {
  const { workPage } = useSESelector((state) => state.main);
  const { page: documentsPage } = useSESelector((state) => state.documents);
  const path: (keyof typeof PathMap)[] = ["base", workPage, DocumentPage.List];

  if (documentsPage === DocumentPage.Single) {
    path.push(DocumentPage.Single);
  }

  return (
    <>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        {documentsPage === DocumentPage.List && "Документы"}
        {documentsPage === DocumentPage.Single && "ToDO"}
      </Typography>
      <Breadcrumbs sx={{ mb: theme.spacing(2) }}>
        {path.map((x) => (
          <StyledBreadcrumb
            key={x}
            color="secondary"
            label={PathMap[x]?.label()}
            icon={x === "base" ? <HomeIcon fontSize="small" /> : undefined}
            onClick={PathMap[x]?.action}
          />
        ))}
      </Breadcrumbs>
      <Divider sx={{ mb: theme.spacing(3) }} />
    </>
  );
};

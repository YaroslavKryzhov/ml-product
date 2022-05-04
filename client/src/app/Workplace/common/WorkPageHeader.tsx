import { Breadcrumbs, Divider, Typography } from "@mui/material";
import React, { useCallback } from "react";
import HomeIcon from "@mui/icons-material/Home";
import { StyledBreadcrumb } from "./styled";
import { useAppDispatch, useSESelector } from "ducks/hooks";
import { DocumentPage, WorkPage } from "ducks/reducers/types";
import { changeWorkPage } from "ducks/reducers/main";
import { changeDocumentPage } from "ducks/reducers/documents";

const pageToHeader = {
  [WorkPage.Documents]: "Документы",
};

const documentsPageToHeader = { [DocumentPage.List]: "Все" };

const subpageToHeader = (workPage: WorkPage, subPage: DocumentPage) => {
  if (workPage === WorkPage.Documents) {
    return documentsPageToHeader[subPage];
  }

  return "";
};

const subpageToListener = (
  dispatch: ReturnType<typeof useAppDispatch>,
  workPage: WorkPage,
  subPage: DocumentPage
) => {
  if (workPage === WorkPage.Documents) {
    if (subPage === DocumentPage.List) {
      return () => {
        dispatch(changeDocumentPage(DocumentPage.List));
      };
    }
  }
};

export const WorkPageHeader: React.FC = () => {
  const { workPage } = useSESelector((state) => state.main);
  const { page: documentsPage } = useSESelector((state) => state.documents);

  const dispatch = useAppDispatch();
  const goHome = useCallback((workPage: WorkPage) => {
    dispatch(changeWorkPage(workPage));
    dispatch(changeDocumentPage(DocumentPage.List));
  }, []);

  return (
    <>
      <Typography sx={{ mb: "10px" }} variant="h5">
        {pageToHeader[workPage]}
      </Typography>
      <Breadcrumbs sx={{ mb: "20px" }}>
        <StyledBreadcrumb
          color="secondary"
          label="Домой"
          icon={<HomeIcon fontSize="small" />}
          onClick={() => goHome(WorkPage.Documents)}
        />
        <StyledBreadcrumb
          color="secondary"
          label={pageToHeader[workPage]}
          onClick={() => goHome(workPage)}
        />
        <StyledBreadcrumb
          color="secondary"
          onClick={subpageToListener(dispatch, workPage, documentsPage)}
          label={subpageToHeader(workPage, documentsPage)}
        />
      </Breadcrumbs>
      <Divider />
    </>
  );
};

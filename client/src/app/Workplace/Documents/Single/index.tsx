import { Box, Stack } from "@mui/material";
import { WorkPageHeader } from "app/Workplace/common/WorkPageHeader";
import { CenteredContainer } from "components/muiOverride";
import { useSESelector } from "ducks/hooks";
import {
  useColumnMarksDocumentQuery,
  useInfoDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { theme } from "globalStyle/theme";
import React from "react";
import { BallTriangle } from "react-loader-spinner";
import { useParams } from "react-router-dom";
import { Categorizer } from "./Categorizer";
import { MainInfo } from "./MainInfo";
import { Pipeline } from "./Pipeline";

export const DocumentSingle: React.FC = () => {
  const { docName } = useParams();
  const { data: docInfo, isLoading: infoLoading } = useInfoDocumentQuery(
    docName!
  );
  const { data: columnMarks, isLoading: marksLoading } =
    useColumnMarksDocumentQuery(docName!);

  return (
    <>
      <WorkPageHeader />
      <Stack sx={{ flexGrow: 1 }}>
        {infoLoading || marksLoading ? (
          <CenteredContainer sx={{ flexGrow: 1 }}>
            <BallTriangle
              color={theme.palette.primary.main}
              width={theme.typography.h1.fontSize}
              height={theme.typography.h1.fontSize}
            />
          </CenteredContainer>
        ) : (
          <>
            {docName && <MainInfo docName={docName} />}
            {!!docInfo?.pipeline?.length && (
              <Pipeline steps={docInfo.pipeline} />
            )}
            {columnMarks && <Categorizer />}
          </>
        )}
      </Stack>
    </>
  );
};

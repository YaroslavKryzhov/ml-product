import { Box } from "@mui/material";
import { WorkPageHeader } from "app/Workplace/common/WorkPageHeader";
import { useSESelector } from "ducks/hooks";
import { useInfoDocumentQuery } from "ducks/reducers/api/documents.api";
import { theme } from "globalStyle/theme";
import React from "react";
import { BallTriangle } from "react-loader-spinner";
import { useParams } from "react-router-dom";

export const DocumentSingle: React.FC = () => {
  // const { data: docInfo, isLoading: infoLoading } = useInfoDocumentQuery();

  console.log(useParams());

  return (
    <>
      <WorkPageHeader />
      <Box>
        {/* {infoLoading ? (
        <BallTriangle
          color={theme.palette.primary.main}
          width={theme.typography.h1.fontSize}
          height={theme.typography.h1.fontSize}
        />
      ) : null} */}
      </Box>
    </>
  );
};

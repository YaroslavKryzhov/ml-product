import { Box } from "@mui/material";
import { useSESelector } from "ducks/hooks";
import { useInfoDocumentQuery } from "ducks/reducers/api/documents.api";
import { theme } from "globalStyle/theme";
import React from "react";
import { BallTriangle } from "react-loader-spinner";

export const DocumentSingle: React.FC = () => {
  // const { data: docInfo, isLoading: infoLoading } = useInfoDocumentQuery();

  return (
    <Box>
      {/* {infoLoading ? (
        <BallTriangle
          color={theme.palette.primary.main}
          width={theme.typography.h1.fontSize}
          height={theme.typography.h1.fontSize}
        />
      ) : null} */}
    </Box>
  );
};

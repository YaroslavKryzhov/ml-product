import { Box, Divider, Typography } from "@mui/material";
import { InfoChip } from "components/infoChip";
import { useInfoDocumentQuery } from "ducks/reducers/api/documents.api";
import { theme } from "globalStyle/theme";
import moment from "moment";
import React from "react";

export const MainInfo: React.FC<{ docName: string }> = ({ docName }) => {
  const { data } = useInfoDocumentQuery(docName);

  if (!data) return null;

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Основное
      </Typography>
      <Box
        sx={{
          display: "flex",
          justifyContent: "flex-start",
          gap: theme.spacing(2),
        }}
      >
        <InfoChip
          label="Загружено"
          info={moment(data.upload_date).format(theme.additional.timeFormat)}
        />
        <InfoChip
          label="Изменено"
          info={moment(data.change_date).format(theme.additional.timeFormat)}
        />
      </Box>
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

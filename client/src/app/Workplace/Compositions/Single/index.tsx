import { Stack } from "@mui/material";
import { WorkPageHeader } from "app/Workplace/common/WorkPageHeader";
import React from "react";

export const CompositionSingle: React.FC<{ createMode?: boolean }> = ({
  createMode,
}) => {
  return (
    <>
      <WorkPageHeader />
      <Stack sx={{ flexGrow: 1 }}></Stack>
    </>
  );
};

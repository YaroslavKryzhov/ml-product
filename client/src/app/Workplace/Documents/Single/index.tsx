import { Stack } from "@mui/material";
import { WorkPageHeader } from "app/Workplace/common/WorkPageHeader";
import React from "react";
import { Markup } from "./Markup";
import { DocumentMethods } from "./DocumentMethods";
import { MainInfo } from "./MainInfo";
import { Pipeline } from "./Pipeline";

export const DocumentSingle: React.FC = () => {
  return (
    <>
      <WorkPageHeader />
      <Stack sx={{ flexGrow: 1 }}>
        <Markup />
        <MainInfo />
        <Pipeline />
        <DocumentMethods />
      </Stack>
    </>
  );
};

import { Stack } from "@mui/material";
import React from "react";
import { Markup } from "./Markup";
import { DocumentMethods } from "./DocumentMethods";
import { MainInfo } from "./MainInfo";
import { Pipeline } from "./Pipeline";
import { WorkPageHeader } from "./WorkPageHeader";

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

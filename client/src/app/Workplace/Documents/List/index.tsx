import { Box } from "@mui/material";
import { nanoid } from "@reduxjs/toolkit";
import { MenuContext } from "app/Workplace";
import { TableFix } from "app/Workplace/common/Table";
import { useAllDocumentsQuery } from "ducks/reducers/api/documents.api";
import { theme } from "globalStyle/theme";
import React, { useContext, useEffect, useState } from "react";

const columns = [
  {
    Header: "Название",
    accessor: "name",
  },
  {
    Header: "Загружено",
    accessor: "upload_date",
  },
  {
    Header: "Изменено",
    accessor: "change_date",
  },
];

export const DocumentsList: React.FC = () => {
  const { data: allDocuments } = useAllDocumentsQuery();
  const { menuOpened } = useContext(MenuContext);
  const [forceResize, setForceResize] = useState("");

  useEffect(() => {
    const interval = setInterval(() => setForceResize(nanoid()), 0);

    setTimeout(
      () => clearInterval(interval),
      theme.transitions.duration.complex
    );

    return () => clearInterval(interval);
  }, [menuOpened]);

  console.log(allDocuments);

  return (
    <Box>
      <TableFix
        forceResize={forceResize}
        resizable
        data={allDocuments || []}
        columns={columns}
        sortBy={[
          { id: columns[2].accessor, desc: true },
          { id: columns[0].accessor, desc: true },
          { id: columns[1].accessor, desc: true },
        ]}
      />
    </Box>
  );
};

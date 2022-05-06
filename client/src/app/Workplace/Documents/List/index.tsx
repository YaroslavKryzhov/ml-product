import { Box, Button } from "@mui/material";
import { nanoid } from "@reduxjs/toolkit";
import { MenuContext } from "app/Workplace";
import { TableFix } from "app/Workplace/common/Table";
import { useAppDispatch } from "ducks/hooks";
import { useAllDocumentsQuery } from "ducks/reducers/api/documents.api";
import { setDialog } from "ducks/reducers/dialog";
import { theme } from "globalStyle/theme";
import React, { useContext, useEffect, useState } from "react";
import { DocumentDrop } from "./DropFileDialog";

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
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const dispatch = useAppDispatch();

  useEffect(() => {
    const interval = setInterval(() => setForceResize(nanoid()), 0);

    setTimeout(
      () => clearInterval(interval),
      theme.transitions.duration.complex
    );

    return () => clearInterval(interval);
  }, [menuOpened]);

  return (
    <Box>
      <Button
        onClick={() =>
          dispatch(
            setDialog({
              title: "Загрузка файла",
              Content: <DocumentDrop onFile={setSelectedFile} />,
              onAccept: () => {},
              onDismiss: () => setSelectedFile(null),
              acceptText: "Загрузить",
              dismissText: "Отменить",
            })
          )
        }
        variant="contained"
        fullWidth
        sx={{ mb: theme.spacing(2) }}
      >
        Загрузить CSV
      </Button>
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

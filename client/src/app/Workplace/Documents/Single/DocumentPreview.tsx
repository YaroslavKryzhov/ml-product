import { TableFix } from "app/Workplace/common/Table";
import { useDocumentQuery } from "ducks/reducers/api/documents.api";
import React, { useMemo } from "react";
import { zipObject, unzip } from "lodash";
import { FullDocument } from "ducks/reducers/types";
import { BallTriangle } from "react-loader-spinner";
import { theme } from "globalStyle/theme";
import { CenteredContainer } from "components/muiOverride";

const convertData = (data: FullDocument) =>
  unzip(Object.values(data).map((x) => Object.values(x as any))).map((zipArr) =>
    zipObject(Object.keys(data), zipArr)
  );

export const DocumentPreview: React.FC<{ docName: string }> = ({ docName }) => {
  const { data, isLoading } = useDocumentQuery(docName!);
  const convertedData = useMemo(() => (data ? convertData(data) : []), [data]);
  const columns = useMemo(
    () =>
      data ? Object.keys(data).map((x) => ({ accessor: x, Header: x })) : [],
    [data]
  );

  if (isLoading)
    return (
      <CenteredContainer sx={{ width: "100vw", height: "calc(100vh - 200px)" }}>
        <BallTriangle
          color={theme.palette.primary.main}
          width={theme.typography.h1.fontSize}
          height={theme.typography.h1.fontSize}
        />
      </CenteredContainer>
    );

  return (
    <TableFix
      defaultColumnSizing={{ minWidth: 70 }}
      forceResize
      resizable
      data={convertedData}
      columns={columns}
    />
  );
};

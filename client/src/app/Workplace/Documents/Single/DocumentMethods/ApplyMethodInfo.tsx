import * as React from "react";
import Typography from "@mui/material/Typography";
import { Box, Paper } from "@mui/material";
import { theme } from "globalStyle/theme";
import { CategoryMark, DocumentMethod } from "ducks/reducers/types";
import { useInfoDocumentQuery } from "ducks/reducers/api/documents.api";
import { always, cond, equals, T } from "ramda";
import { useDocumentNameForce } from "../../hooks";
import { OverflowText } from "components/styles";
import { ElementWithTooltip } from "components/ElementWithTooltip";

const ColumnsTransformInfo: React.FC<{
  type: CategoryMark;
  gapsAnnounce?: boolean;
}> = ({ type, gapsAnnounce }) => {
  const docName = useDocumentNameForce();
  const { data: infoData } = useInfoDocumentQuery(docName!);
  const colNames: string[] | null =
    infoData?.column_types && Array.isArray(infoData?.column_types[type])
      ? (infoData?.column_types[type] as string[])
      : null;

  return (
    <Box sx={{ textAlign: "center" }}>
      {colNames?.length ? (
        <>
          <Typography
            variant="body1"
            sx={{ mb: gapsAnnounce ? 0 : theme.spacing(2) }}
          >
            Метод будет применен только к <b>{type}</b> признакам.
          </Typography>
          {gapsAnnounce && (
            <Typography variant="body1" sx={{ mb: theme.spacing(2) }}>
              Eсли в данных есть пропуски, они будут заполнены{" "}
              <b>mean/median</b> методом.
            </Typography>
          )}

          <Box
            sx={{
              width: "600px",
              display: "flex",
              flexWrap: "wrap",
              justifyContent: "center",
              gap: `${theme.spacing(2)} ${theme.spacing(4)}`,
              padding: `${theme.spacing(2)} 0 ${theme.spacing(2)} 0`,
            }}
          >
            {colNames.map((x) => (
              <Paper
                key={x}
                sx={{
                  padding: `${theme.spacing(1)} ${theme.spacing(2)}`,
                  width: "150px",
                  ...OverflowText,
                }}
              >
                <ElementWithTooltip width={118} title={x}>
                  {x}
                </ElementWithTooltip>
              </Paper>
            ))}
          </Box>
        </>
      ) : (
        <Box>
          <Typography variant="body1">
            Не найдено признаков, на которые может повлиять данный метод.
          </Typography>
          <Typography variant="body1">
            Вы действительно хотите попытаться его применить?
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export const ApplyMethodInfo: React.FC<{ method: DocumentMethod }> = ({
  method,
}) => {
  return cond<DocumentMethod[], JSX.Element | null>([
    [
      equals<DocumentMethod>(DocumentMethod.standardize_features),
      always(<ColumnsTransformInfo type={CategoryMark.numeric} />),
    ],
    [
      (x) =>
        [
          DocumentMethod.outliersIsolationForest,
          DocumentMethod.outliersEllipticEnvelope,
          DocumentMethod.outliersLocalFactor,
          DocumentMethod.outliersOneClassSvm,
        ].includes(x),
      always(<ColumnsTransformInfo type={CategoryMark.numeric} gapsAnnounce />),
    ],
    [
      (x) =>
        [
          DocumentMethod.oneHotEncoding,
          DocumentMethod.ordinalEncoding,
        ].includes(x),
      always(<ColumnsTransformInfo type={CategoryMark.categorical} />),
    ],
    [
      T,
      always(
        <Typography variant="body1">
          Вы действительно хотите применить метод <b>{method}</b>?`
        </Typography>
      ),
    ],
  ])(method);
};

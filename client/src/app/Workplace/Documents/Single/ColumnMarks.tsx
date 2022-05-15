import { LoadingButton } from "@mui/lab";
import { Box, Divider, Snackbar, Typography } from "@mui/material";
import { Categorizer, Distribution } from "app/Workplace/common/Categorizer";
import { SlideTr } from "app/Workplace/common/styled";
import {
  useChangeColumnMarksMutation,
  useColumnMarksDocumentQuery,
  useColumnsDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { CategoryMark } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { first, omit } from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const categories = [
  { value: CategoryMark.categorical, label: "Категориальные" },
  { value: CategoryMark.target, label: "Целевой", singleCapacity: true },
  { value: CategoryMark.numeric, label: "Числовые" },
];

export const ColumnMarks: React.FC = () => {
  const [marksDistribution, setMarksDistribution] = useState<Distribution>({
    heap: [],
    [CategoryMark.categorical]: [],
    [CategoryMark.target]: [],
    [CategoryMark.numeric]: [],
  });
  const { docName } = useParams();
  const { data: columnMarks } = useColumnMarksDocumentQuery(docName!);
  const { data: columns } = useColumnsDocumentQuery(docName!);
  const [saveColumnMarks, { isLoading: isSaveLoading, isError, isSuccess }] =
    useChangeColumnMarksMutation();

  const [noticeShowed, setNoticeShowed] = useState(false);

  useEffect(() => {
    if (!(columnMarks && columns)) return;

    const usedMarks = Object.values(columnMarks)
      .map((x) => (Array.isArray(x) ? x : [x]))
      .flat();

    const heap = columns.filter((x) => !usedMarks.includes(x));

    setMarksDistribution({
      heap,
      categorical: columnMarks.categorical || [],
      numeric: columnMarks.numeric || [],
      target: columnMarks.target ? [columnMarks.target] : [],
    });
  }, [JSON.stringify(columns), JSON.stringify(columnMarks)]);

  const onSave = useCallback(
    () =>
      saveColumnMarks({
        body: {
          ...(omit(marksDistribution, "heap") as any),
          target: first(marksDistribution[CategoryMark.target]) || "",
        },
        filename: docName!,
      }).then(() => setNoticeShowed(true)),
    [marksDistribution, docName]
  );

  if (!columnMarks) return null;

  return (
    <Box sx={{ position: "relative" }}>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Категоризация колонок
      </Typography>

      <Categorizer
        heap={{ label: "Нераспределенные метки", value: "heap" }}
        categories={categories}
        distribution={marksDistribution}
        distributionChange={setMarksDistribution}
      />

      <Snackbar
        autoHideDuration={3000}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
        open={noticeShowed}
        onClose={() => setNoticeShowed(false)}
        message={
          <Typography
            variant="body2"
            sx={{
              color: isError
                ? theme.palette.error.main
                : theme.palette.success.main,
            }}
          >
            {isError && "Ошибка сохранения"}
            {isSuccess && "Успешно сохранено"}
          </Typography>
        }
        TransitionComponent={SlideTr}
      />

      <LoadingButton
        loading={isSaveLoading}
        onClick={onSave}
        variant="contained"
        sx={{
          bottom: "52px",
          height: "min-content",
          width: "300px",
          position: "absolute",
        }}
      >
        Сохранить
      </LoadingButton>
      <Divider sx={{ mb: theme.spacing(3), mt: theme.spacing(3) }} />
    </Box>
  );
};

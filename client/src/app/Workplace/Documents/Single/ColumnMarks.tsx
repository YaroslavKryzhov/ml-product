import { Box, Typography } from "@mui/material";
import { Categorizer, Distribution } from "app/Workplace/common/Categorizer";
import {
  useColumnMarksDocumentQuery,
  useColumnsDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { CategoryMark } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import React, { useEffect, useState } from "react";
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
  const { data: columnMarks, isLoading: marksLoading } =
    useColumnMarksDocumentQuery(docName!);
  const { data: columns, isLoading: columnsLoading } = useColumnsDocumentQuery(
    docName!
  );

  useEffect(() => {
    if (!(columnMarks && columns)) return;

    const usedMarks = Object.values(columnMarks)
      .map((x) => (Array.isArray(x) ? x : [x]))
      .flat();

    const heap = columns.filter((x) => !usedMarks.includes(x));

    setMarksDistribution({
      heap,
      ...columnMarks,
      target: columnMarks.target ? [columnMarks.target] : [],
    });
  }, [JSON.stringify(columns), JSON.stringify(columnMarks)]);

  if (!columnMarks) return null;

  return (
    <Box>
      <Typography sx={{ mb: theme.spacing(2) }} variant="h5">
        Категоризация колонок
      </Typography>
      <Categorizer
        heap={{ label: "Нераспределенные метки", value: "heap" }}
        categories={categories}
        distribution={marksDistribution}
        distributionChange={setMarksDistribution}
      />
    </Box>
  );
};

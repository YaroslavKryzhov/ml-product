import React, { useCallback } from "react";
import { CategoryMark, DFInfo, ErrorResponse } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import {
  Box,
  ToggleButton,
  ToggleButtonGroup,
  Tooltip,
  Typography,
} from "@mui/material";
import { StatsGraph } from "./statGraph";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import { useAppDispatch } from "ducks/hooks";
import { T } from "ramda";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import { SIMPLE_HEIGHT } from "./contants";
import { OverflowText } from "app/Workplace/common/styles";
import { MoreColumnInfo } from "./MoreColumnInfo";
import {
  useMarkAsCategoricalMutation,
  useMarkAsNumericMutation,
} from "ducks/reducers/api/documents.api";
import { useParams } from "react-router-dom";
import Filter1Icon from "@mui/icons-material/Filter1";
import TextFormatIcon from "@mui/icons-material/TextFormat";
import DeleteIcon from "@mui/icons-material/Delete";
import { SnackBarType, useNotice } from "app/Workplace/common/useNotice";

const DataHeaderCaption: React.FC<{
  children: React.ReactNode;
  important?: boolean;
}> = (props) => (
  <Typography
    sx={{
      display: "block",
      lineHeight: theme.typography.body1.fontSize,
      color: props.important
        ? theme.palette.info.dark
        : theme.palette.primary.light,
    }}
    variant={props.important ? "body2" : "caption"}
  >
    {props.children}
  </Typography>
);

export const HeaderCell: React.FC<DFInfo & { right?: boolean }> = ({
  type,
  data,
  name,
  not_null_count,
  data_type,
  right,
}) => {
  const { docName } = useParams();
  const dispatch = useAppDispatch();
  const [markAsCategorical] = useMarkAsCategoricalMutation();
  const [markAsNumeric] = useMarkAsNumericMutation();

  const showColumnError = useNotice({
    label: " Не удалось изменить тип колонки",
    type: SnackBarType.error,
  });

  const setDialogProps = useCallback(() => {
    data &&
      dispatch(
        setDialog({
          title: `Подробности о ${name}`,
          Content: (
            <MoreColumnInfo
              type={type}
              data={data}
              name={name}
              not_null_count={not_null_count}
              data_type={data_type}
            />
          ),
          onDismiss: T,
          dismissText: "Закрыть",
        })
      );
  }, [data, type, name, data_type, not_null_count, type]);

  const markChange = useCallback(
    (newMark: CategoryMark) => {
      console.log(1212);
      dispatch(
        setDialog({
          title: "Изменение типа колонки",
          text: `Вы действительно хотите изменить тип ${name} на ${newMark}?`,
          onAccept: async () => {
            dispatch(setDialogLoading(true));

            let res: any = null;

            try {
              if (newMark === CategoryMark.categorical)
                res = await markAsCategorical({
                  filename: docName!,
                  columnName: name,
                });

              if (newMark === CategoryMark.numeric) {
                res = await markAsNumeric({
                  filename: docName!,
                  columnName: name,
                });
              }
              if ((res.data as ErrorResponse)?.status_code === 409)
                throw new Error();
            } catch {
              showColumnError(true);
            }

            dispatch(setDialogLoading(false));
          },
          onDismiss: T,
        })
      );
    },
    [docName]
  );

  const onCategoryChange = useCallback(
    (_: unknown, val: CategoryMark) => val && markChange(val),
    [markChange]
  );

  return (
    <Box
      sx={{
        flexGrow: 1,
        padding: theme.spacing(1),
        overflow: "hidden",
        textAlign: right ? "right" : "left",
        cursor: "pointer",
        "&:hover": {
          background: theme.palette.info.light,
        },
      }}
    >
      <Box
        sx={{
          display: "flex",
          ...OverflowText,
          justifyContent: right ? "flex-end" : "flex-start",
        }}
      >
        <Tooltip followCursor title={name}>
          <Box sx={{ ...OverflowText }}>{name}</Box>
        </Tooltip>
      </Box>
      <Box
        sx={{
          mb: theme.spacing(1),
          mt: theme.spacing(1),
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        {data && (
          <ToggleButton value="size" sx={{ p: "2px" }}>
            <OpenInFullIcon
              onClick={setDialogProps}
              sx={{
                fontSize: theme.typography.caption.fontSize,
              }}
            />
          </ToggleButton>
        )}

        <ToggleButtonGroup
          exclusive
          value={type}
          onChange={onCategoryChange}
          onClick={(e) => e.stopPropagation()}
        >
          <ToggleButton sx={{ p: "2px" }} value={CategoryMark.numeric}>
            <Filter1Icon sx={{ fontSize: theme.typography.caption.fontSize }} />
          </ToggleButton>
          <ToggleButton sx={{ p: "2px" }} value={CategoryMark.categorical}>
            <TextFormatIcon
              sx={{ fontSize: theme.typography.caption.fontSize }}
            />
          </ToggleButton>
        </ToggleButtonGroup>

        <ToggleButton value="delete" sx={{ p: "2px" }}>
          <DeleteIcon
            sx={{
              fontSize: theme.typography.caption.fontSize,
            }}
          />
        </ToggleButton>
      </Box>

      {type && <DataHeaderCaption important>Type: {type}</DataHeaderCaption>}

      <DataHeaderCaption>Not Null: {not_null_count}</DataHeaderCaption>
      <DataHeaderCaption>DataType: {data_type}</DataHeaderCaption>
      {data && (
        <Box sx={{ height: SIMPLE_HEIGHT }}>
          <Box
            sx={{
              display: "flex",
              position: "absolute",
              justifyContent: right ? "flex-end" : "flex-start",
            }}
          >
            <StatsGraph isSimple data={data} type={type} />
          </Box>
        </Box>
      )}
    </Box>
  );
};

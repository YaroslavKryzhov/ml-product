import React, { useCallback } from "react";
import { CategoryMark, DFInfo } from "ducks/reducers/types";
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
  useDeleteColumnMutation,
  useInfoDocumentQuery,
} from "ducks/reducers/api/documents.api";
import { useParams } from "react-router-dom";
import Filter1Icon from "@mui/icons-material/Filter1";
import TextFormatIcon from "@mui/icons-material/TextFormat";
import DeleteIcon from "@mui/icons-material/Delete";
import { useChangeColumnType } from "./useChangeColumnType";

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

  const { data: infoDocument } = useInfoDocumentQuery(docName!);
  const [deleteColumn] = useDeleteColumnMutation();

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
  }, [data, name, data_type, not_null_count, type, dispatch]);

  const setDialogDeleteProps = useCallback(() => {
    dispatch(
      setDialog({
        title: `Удаление ${name}`,
        text: `Вы действительно хотите удалить колонку ${name}?`,
        onAccept: async () => {
          dispatch(setDialogLoading(true));
          await deleteColumn({ filename: docName!, columnName: name });

          dispatch(setDialogLoading(false));
        },
        onDismiss: T,
      })
    );
  }, [name, dispatch, deleteColumn, docName]);

  const markChange = useChangeColumnType(name);

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
        <ToggleButton value="size" sx={{ p: "2px" }}>
          <OpenInFullIcon
            onClick={setDialogProps}
            sx={{
              fontSize: theme.typography.caption.fontSize,
            }}
          />
        </ToggleButton>

        <Tooltip
          disableHoverListener={!!infoDocument?.column_types?.target}
          followCursor
          title="Доступно только после разметки"
        >
          <ToggleButtonGroup
            disabled={!infoDocument?.column_types?.target}
            exclusive
            value={type}
            onChange={(_: unknown, val: CategoryMark) => val && markChange(val)}
          >
            <ToggleButton sx={{ p: "2px" }} value={CategoryMark.numeric}>
              <Filter1Icon
                sx={{ fontSize: theme.typography.caption.fontSize }}
              />
            </ToggleButton>
            <ToggleButton sx={{ p: "2px" }} value={CategoryMark.categorical}>
              <TextFormatIcon
                sx={{ fontSize: theme.typography.caption.fontSize }}
              />
            </ToggleButton>
          </ToggleButtonGroup>
        </Tooltip>

        <ToggleButton value="delete" sx={{ p: "2px" }}>
          <DeleteIcon
            onClick={setDialogDeleteProps}
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

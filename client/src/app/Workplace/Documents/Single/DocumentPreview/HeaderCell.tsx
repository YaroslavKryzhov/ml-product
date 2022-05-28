import React, { useCallback } from "react";
import { DFInfo } from "ducks/reducers/types";
import { theme } from "globalStyle/theme";
import { Box, Tooltip, Typography } from "@mui/material";
import { StatsGraph } from "./statGraph";
import OpenInFullIcon from "@mui/icons-material/OpenInFull";
import { useAppDispatch } from "ducks/hooks";
import { T } from "ramda";
import { setDialog } from "ducks/reducers/dialog";
import { SIMPLE_HEIGHT } from "./contants";
import { OverflowText } from "app/Workplace/common/styles";
import { MoreColumnInfo } from "./MoreColumnInfo";

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
  const dispatch = useAppDispatch();
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

  return (
    <Box
      onClick={setDialogProps}
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
          mb: theme.spacing(1),
          display: "flex",
          ...OverflowText,
          justifyContent: right ? "flex-end" : "flex-start",
        }}
      >
        <Tooltip followCursor title={name}>
          <Box sx={{ ...OverflowText }}>{name}</Box>
        </Tooltip>

        {data && (
          <OpenInFullIcon
            sx={{
              ml: theme.spacing(1),
              mt: "7px",
              fontSize: theme.typography.caption.fontSize,
            }}
          />
        )}
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

import { useCallback } from "react";
import { CategoryMark, StandardResponseData } from "ducks/reducers/types";
import { useAppDispatch } from "ducks/hooks";
import { T } from "ramda";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import {
  useMarkAsCategoricalMutation,
  useMarkAsNumericMutation,
} from "ducks/reducers/api/documents.api";
import { useParams } from "react-router-dom";
import { addNotice, SnackBarType } from "ducks/reducers/notices";

export const useChangeColumnType = (columnName: string) => {
  const dispatch = useAppDispatch();
  const { docName } = useParams();

  const [markAsCategorical] = useMarkAsCategoricalMutation();
  const [markAsNumeric] = useMarkAsNumericMutation();

  return useCallback(
    (newMark: CategoryMark) => {
      dispatch(
        setDialog({
          title: "Изменение типа колонки",
          text: `Вы действительно хотите изменить тип ${columnName} на ${newMark}?`,
          onAccept: async () => {
            dispatch(setDialogLoading(true));

            let res: any = null;

            if (newMark === CategoryMark.categorical)
              res = (await markAsCategorical({
                filename: docName!,
                columnName,
              })) as StandardResponseData;

            if (newMark === CategoryMark.numeric) {
              res = (await markAsNumeric({
                filename: docName!,
                columnName,
              })) as StandardResponseData;
            }
            if (res.data?.status_code === 409 || res.error)
              dispatch(
                addNotice({
                  label: "Не удалось изменить тип колонки",
                  type: SnackBarType.error,
                  id: Date.now(),
                })
              );
            if (res.data?.status_code === 200)
              dispatch(
                addNotice({
                  label: "Тип колонки успешно изменен",
                  type: SnackBarType.success,
                  id: Date.now(),
                })
              );

            dispatch(setDialogLoading(false));
          },
          onDismiss: T,
        })
      );
    },
    [docName, columnName, dispatch, markAsCategorical, markAsNumeric]
  );
};

import { CategoryMark } from "ducks/reducers/types";
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
  const { docId } = useParams();

  const [markAsCategorical] = useMarkAsCategoricalMutation();
  const [markAsNumeric] = useMarkAsNumericMutation();

  return (newMark: CategoryMark) => {
    dispatch(
      setDialog({
        title: "Изменение типа колонки",
        text: `Вы действительно хотите изменить тип ${columnName} на ${newMark}?`,
        onAccept: async () => {
          dispatch(setDialogLoading(true));

          let res: any = null;

          if (newMark === CategoryMark.categorical)
            res = await markAsCategorical({
              dataframe_id: docId!,
              column_name: columnName,
            });

          if (newMark === CategoryMark.numeric) {
            res = await markAsNumeric({
              dataframe_id: docId!,
              column_name: columnName,
            });
          }
          console.log(res);
          if (res.data?.status_code === 409)
            dispatch(
              addNotice({
                label: "Не удалось изменить тип колонки",
                type: SnackBarType.error,
                id: Date.now(),
              })
            );
          if (
            res.data?.status_code === 200 ||
            res?.error?.originalStatus === 200
          )
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
  };
};

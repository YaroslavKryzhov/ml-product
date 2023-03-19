import { pathify, useAppDispatch } from "ducks/hooks";
import { useDeleteCompositionMutation } from "ducks/reducers/api/compositions.api";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import { AppPage, DocumentPage, WorkPage } from "ducks/reducers/types";
import { T } from "ramda";
import { useNavigate } from "react-router-dom";

export const useDeleteComposition = (options?: { redirectAfter?: boolean }) => {
  const navigate = useNavigate();
  const [deleteComp] = useDeleteCompositionMutation();
  const dispatch = useAppDispatch();

  return (name: string, id: string) =>
    dispatch(
      setDialog({
        title: "Удаление",
        text: `Вы действительно хотите удалить композицию ${name}?`,
        onAccept: async () => {
          dispatch(setDialogLoading(true));
          await deleteComp({ model_id: id });
          dispatch(setDialogLoading(false));
          if (options?.redirectAfter) {
            navigate(
              pathify([
                AppPage.Workplace,
                WorkPage.Compositions,
                DocumentPage.List,
              ])
            );
          }
        },
        onDismiss: T,
      })
    );
};

import { pathify, useAppDispatch } from "ducks/hooks";
import { useDeleteDocumentMutation } from "ducks/reducers/api/documents.api";
import { setDialog, setDialogLoading } from "ducks/reducers/dialog";
import { AppPage, DocumentPage, WorkPage } from "ducks/reducers/types";
import { first } from "lodash";
import { T } from "ramda";
import { useNavigate } from "react-router-dom";

export const useDeleteFile = (options?: { redirectAfter?: boolean }) => {
  const navigate = useNavigate();
  const [deleteDoc] = useDeleteDocumentMutation();
  const dispatch = useAppDispatch();

  return (name: string) =>
    dispatch(
      setDialog({
        title: "Удаление",
        text: `Вы действительно хотите удалить файл ${name}?`,
        onAccept: async () => {
          dispatch(setDialogLoading(true));
          await deleteDoc(name);
          dispatch(setDialogLoading(false));
          if (options?.redirectAfter) {
            navigate(
              pathify([
                AppPage.Workplace,
                WorkPage.Documents,
                DocumentPage.List,
              ])
            );
          }
        },
        onDismiss: T,
      })
    );
};

export const useDocumentNameForce = (): string | null =>
  first(window.location.pathname.match(/(?<=documents\/list\/).*$/g)) || null;

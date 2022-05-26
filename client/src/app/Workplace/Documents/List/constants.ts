import { TaskType } from "ducks/reducers/types";

export const TASK_TYPE_LABEL = {
  [TaskType.regression]: "Регрессия",
  [TaskType.classification]: "Классификация",
};

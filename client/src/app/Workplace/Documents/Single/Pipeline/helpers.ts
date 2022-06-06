import { compose, flatten, map, prop, values, zipObj } from "ramda";
import { ButtonsData } from "../DocumentMethods/constants";
import { DocumentMethod, PipelineUnit } from "ducks/reducers/types";

export const PipelineGroups = {
  ...ButtonsData,
  more: [{ label: "Удаление колонки", value: DocumentMethod.dropСolumn }],
};

export const mapPath = (key: string) =>
  (compose as any)(map(prop(key)), flatten, values)(PipelineGroups);

export const PipelineLabels = zipObj(mapPath("value"), mapPath("label"));

export const BuildLabel = (unit: PipelineUnit) =>
  `${PipelineLabels[unit.function_name]} ${
    unit.param ? `(${unit.param})` : ""
  }`;

import { useSelector } from "@/redux/hooks";
import { IModel } from "@/utils/types";
import { VStack, Text, Checkbox, useToast, Select, HStack } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { DefaultButton } from "@/components/Common";
import { api, errToast, genHash, successToast } from "@/utils/misc";

export function ComposeCreateModal({ onClose }: { onClose: any }) {
    const toast = useToast();
    const { Authorization } = useSelector(({ misc }) => misc);
    const { modelsList } = useSelector(({ dataframe }) => dataframe);
    const [checked, setChecked] = useState<IModel[]>([]);
    const [types, setTypes] = useState<string[]>([]);

    useEffect(() => {
        api.get('/model/specs/composition_types').then(res => setTypes(res.data));
    }, []);

    return <VStack align='start' py='20px' spacing='30px'>
        <Text fontSize='24px' fontWeight={600}>Новая композиция</Text>
        <Text fontSize='18px'>Выберите модели для объединения в композицию</Text>

        <HStack w='100%' justify='space-between' align='start' px='20%'>
            {Array.from(new Set(modelsList.map((model: IModel) => model.task_type)))
                .map((taskType: string) => modelsList.filter((model: IModel) => model.task_type === taskType))
                .filter((modelsChunk: IModel[]) => modelsChunk.length > 0)
                .map((modelsChunk: IModel[], i: number) =>
                    <VStack key={i} spacing='8px' align='start'>
                        <Text fontSize='24px' fontWeight={600} mb='4px'>{modelsChunk[0].task_type}</Text>

                        {modelsChunk.map((model: IModel, j: number) => <Checkbox key={j} isDisabled={checked.length > 0 && checked[0].task_type !== model.task_type} isChecked={checked.findIndex((mx: IModel) => mx._id === model._id) > -1} onChange={(e: any) => {
                            if (e.target.checked) setChecked(s => [...s, model]);
                            else setChecked(s => s.filter((xs: IModel) => xs._id !== model._id));
                        }}>{model.filename}</Checkbox>)}
                    </VStack>)}
        </HStack>

        {checked.length > 0 && <>
            <Text fontSize='18px' fontWeight={600} mb='-18px'>Тип композиции</Text>
            <Select w='50%' id='composeTypeSelect'>
                {types
                    .filter((type: string) => checked[0].task_type === 'classification'
                        ? type.includes('Class')
                        : type.includes('Regr'))
                    .map((type: string, i: number) => <option key={i} value={type}>{type}</option>)}
            </Select>
        </>}

        <DefaultButton onClick={() => {
            const theType = document.getElementById('composeTypeSelect');

            api.post(
                '/model/processing/build_composition?composition_name=' + `composed_${genHash(6)}`,
                {
                    model_ids: checked.map((model: IModel) => model._id),
                    composition_params: {
                        model_type: (theType as HTMLSelectElement).value,
                        params: {}
                    }
                },
                { headers: { Authorization } }
            )
                .then(res => {
                    successToast(toast, res.data.message);
                    onClose();
                })
                .catch(err => errToast(toast, err));
        }}>Создать композицию</DefaultButton>
    </VStack>
}
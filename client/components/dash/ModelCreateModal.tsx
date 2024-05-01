'use client';

import { Checkbox, HStack, Icon, Input, Select, Slider, SliderFilledTrack, SliderThumb, SliderTrack, Spinner, Text, Tooltip, useToast, VStack } from "@chakra-ui/react";
import { useCallback, useEffect, useState } from "react";
import { useSelector } from "@/redux/hooks";
import { IDataframe, IParam } from "@/utils/types";
import { DefaultButton } from "@/components/Common";
import { api, arrToChunks, errToast, genHash, getCustomDate, successToast } from "@/utils/misc";
import { AiOutlineClose } from "react-icons/ai";

const stackStyles = {
    w: '100%',
    align: 'start',
    spacing: '20px'
};

export function ModelCreateModal({ onClose, dfID }: { onClose: any, dfID: string | null }) {
    const toast = useToast();
    const [params, setParams] = useState<any[]>([]);
    const [sliderValue, setSliderValue] = useState(80);
    const { DFsList } = useSelector(state => state.dataframe);
    const { Authorization } = useSelector(state => state.misc);
    // const query = useSearchParams();

    // const dfID = query.get('dataframe_id');
    const dataframe = DFsList.find((df: IDataframe) => df._id === dfID);

    const [taskType, setTaskType] = useState(-1);
    const [taskTypes, setTaskTypes] = useState<string[]>([]);
    const [paramsTypes, setParamsTypes] = useState<string[]>([]);
    const [modelTypes, setModelTypes] = useState<string[]>([]);
    const [paramsSelectionType, setParamsSelectionType] = useState('default');

    const updateParams = useCallback((task: string) => {
        api.get('/model/specs/model_types/parameters/' + task)
            .then(res => setParams(Object.values(res.data.properties)))
            .catch(err => errToast(toast, err));
    }, [toast]);

    const updateModelTypes = useCallback((task: string) => {
        if (!taskTypes.includes(task)) return;

        api.get('/model/specs/model_types?task_type=' + task).then(res => {
            setModelTypes(res.data);
            updateParams(res.data[0]);
        });
    }, [taskTypes, updateParams]);

    useEffect(() => {
        api.get('/model/specs/task_types').then(res => {
            setTaskTypes(res.data);
            updateModelTypes(res.data[0]);
        });
        api.get('/model/specs/params_types').then(res => setParamsTypes(res.data));
    }, [dfID, updateModelTypes, updateParams]);

    return dataframe ? <VStack align='start' py='20px' spacing='20px'>
        <VStack {...stackStyles} key={1}>
            <Text fontSize='30px' fontWeight={700} letterSpacing='1px'>Создать модель</Text>

            <VStack align='start' spacing='16px'>
                <Text fontSize='24px'>{dataframe.filename}</Text>
                <Text fontSize='14px' letterSpacing='0.5px' fontWeight={300} opacity={0.5}>Создано {getCustomDate(dataframe.created_at)}</Text>
            </VStack>

            <VStack w='100%' spacing='20px'>
                <HStack w='100%' justify='space-between' align='start' p='20px 10px' fontSize='20px' fontWeight={600} borderRadius='15px'>
                    <VStack align='start' w='24%'>
                        <Text>Тип задачи</Text>
                        <Select placeholder='❓ Выберите тип задачи' id='taskTypeSelect' onChange={(e: any) => {
                            setTaskType(taskTypes.indexOf(e.target.value));
                            updateModelTypes(e.target.value);
                        }}>
                            {taskTypes.map((tt: string, i: number) => <option key={i} value={tt}>{tt}</option>)}
                        </Select>
                    </VStack>
                    
                    {taskType > -1 && <>
                        <VStack align='start' w='24%'>
                            <Text>Тип модели</Text>
                            <Select defaultValue={modelTypes[0]} id='modelType' onChange={(e: any) => updateParams(e.target.value)}>
                                {modelTypes.map((tt: string, i: number) => <option key={i} value={tt}>{tt}</option>)}
                            </Select>
                        </VStack>
                        <VStack align='start' w='24%'>
                            <Text>Тип подбора параметров</Text>
                            <Select value={paramsSelectionType} onChange={(e: any) => setParamsSelectionType(e.target.value)} id='paramsType'>
                                {paramsTypes.map((tt: string, i: number) => <option key={i} value={tt}>{tt}</option>)}
                            </Select>
                        </VStack>
                        <VStack align='start' w='24%' spacing='20px' opacity={[0, 1].includes(taskType) ? 1 : 0} pointerEvents={[0, 1].includes(taskType) ? 'auto' : 'none'}>
                            <Text>Соотношение train/test</Text>
                            <Slider aria-label='train/test' value={sliderValue} onChange={setSliderValue}>
                                <SliderTrack>
                                    <SliderFilledTrack />
                                </SliderTrack>
                                <Tooltip
                                    hasArrow
                                    bg='main.400'
                                    color='white'
                                    placement='right'
                                    isOpen={[0, 1].includes(taskType)}
                                    label={`${sliderValue / 100}`}
                                >
                                    <SliderThumb w='10px' h='10px' bg='main.400' boxShadow='0px 0px 10px 0px rgba(0,0,255,0.5)' />
                                </Tooltip>
                            </Slider>
                            {taskType === 0 && <Checkbox size='md' id='startCheck'><Text fontWeight={400}>Стратифицировать выборку при разделении</Text></Checkbox>}
                        </VStack>
                    </>}
                </HStack>

                {paramsSelectionType !== 'hyperopt' && taskType > -1 && <VStack w='100%' spacing='14px'>
                    {arrToChunks(params, 3).map((chunk: IParam[], i: number) => <HStack key={i} w='100%' justify='space-between' align='start'>
                        {chunk.map((x: IParam, j: number) => <VStack key={j} justify='start' align='start' spacing='6px' w='32%' pos='relative'>
                            <HStack w='100%' pos='relative'>
                                <Text>{x.title}</Text>
                                <Text opacity={0.5} fontWeight={400} fontSize='12px' pos='absolute' right={0}>{x.type}</Text>
                            </HStack>

                            {x.type === 'string'
                                ? <Select isDisabled={paramsSelectionType === 'default'} defaultValue={x.enum ? x.enum[0] : ''} className='param' id={`param_${x.title}`}>
                                    {x.enum?.map((tt: string, k: number) => <option key={k} value={tt}>{tt}</option>)}
                                </Select>
                                : <>
                                    <Input isDisabled={paramsSelectionType === 'default'} w='100%' className='param' id={`param_${x.title}`} defaultValue={x.default} />
                                    {paramsSelectionType !== 'default' && <Icon as={AiOutlineClose} pos='absolute' color='main.400' boxSize='15px' top='34px' right='12px' zIndex={2} _hover={{ cursor: 'pointer' }} onClick={() => {
                                        const input: HTMLInputElement = document.getElementById(`param_${x.title}`) as HTMLInputElement;
                                        if (!input) return;
                                        input.value = '';
                                    }} />}
                                </>}

                            {x.type === 'integer' && <VStack w='100%' fontSize='12px' opacity={0.5} align='start' fontWeight={400}>
                                {Object.keys(x).filter((x: string) => !['title', 'default', 'type'].includes(x)).map((key: string, k: number) => <Text key={k}>{key}: {x[key as keyof typeof x]}</Text>)}
                            </VStack>}
                        </VStack>)}
                    </HStack>)}
                </VStack>}

                {taskType > -1 && <DefaultButton onClick={() => {
                    const taskTypeSelect: HTMLElement | null = document.getElementById('taskTypeSelect');
                    const modelType: HTMLElement | null = document.getElementById('modelType');
                    const paramsType: HTMLElement | null = document.getElementById('paramsType');
                    const startCheck: HTMLElement | null = document.getElementById('startCheck');

                    const task_type = taskTypeSelect ? (taskTypeSelect as HTMLSelectElement).value : '';

                    const query = {
                        model_name: genHash(10),
                        dataframe_id: dataframe._id,
                        task_type,
                        params_type: paramsType ? (paramsType as HTMLSelectElement).value : ''
                    };

                    if (task_type === 'classification') Object.assign(query, { test_size: (1 - sliderValue / 100), stratify: startCheck ? (startCheck as any).checked : '' });

                    const body = {
                        model_type: modelType ? (modelType as HTMLInputElement).value : '',
                        params: paramsSelectionType === 'custom'
                            ? Object.fromEntries(Array.from(document.getElementsByClassName('param')).map((el: any) => [el.id.slice(6), el.value]))
                            : {}
                    };

                    api.post(`/model/processing/train?${Object.keys(query).map((key: string) => `${key}=${encodeURIComponent(query[key as keyof typeof query])}`).join('&')}`, body, { headers: { Authorization } })
                        .then(res => {
                            onClose();
                            successToast(toast, res.data.message);
                        })
                        .catch(err => errToast(toast, err));
                }}>Обучить модель</DefaultButton>}
            </VStack>
        </VStack>
    </VStack> : <Spinner size='lg' />
}
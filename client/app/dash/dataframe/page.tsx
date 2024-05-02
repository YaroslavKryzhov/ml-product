'use client';

import { Box, Button, Checkbox, Divider, Flex, HStack, Icon, IconButton, Tooltip, Input, Modal, UnorderedList, ListItem, ModalBody, ModalCloseButton, ModalContent, ModalFooter, ModalHeader, ModalOverlay, Radio, RadioGroup, Select, SimpleGrid, Spinner, Stack, Text, useDisclosure, useToast, VStack } from "@chakra-ui/react";
import { BiSolidRightArrow } from "react-icons/bi";
import { DefaultButton } from "@/components/Common";
import { HiOutlineDownload } from "react-icons/hi";
import { api, arrToChunks, errToast, getCustomDate, successToast } from "@/utils/misc";
import { nextPage, prevPage, renameDataframe, setCorrMatrix, setCurrentValues, setJobs, setPage, setTargetFeature, setTree } from "@/redux/dataframeSlice";
import { IColumn, IDataframe, IParam } from "@/utils/types";
import { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "@/redux/hooks";
import { useRouter, useSearchParams } from "next/navigation";
import { DeleteIconButton } from "@/components";
import { ApplyMethodModal, ModelCreateModal } from "@/components/dash";
import { tableViews } from "@/utils/enums";
import { AiOutlineClose } from "react-icons/ai";
import { Suspense } from 'react';
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip as ChartTooltip, XAxis, YAxis } from 'recharts';
import { FaArrowRight, FaCheck, FaRegCircleXmark } from "react-icons/fa6";
import { AnimatePresence, motion } from "framer-motion";

function getCellColor(n: string) {
    if (isNaN(parseInt(n))) return 'none';
    
    const num = parseFloat(n);
    const abs = Math.abs(num);

    if (abs > 0 && abs < 0.1) return num > 0 ? '#cfe9db' : '#edc4c4';
    else if (abs >= 0.1 && abs < 0.2) return num > 0 ? '#b7dbc7' : '#e0afaf';
    else if (abs >= 0.2 && abs < 0.3) return num > 0 ? '#9ec9b2' : '#d9a4a4';
    else if (abs >= 0.3 && abs < 0.4) return num > 0 ? '#86bb9f' : '#d19797';
    else if (abs >= 0.4 && abs < 0.5) return num > 0 ? '#78b293' : '#c88888';
    else if (abs >= 0.5 && abs < 0.6) return num > 0 ? '#70ac8c' : '#c17f7f';
    else if (abs >= 0.6 && abs < 0.7) return num > 0 ? '#66a483' : '#ba7878';
    else if (abs >= 0.7 && abs < 0.8) return num > 0 ? '#609e7d' : '#b37070';
    else if (abs >= 0.8 && abs < 0.9) return num > 0 ? '#5a9877' : '#ad6969';
    else if (abs >= 0.9 && abs <= 1) return num > 0 ? '#539170' : '#a66262';
}

const initSelectFeature = '❓ Select feature';

export default function DataframePage() {
    const [search, setSearch] = useState(initSelectFeature);
    const [details, setDetails] = useState<IColumn[]>([]);
    const [selectedDF, setSelectedDF] = useState('');
    const [successSelection, setSuccessSelection] = useState(false);
    const [featureToShow, setFeatureToShow] = useState(-1);
    const [newFilename, setNewFilename] = useState('');
    const { isOpen: isOpenDelete, onOpen: onOpenDelete, onClose: onCloseDelete } = useDisclosure();
    const { isOpen: isOpenApply, onOpen: onOpenApply, onClose: onCloseApply } = useDisclosure();
    const { isOpen: isOpenApplyPipeline, onOpen: onOpenApplyPipeline, onClose: onCloseApplyPipeline } = useDisclosure();
    const { isOpen: isOpenModel, onOpen: onOpenModel, onClose: onCloseModel } = useDisclosure();
    const { isOpen: isOpenFeature, onOpen: onOpenFeature, onClose: onCloseFeature } = useDisclosure();
    const { DFsList, page, currentValues, pagesCount, corrMatrix } = useSelector(state => state.dataframe);
    const dispatch = useDispatch();
    const query = useSearchParams()!;
    const toast = useToast();
    const router = useRouter();
    const { Authorization } = useSelector(state => state.misc);

    const dataframe = DFsList.find((df: IDataframe) => df._id === query.get('dataframe_id'));
    const [view, setView] = useState(tableViews[0]);

    const updateDFContent = useCallback((page: number) => {
        api.get(`/dataframe/content?dataframe_id=${query.get('dataframe_id')}&page=${page + 1}&rows_on_page=20`, { headers: { Authorization } })
            .then(res => dispatch(setCurrentValues(res.data)))
            .catch(err => errToast(toast, err));
    }, [Authorization, dispatch, query, toast]);

    function handleTypeChange(column: string, e: string) {
        api.put(`/dataframe/edit/change_columns_type?dataframe_id=${dataframe?._id}&new_type=${e}`, [column], { headers: { Authorization } })
            .then(() => {
                successToast(toast, 'Тип столбца сменён!');
                updateStats();
            })
            .catch(err => errToast(toast, err));
    }

    const [params, setParams] = useState<any>({});
    const [selectionMethods, setSelectionMethods] = useState<string[]>([]);
    const [checkedMethods, setCheckedMethods] = useState<string[]>([]);

    const updateParams = useCallback((method: string) => {
        if (method === 'SelectFromModel') api.get('/model/specs/task_types').then(res => {
            setParams((s: any) => {
                const toReturn = structuredClone(s);
                toReturn[method] = [{ title: 'estimator', type: 'string', enum: res.data }];
                return toReturn;
            });
        });
        else api.get('/dataframe/specs/feature_selection/methods/parameters/' + method)
            .then(res => {
                setParams((s: any) => {
                    const toReturn = structuredClone(s);
                    toReturn[method] = Object.values(res.data.properties);
                    return toReturn;
                });
            })
            .catch(err => errToast(toast, err));
    }, [toast]);

    const updateStats = useCallback(() => {
        api.get('/dataframe/content/statistics?dataframe_id=' + query.get('dataframe_id'), { headers: { Authorization } })
            .then(res => {
                const el = res.data.find((x: any) => x.name === dataframe?.target_feature);
                if (el) {
                    setDetails([el, ...res.data.filter((x: any) => x.name !== el.name)]);
                    setSearch(`${dataframe?.target_feature}`);
                } else if (dataframe) setDetails(res.data);
            })
            .catch(err => errToast(toast, err));
    }, [Authorization, dataframe, query, toast]);

    useEffect(() => {
        if (!Authorization) return;
        updateDFContent(0);
        updateStats();
        if (dataframe) setNewFilename(dataframe.filename);

        api.get('/dataframe/specs/feature_selection/methods').then(res => setSelectionMethods(res.data.methods));
        api.get('/dataframe/content/corr_matrix?dataframe_id=' + query.get('dataframe_id'), { headers: { Authorization } })
            .then(res => dispatch(setCorrMatrix(res.data)))
            .catch(err => errToast(toast, err));

    }, [Authorization, dataframe, dispatch, query, toast, updateDFContent, updateStats]);

    const CustomChartTooltip = ({ payload }: { payload?: any[] }) => <Flex p='10px 20px' bg='white' borderRadius='10px' border='2px solid lightgray' color='main.400'><Text>{payload ? payload[0]?.value : ''}</Text></Flex>;

    const NumericBlock = ({ i }: { i: number }) => {
        const d = details[i];

        return <HStack key={i} w='100%' h='400px' p='20px' justify='space-between' bg='white'>
            <VStack w='48%' h='100%' spacing='20px' pos='relative'>
                <HStack w='100%' justify='space-between'>
                    <Text fontSize='24px'>{d.name}</Text>
                    <DeleteIconButton exec={() => api.post(
                        `/dataframe/edit/apply_method?dataframe_id=${dataframe?._id}&new_filename=${dataframe?.filename + `_no${d.name}`}`,
                        [{ method_name: 'drop_columns', columns: [d.name], params: {} }],
                        { headers: { Authorization } }
                    )
                        .then(() => {
                            successToast(toast, `Столбец ${d.name} удалён и создан новый датафрейм!`);
                            if (isOpenFeature) onCloseFeature();
                        })
                        .catch(err => errToast(toast, err))} />
                </HStack>

                <ResponsiveContainer width='100%' height='100%' style={{ fontWeight: 400, marginLeft: '-40px' }}>
                    <BarChart data={d.data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="right" />
                        <YAxis />
                        <ChartTooltip content={<CustomChartTooltip />} />
                        <Bar dataKey="value" fill="#6f97e5" barSize={40} />
                    </BarChart>
                </ResponsiveContainer>
            </VStack>

            <VStack w='49%' spacing='16px'>
                <VStack w='100%' spacing='4px' align='start'>
                    <Text fontSize='18px'>Тип</Text>
                    <RadioGroup value={d.type} onChange={(e: string) => handleTypeChange(d.name, e)}>
                        <HStack fontWeight={400} spacing='20px'>
                            <Radio value='numeric'>Числовой</Radio>
                            <Radio value='categorical'>Категориальный</Radio>
                        </HStack>
                    </RadioGroup>
                </VStack>

                <VStack w='100%' spacing='10px' fontWeight={400} align='start'>
                    <Text>Тип данных: {d.data_type}</Text>
                    <Text>Непустые: {d.not_null_count}</Text>
                    <Text>Отсутствуют значения: {d.null_count}</Text>
                    <Text>Среднее: {d.column_stats.mean}</Text>
                    <Text>Стандартное отклонение: {d.column_stats.std}</Text>
                </VStack>

                <VStack w='100%' pr='20%' spacing='10px' align='start' fontWeight={400}>
                    <Text fontSize='18px' fontWeight={600}>Квантили</Text>
                    <HStack w='100%' justify='space-between' px='6px'>
                        {['Min', '25%', '50%', '75%', 'Max'].map((p: string) => <Text key={p} w='19%'>{p}</Text>)}
                    </HStack>

                    <Divider border='1px solid black' opacity={0.1} />

                    <HStack w='100%' justify='space-between' px='6px'>
                        {[d.column_stats.min, d.column_stats.first_percentile, d.column_stats.second_percentile, d.column_stats.third_percentile, d.column_stats.max].map((p: number, i: number) => <Text key={i} w='19%'>{Math.floor(p * 10000) / 10000}</Text>)}
                    </HStack>

                    <Divider border='1px solid black' opacity={0.1} />
                </VStack>
            </VStack>
        </HStack>;
    };

    const CategoricalBlock = ({ i }: { i: number }) => {
        const d = details[i];
        const data = d.data.slice(-5);

        return <HStack key={i} w='100%' h='400px' p='20px' justify='space-between' bg='white'>
            <VStack w='48%' h='100%' spacing='20px' pos='relative'>
                <HStack w='100%' justify='space-between'>
                    <Text fontSize='24px'>{d.name}</Text>
                    <DeleteIconButton exec={() => api.post(
                        `/dataframe/edit/apply_method?dataframe_id=${dataframe?._id}&new_filename=${dataframe?.filename + `_no${d.name}`}`,
                        [{ method_name: 'drop_columns', columns: [d.name], params: {} }],
                        { headers: { Authorization } }
                    )
                        .then(() => {
                            successToast(toast, `Столбец ${d.name} удалён и создан новый датафрейм!`);
                            if (isOpenFeature) onCloseFeature();
                        })
                        .catch(err => errToast(toast, err))} />
                </HStack>

                <ResponsiveContainer width='100%' height='100%' style={{ fontWeight: 400, marginLeft: '-40px' }}>
                    <BarChart data={d.data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <ChartTooltip content={<CustomChartTooltip />} />
                        <Bar dataKey="value" fill="#6f97e5" barSize={40} />
                    </BarChart>
                </ResponsiveContainer>
            </VStack>

            <VStack w='49%' spacing='16px'>
                <VStack w='100%' spacing='4px' align='start'>
                    <Text fontSize='18px'>Тип</Text>
                    <RadioGroup value={d.type} onChange={(e: string) => handleTypeChange(d.name, e)}>
                        <HStack fontWeight={400} spacing='20px'>
                            <Radio value='numeric'>Числовой</Radio>
                            <Radio value='categorical'>Категориальный</Radio>
                        </HStack>
                    </RadioGroup>
                </VStack>

                <VStack w='100%' spacing='10px' fontWeight={400} align='start'>
                    <Text>Тип данных: {d.data_type}</Text>
                    <Text>Непустые: {d.not_null_count}</Text>
                    <Text>Отсутствуют значения: {d.null_count}</Text>
                </VStack>

                <VStack w='100%' pr='20%' spacing='10px' align='start' fontWeight={400}>
                    <Text fontSize='18px' fontWeight={600}>Наиболее частые значения</Text>
                    <HStack w='100%' justify='space-between' px='6px'>
                        {['Значение', ...data.map((x: any) => x.name)].map((p: string, i: number) => <Text key={i} w={`${100 / (data.length + 1) - 1}%`}>{p}</Text>)}
                    </HStack>

                    <Divider border='1px solid black' opacity={0.1} />

                    <HStack w='100%' justify='space-between' px='6px'>
                        {['Частота', ...data.map((x: any) => `${Math.round(x.value * 10000) / 10000}`)].map((p: string, i: number) => <Text key={i} w={`${100 / (data.length + 1) - 1}%`}>{p}</Text>)}
                    </HStack>

                    <Divider border='1px solid black' opacity={0.1} />
                </VStack>
            </VStack>
        </HStack>;
    };

    return dataframe ? <Suspense fallback={<></>}>
        <HStack spacing='8px' fontSize='18px' fontWeight={400} p='10px 14px' borderRadius='10px' bg='main.100'>
            {document.getElementById('tree_' + query.get('dataframe_id')) &&
                JSON.parse(document.getElementById('tree_' + query.get('dataframe_id'))?.innerHTML ?? '[]').map((parent: string, i: string) => <HStack key={i} spacing='8px'>
                    <Text>{parent}</Text>
                    <Icon as={BiSolidRightArrow} color='gray.300' boxSize='14px' />
                </HStack>)}
            <Text>{dataframe.filename}</Text>
        </HStack>

        <HStack w='100%' justify='space-between'>
            <VStack pl='8px' align='start' spacing='16px' pos='relative'>
                <Input minW='400px' fontWeight={600} border='none' _hover={{ outline: '1px solid lightgray' }} transition='0.1s' fontSize='26px' value={newFilename} onChange={(e: any) => setNewFilename(e.target.value)} />

                {newFilename !== dataframe.filename && <IconButton pos='absolute' zIndex={1} right='-50px' bg='none' color='main.400' _hover={{ color: 'green.500', transform: 'scale(1.2)' }} transition='0.1s' fontSize='18px' icon={<FaCheck />} aria-label='rename' onClick={() => {
                    api.put(`/dataframe/rename?dataframe_id=${dataframe._id}&new_filename=${newFilename}`, {}, { headers: { Authorization } })
                        .then(() => {
                            successToast(toast, `Датафрейм переименован!`);
                            dispatch(renameDataframe([dataframe.filename, newFilename]));
                            api.get('/dataframe/metadata/trees', { headers: { Authorization } }).then(res => dispatch(setTree(res.data)));
                        })
                        .catch(err => errToast(toast, err));
                }} />}

                <Text ml='18px' fontSize='14px' letterSpacing='0.5px' fontWeight={300} opacity={0.5}>Создано {getCustomDate(dataframe.created_at)}</Text>
            </VStack>

            <HStack spacing={0}>
                <DefaultButton onClick={onOpenModel}>Создать модель</DefaultButton>
                <IconButton ml='20px' aria-label='download' icon={<HiOutlineDownload />} fontSize='30px' color='main.400' bg='none' onClick={() => {
                    api.get(
                        '/dataframe/download?dataframe_id=' + dataframe._id,
                        { headers: { Authorization }, responseType: 'blob' }
                    ).then(res => {
                        const href = URL.createObjectURL(res.data);
                        const link = document.createElement('a');
                        link.href = href;
                        link.setAttribute('download', dataframe.filename);
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        URL.revokeObjectURL(href);
                    });
                }} _hover={{ cursor: 'pointer' }} _active={{}} />
                <DeleteIconButton exec={onOpenDelete} />
            </HStack>
        </HStack>

        <VStack w='100%' borderRadius={6} p='8px 16px 8px 24px' align='start' spacing='24px'>
            <HStack spacing='18px'>
                <DefaultButton onClick={onOpenApply}>Применить метод</DefaultButton>
                <Button onClick={onOpenApplyPipeline} colorScheme='green' fontSize='14px'>Применить пайплайн</Button>
            </HStack>

            {dataframe.pipeline.length > 0
                ? <SimpleGrid spacingX='24px' spacingY='8px' columns={5}>
                    <Flex bg='green.500' p='4px 12px' borderRadius={20} userSelect='none'>
                        <Text fontSize='14px' color='white' lineHeight='16px'>Применённые методы</Text>
                    </Flex>

                    {dataframe.pipeline.map((obj: any, i: number) => <Tooltip key={i} closeOnClick={false} label={<VStack align='start' spacing='16px' p='10px'>
                        <VStack align='start' spacing='4px'>
                            <Text fontWeight={600} fontSize='18px'>Columns</Text>
                            {obj.columns.length > 0
                                ? <UnorderedList>
                                    {obj.columns.map((col: string, j: number) => <ListItem key={j}>{col}</ListItem>)}
                                </UnorderedList>
                                : <Text>no columns</Text>}
                        </VStack>

                        <Text as='pre'>Params {JSON.stringify(obj?.params ?? {}, null, 4)}</Text>
                    </VStack>}>
                        <Flex _hover={{ cursor: 'help' }} bg='main.300' p='4px 12px' justify='center' pos='relative' borderRadius={20}>
                            <Text fontSize='14px' userSelect='none' fontWeight={400} color='white' lineHeight='16px'>{obj.method_name}</Text>
                            <Icon as={FaArrowRight} boxSize='16px' color='gray.400' pos='absolute' top='4px' left='-20px' />
                        </Flex>
                    </Tooltip>)}
                </SimpleGrid>
                : <Flex bg='main.500' p='4px 12px' borderRadius={20}>
                    <Text fontSize='14px' color='white' lineHeight='16px'>Методы не применены</Text>
                </Flex>}
        </VStack>

        <VStack w='max-content' align='start' spacing={0}>
            <Text fontSize='16px' lineHeight='100%' letterSpacing='1px' p='8px'>Целевой признак</Text>

            <HStack pos='relative'>
                <Select w='250px' value={search} onChange={(e: any) => setSearch(e.target.value)}>
                    {!dataframe.target_feature && <option>{initSelectFeature}</option>}
                    {details.map((x: any, i: number) => <option key={i} value={x.name}>{x.name}</option>)}
                </Select>

                {/* @ts-ignore */}
                <DefaultButton isDisabled={search === dataframe.target_feature || search === initSelectFeature} h='40px' onClick={() => {
                    api.put(`/dataframe/edit/target?dataframe_id=${dataframe._id}&target_column=${search}`, {}, { headers: { Authorization } })
                        .then(() => {
                            successToast(toast, 'Целевой признак задан!');
                            dispatch(setTargetFeature({ id: dataframe._id, search }));
                        })
                        .catch(err => errToast(toast, err));
                }}>Задать</DefaultButton>

                <IconButton isDisabled={dataframe.target_feature === null} colorScheme='red' w='40px' h='40px' icon={<FaRegCircleXmark />} aria-label='clear target feature' onClick={() => {
                    api.delete(`/dataframe/edit/target?dataframe_id=${dataframe._id}`, { headers: { Authorization } })
                        .then(() => {
                            successToast(toast, 'Выбор целевого признака очищен!');
                            dispatch(setTargetFeature({ id: dataframe._id, search: null }));
                        })
                        .catch(err => errToast(toast, err));
                }} />
            </HStack>
        </VStack>

        <VStack w='100%' spacing='14px' align='start' bg='main.100' borderRadius={6} p='14px'>
            <HStack w='100%' spacing='8px'>
                {['Детально', 'Компактно', 'Подробнее', 'Матрица корреляции', 'Отбор признаков'].map((x: string, i: number) =>
                    <Text key={i} color={view === x ? 'main.400' : 'black'} bg={view === x ? 'main.200' : 'none'} borderRadius={6} p='6px 12px' fontSize='24px' lineHeight='100%' letterSpacing='1px' _hover={{ cursor: 'pointer', bg: 'main.200' }} transition='0.1s' onClick={() => setView(x)}>{x}</Text>)}
            </HStack>

            <Divider w='100%' borderColor='gray.300' />

            <AnimatePresence mode='wait'>
                <motion.div
                    key={view}
                    style={{ width: '100%' }}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.06 }}
                >
                    <VStack key={view} w='100%' spacing='24px' align='start' overflowX='auto'>
                        {['Детально', 'Компактно'].includes(view) && <HStack spacing={0} align='start'>
                            {details.map((x: any, i: number) => {
                                const isBlue = dataframe.target_feature === x.name;

                                return <VStack w='max-content' key={i} spacing={0} borderTop='1px solid' borderLeft={i === 0 ? '1px solid' : 'none'} borderBottom='1px solid' borderRight='1px solid' borderColor={isBlue ? 'main.400' : 'gray.400'} _hover={{ cursor: 'pointer', color: 'main.400' }} onClick={() => {
                                    setFeatureToShow(i);
                                    onOpenFeature();
                                }}>
                                    <VStack w='100%' align='start' bg={isBlue ? 'main.200' : 'white'} transition='0.1s' p='10px'>
                                        <Text>{x.name}</Text>

                                        {view !== 'Компактно' && <>
                                            <VStack w='100%' spacing='2px' fontSize='14px' letterSpacing='1px' fontWeight={400} align='start'>
                                                <Text>Тип: {x.type}</Text>
                                                <Text>Пустые: {x.null_count}</Text>
                                            </VStack>

                                            <Divider w='100%' borderColor={isBlue ? 'main.400' : 'gray.400'} />

                                            <HStack w='100%' h='70px' align='end' spacing='4px'>
                                                {x.data.map((val: any, i: number) => <VStack key={i} w={x.type === 'categorical' ? '100%' : '10px'} spacing={0} h='100%' justify='end'>
                                                    <Box w='100%' bg={isBlue ? 'main.400' : 'gray.400'} h={`${val.value / Math.max(...x.data.map((v: any) => v.value)) * 100}%`} />
                                                </VStack>)}
                                            </HStack>
                                        </>}
                                    </VStack>

                                    <VStack w='100%' fontSize='16px' spacing='4px' borderTop='1px solid' borderColor={isBlue ? 'main.400' : 'gray.400'} bg='white'>
                                        {currentValues[x.name] && currentValues[x.name].map((value: string, i: number) => <VStack key={i} w='100%' h='30px'>
                                            <Divider w='100%' borderColor={i > 0 ? isBlue ? 'main.400' : 'gray.400' : 'rgba(0,0,0,0)'} />
                                            <Text w='100%' px='10px' transition='0.1s' textAlign='left' fontFamily='Roboto Mono Variable' fontSize='13px' fontWeight={400} color={isBlue ? 'main.400' : 'black'}>{isNaN(parseFloat(value)) ? value : Math.round(parseFloat(value) * 10000) / 10000}</Text>
                                        </VStack>)}
                                    </VStack>
                                </VStack>;
                            })}
                        </HStack>}

                        {view === 'Матрица корреляции' && <HStack spacing={0} align='start'>
                            {[
                                { name: '⠀', data: Object.keys(corrMatrix) },
                                ...Object.keys(corrMatrix).map((key: string) => ({
                                    name: key,
                                    data: Object.values(corrMatrix).map((v: any) => Math.round(v[key] * 10000) / 10000)
                                }))
                            ].map((x: any, i: number) => {
                                return <VStack w='max-content' key={i} spacing={0} borderTop='1px solid' borderLeft={i === 0 ? '1px solid' : 'none'} bg='white' borderBottom='1px solid' borderRight='1px solid' borderColor='gray.400' fontWeight={i === 0 ? 600 : 400}>
                                    <VStack w='100%' align='start' p='10px' bg='white'>
                                        <Text fontWeight={600}>{x.name}</Text>
                                    </VStack>

                                    <VStack w='100%' fontSize='16px' spacing='0px' borderTop='1px solid' borderColor='gray.400'>
                                        {x.data.map((value: string, i: number) => <VStack key={i} bg={getCellColor(value)} w='100%' h='30px'>
                                            <Divider w='100%' borderColor={i > 0 ? 'gray.400' : 'rgba(0,0,0,0)'} />
                                            <Text w='100%' px='10px' textAlign='left' fontFamily='Roboto Mono Variable' fontSize='13px'>{value}</Text>
                                        </VStack>)}
                                    </VStack>
                                </VStack>;
                            })}
                        </HStack>}

                        {view === 'Подробнее' && <VStack w='100%' spacing='14px'>
                            {details.map((d: any, i: number) => d.type === 'numeric'
                                ? <NumericBlock key={i} i={i} />
                                : <CategoricalBlock key={i} i={i} />)}
                        </VStack>}

                        {view === 'Отбор признаков' && <VStack w='100%' align='start' spacing='30px'>
                            <VStack w='100%' align='start' spacing='20px' px='10px'>
                                <Text fontSize='24px' color='gray.700'>Методы отбора</Text>

                                <SimpleGrid columns={2} spacingX='18px' spacingY='8px' fontWeight={400}>
                                    {selectionMethods.map((s: string, j: number) => {
                                        return <Checkbox key={j} isChecked={checkedMethods.includes(s)} className='methodCheck' onChange={(e: any) => {
                                            if (e.target.checked) {
                                                setCheckedMethods(init => [...init, s]);
                                                updateParams(s);
                                            } else setCheckedMethods(init => init.filter((h: string) => h !== s));
                                        }}>{s}</Checkbox>;
                                    })}
                                </SimpleGrid>

                                <VStack w='100%' spacing='14px'>
                                    {Object.keys(params)
                                        .filter((px: string) => params[px].length > 0 && checkedMethods.includes(px))
                                        .map((px: string, i: number) => <VStack key={i} w='100%' align='start' spacing='14px'>
                                            <Divider w='90%' borderColor='gray.400' />
                                            <Text color='main.300' fontSize='20px'>{px}</Text>

                                            {arrToChunks(params[px], 2).map((chunk: IParam[], i: number) => <HStack key={i} w='100%' justify='space-between' align='start'>
                                                {chunk.map((x: IParam, j: number) => <VStack key={j} justify='start' align='start' spacing='6px' w='49%' pos='relative'>
                                                    <HStack w='100%' pos='relative'>
                                                        <Text>{x.title}</Text>
                                                        <Text opacity={0.5} fontWeight={400} fontSize='12px' pos='absolute' right={0}>{x.type}</Text>
                                                    </HStack>

                                                    {x.type === 'string'
                                                        ? <Select defaultValue={x.enum ? x.enum[0] : ''} className={`param_${px}`} id={`param_${x.title}`} onChange={() => setSuccessSelection(false)}>
                                                            {x.enum?.map((tt: string, k: number) => <option key={k} value={tt}>{tt}</option>)}
                                                        </Select>
                                                        : <>
                                                            <Input w='100%' defaultValue={x.default} className={`param_${px}`} id={`param_${x.title}`} onChange={() => setSuccessSelection(false)} />
                                                            <Icon as={AiOutlineClose} pos='absolute' color='main.400' boxSize='15px' top='34px' right='12px' zIndex={2} _hover={{ cursor: 'pointer' }} onClick={() => {
                                                                const input: HTMLInputElement = document.getElementById(`param_${x.title}`) as HTMLInputElement;
                                                                if (input) input.value = '';
                                                            }} />
                                                        </>}

                                                    {x.type === 'integer' && <VStack w='100%' fontSize='12px' opacity={0.5} align='start' fontWeight={400}>
                                                        {Object.keys(x).filter((x: string) => !['title', 'default', 'type'].includes(x)).map((key: string, k: number) => <Text key={k}>{key}: {x[key as keyof typeof x]}</Text>)}
                                                    </VStack>}
                                                </VStack>)}
                                            </HStack>)}
                                        </VStack>)}
                                </VStack>

                                {/* @ts-ignore */}
                                <DefaultButton isDisabled={checkedMethods.length <= 0 || successSelection} onClick={() => {
                                    const res: any[] = [];
                                    checkedMethods.forEach((method: string) => {
                                        const inputs = document.getElementsByClassName('param_' + method);
                                        res.push({
                                            method_name: method,
                                            params: Object.fromEntries(Array.from(inputs).map((input: any) => [input.id.slice(6), input.value]))
                                        });
                                    });

                                    api.post(
                                        `/dataframe/edit/feature_importances?dataframe_id=${dataframe._id}&task_type=classification`,
                                        res,
                                        { headers: { Authorization } }
                                    )
                                        .then(res => {
                                            setSuccessSelection(true);
                                            successToast(toast, res.data.message);
                                            api.get('/background_jobs/all', { headers: { Authorization } }).then(res => dispatch(setJobs(res.data)));
                                        })
                                        .catch(err => errToast(toast, err));
                                }}>Отобрать признаки</DefaultButton>
                            </VStack>

                            {dataframe?.feature_importance_report?.result && <>
                                <Text fontSize='24px' mt='10px' mb='-18px'>Последний отбор</Text>

                                <HStack spacing={0} align='start'>
                                    {[
                                        { name: '⠀', data: Object.keys(dataframe.feature_importance_report.result) },
                                        ...Object.keys(Object.values(dataframe.feature_importance_report.result)[0] as unknown as string[]).map((key: string) => ({
                                            name: key,
                                            data: Object.values(dataframe.feature_importance_report.result).map((v: any) => JSON.stringify(typeof v[key] === 'number' ? Math.round(v[key] * 10000) / 10000 : v[key]))
                                        }))
                                    ].map((x: any, i: number) => {
                                        return <VStack key={i} spacing={0} borderTop='1px solid' borderLeft={i === 0 ? '1px solid' : 'none'} borderBottom='1px solid' borderRight='1px solid' borderColor='gray.400' fontWeight={i === 0 ? 600 : 400}>
                                            <VStack w='100%' align='start' p='10px' bg='white'>
                                                <Text fontWeight={600}>{x.name}</Text>
                                            </VStack>

                                            <VStack w='100%' fontSize='16px' spacing={0} bg='white' borderTop='1px solid' borderColor='gray.400'>
                                                {x.data.map((value: string, i: number) => <VStack key={i} w='100%' h='30px' bg={value === 'true' ? 'green.100' : value === 'false' ? 'red.100' : 'none'}>
                                                    <Divider w='100%' borderColor={i > 0 ? 'gray.400' : 'rgba(0,0,0,0)'} />
                                                    <Text w='100%' px='10px' textAlign='left' fontFamily='Roboto Mono Variable' fontSize='13px'>{value}</Text>
                                                </VStack>)}
                                            </VStack>
                                        </VStack>;
                                    })}
                                </HStack>
                            </>}
                        </VStack>}
                    </VStack>

                    {['Детально', 'Компактно'].includes(view) && <SimpleGrid columns={17} spacing='8px'>
                        <Flex opacity={page <= 0 ? 0.5 : 1} transition='0.1s' boxSize='32px' bg='white' borderRadius={6} justify='center' align='center' _hover={page <= 0 ? { cursor: 'not-allowed' } : { cursor: 'pointer', bg: 'gray.100' }} onClick={() => {
                            if (page <= 0) return;
                            updateDFContent(page - 1);
                            dispatch(prevPage());
                        }}>
                            <svg width='8' height='12' viewBox='0 0 8 12' fill='none' xmlns='http://www.w3.org/2000/svg'><path d='M6.5 1L1.5 6L6.5 11' stroke='#8C9CB0' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' /></svg>
                        </Flex>

                        {(pagesCount > 15
                            ? page < 2
                                ? [0, 1, 2, '...', pagesCount - 1]
                                : page >= pagesCount - 2
                                    ? [0, '...', pagesCount - 3, pagesCount - 2, pagesCount - 1]
                                    : [0, '...', page - 1, page, page + 1, '...', pagesCount - 1]
                            : Array.from({ length: pagesCount }, (_, i) => i)
                        ).map((i: string | number, j: number) => <Stack key={j} transition='0.1s' boxSize='32px' bg={page === i ? 'blue.400' : 'white'} borderRadius={6} justify='center' align='center' _hover={page === i || typeof i === 'string' ? {} : { cursor: 'pointer', bg: 'gray.100' }} onClick={() => {
                            if (typeof i === 'string') return;
                            updateDFContent(i);
                            dispatch(setPage(i));
                        }}>
                            <Text userSelect='none' fontSize='16px' lineHeight='16px' color={page === i ? 'white' : 'rgb(140, 156, 176)'}>{typeof i === 'string' ? i : i + 1}</Text>
                        </Stack>)}

                        <Flex opacity={page >= pagesCount - 1 ? 0.5 : 1} transition='0.1s' boxSize='32px' bg='white' borderRadius={6} justify='center' align='center' _hover={page > pagesCount - 1 ? { cursor: 'not-allowed' } : { cursor: 'pointer', bg: 'gray.100' }} onClick={() => {
                            if (page >= pagesCount - 1) return;
                            updateDFContent(page + 1);
                            dispatch(nextPage());
                        }}>
                            <svg width='8' height='12' viewBox='0 0 8 12' fill='none' xmlns='http://www.w3.org/2000/svg'><path d='M1.5 11L6.5 6L1.5 1' stroke='#8C9CB0' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' /></svg>
                        </Flex>
                    </SimpleGrid>}
                </motion.div>
            </AnimatePresence>
        </VStack>

        <Modal isOpen={isOpenDelete} onClose={onCloseDelete}>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalHeader>Удаление датафрейма</ModalHeader>
                <ModalBody>
                    <Text>Вы уверены, что хотите удалить датафрейм <b>{dataframe.filename}</b>?</Text>
                </ModalBody>
                <ModalFooter>
                    <HStack spacing='12px'>
                        <Button onClick={onCloseDelete}>Оставить</Button>
                        <Button bg='red.500' onClick={() => {
                            api.delete('/dataframe?dataframe_id=' + dataframe._id, { headers: { Authorization } }).then(res => {
                                onCloseDelete();
                                if (res.status === 200) {
                                    successToast(toast, `Датафрейм ${dataframe.filename} удалён!`);
                                    router.push('/dash');
                                } else errToast(toast, res);
                            });
                        }}>Удалить</Button>
                    </HStack>
                </ModalFooter>
            </ModalContent>
        </Modal>

        <Modal isOpen={isOpenApply} onClose={onCloseApply} closeOnOverlayClick={false} size='6xl'>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalCloseButton boxSize='40px' transform='scale(1.5)' color='main.400' />

                <ModalBody bg='main.100'>
                    <Suspense fallback={<></>}>
                        <ApplyMethodModal features={details.map((d: any) => d.name)} df_name={dataframe.filename} onClose={onCloseApply} />
                    </Suspense>
                </ModalBody>
            </ModalContent>
        </Modal>

        <Modal isOpen={isOpenApplyPipeline} onClose={onCloseApplyPipeline} closeOnOverlayClick={false} size='2xl'>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalCloseButton boxSize='40px' transform='scale(1.5)' color='main.400' />

                <ModalBody bg='main.100'>
                    <Suspense fallback={<></>}>
                        <VStack align='start' py='20px' spacing='12px'>
                            <Text fontSize='20px' fontWeight={600}>Выберите датафрейм, к которому нужно применить пайплайн</Text>

                            <Select w='100%' placeholder='❓ Select dataframe' value={selectedDF} onChange={(e: any) => setSelectedDF(e.target.value)}>
                                {DFsList.map((df: IDataframe, i: number) => <option key={i} value={df._id}>{df.filename}</option>)}
                            </Select>

                            <Input w='100%' placeholder='new filename' defaultValue={`${query.get('dataframe_id')}_piped`} id='newPipedDfFilename' />

                            {/* @ts-ignore */}
                            <DefaultButton isDisabled={selectedDF === ''} onClick={() => {
                                api.post(
                                    `/dataframe/edit/copy_pipeline?dataframe_id_from=${query.get('dataframe_id')}&dataframe_id_to=${selectedDF}&new_filename=${(document.getElementById('newPipedDfFilename') as HTMLInputElement)?.value}`,
                                    {},
                                    { headers: { Authorization } }
                                )
                                    .then(onCloseApplyPipeline)
                                    .catch((err: any) => errToast(toast, err));
                            }}>Применить</DefaultButton>
                        </VStack>
                    </Suspense>
                </ModalBody>
            </ModalContent>
        </Modal>

        <Modal isOpen={isOpenModel} onClose={onCloseModel} closeOnOverlayClick={false} size='6xl'>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalCloseButton boxSize='40px' transform='scale(1.5)' color='main.400' />

                <ModalBody bg='main.100'>
                    <Suspense fallback={<></>}>
                        <ModelCreateModal dfID={query.get('dataframe_id')} onClose={onCloseModel} />
                    </Suspense>
                </ModalBody>
            </ModalContent>
        </Modal>

        <Modal isOpen={isOpenFeature} onClose={onCloseFeature} size='6xl' isCentered>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalCloseButton boxSize='40px' transform='scale(1.5)' color='main.400' />

                <ModalBody>
                    {featureToShow > -1 && details[featureToShow].type === 'numeric'
                        ? <NumericBlock key={featureToShow} i={featureToShow} />
                        : <CategoricalBlock key={featureToShow} i={featureToShow} />}
                </ModalBody>
            </ModalContent>
        </Modal>
    </Suspense> : <Flex w='100%' h='400px' justify='center' align='center'><Spinner size='xl' colorScheme='blue' transform='scale(3)' /></Flex>
}
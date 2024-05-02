'use client';
import { DeleteIconButton } from "@/components";
import { DefaultButton } from "@/components/Common";
import { renameModel } from "@/redux/dataframeSlice";
import { useDispatch, useSelector } from "@/redux/hooks";
import { api, arrToChunks, errToast, getCustomDate, successToast } from "@/utils/misc";
import { IDataframe, IModel } from "@/utils/types";
import { Link } from "@chakra-ui/next-js";
import { HStack, Spinner, VStack, Text, Input, IconButton, Alert, AlertIcon, useToast, useDisclosure, Modal, ModalOverlay, ModalContent, Button, ModalFooter, ModalBody, ModalHeader, Switch, FormControl, FormLabel, Icon, Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon, Divider, SimpleGrid, UnorderedList, ListItem, Select, Box } from "@chakra-ui/react";
import { useRouter } from "next/navigation";
import { Suspense, useEffect, useState } from "react";
import { BiSolidRightArrow } from "react-icons/bi";
import { FaCheck } from "react-icons/fa6";
import { CartesianGrid, ResponsiveContainer, XAxis, YAxis, Bar, BarChart, Line, LineChart } from "recharts";

export default function ModelPage() {
    const { DFsList, currentModel: model, modelsList } = useSelector(({ dataframe }) => dataframe);
    const { Authorization } = useSelector(state => state.misc);
    const toast = useToast();
    const router = useRouter();
    const dispatch = useDispatch();
    const [reports, setReports] = useState<any>({});
    const { isOpen: isOpenDelete, onOpen: onOpenDelete, onClose: onCloseDelete } = useDisclosure();
    const { isOpen: isOpenPredict, onOpen: onOpenPredict, onClose: onClosePredict } = useDisclosure();
    const [newFilename, setNewFilename] = useState('');

    useEffect(() => {
        if (model) setNewFilename(model.filename);
    }, [model]);

    // const [toApply, setToApply] = useState<IDataframe | null>(null);

    return model ? <Suspense fallback={<></>}>
        <HStack spacing='8px' fontSize='18px' fontWeight={400} p='10px 14px' borderRadius='10px' bg='main.100'>
            {document.getElementById('tree_' + model.dataframe_id) &&
                JSON.parse(document.getElementById('tree_' + model.dataframe_id)?.innerHTML ?? '[]')
                    .map((parent: string, i: string) => <HStack key={i} spacing='8px'>
                        <Text>{parent}</Text>
                        <Icon as={BiSolidRightArrow} color='gray.300' boxSize='14px' />
                    </HStack>)}

            <HStack spacing='8px'>
                <Text>{DFsList.find((df: IDataframe) => df._id === model.dataframe_id)?.filename}</Text>
                <Icon as={BiSolidRightArrow} color='gray.300' boxSize='14px' />
            </HStack>

            <Text>{model.filename}</Text>
        </HStack>

        <HStack w='100%' justify='space-between'>
            <VStack pl='8px' align='start' spacing='16px' pos='relative'>
                <Input minW='400px' fontWeight={600} border='none' _hover={{ outline: '1px solid lightgray' }} transition='0.1s' fontSize='26px' value={newFilename} onChange={(e: any) => setNewFilename(e.target.value)} />

                {newFilename !== model.filename && <IconButton pos='absolute' zIndex={1} right='-50px' bg='none' color='main.400' _hover={{ color: 'green.500', transform: 'scale(1.2)' }} transition='0.1s' fontSize='18px' icon={<FaCheck />} aria-label='rename' onClick={() => {
                    api.put(`/model/rename?model_id=${model._id}&new_filename=${newFilename}`, {}, { headers: { Authorization } })
                        .then(() => {
                            successToast(toast, `Модель переименована!`);
                            dispatch(renameModel([model.filename, newFilename]));
                        })
                        .catch(err => errToast(toast, err));
                }} />}

                <Text fontSize='14px' letterSpacing='0.5px' fontWeight={300} opacity={0.5}>Создано {getCustomDate(model.created_at)}</Text>
            </VStack>

            <HStack spacing='12px'>
                <DefaultButton onClick={onOpenPredict}>Предсказать по модели</DefaultButton>
                <DeleteIconButton exec={onOpenDelete} />
            </HStack>
        </HStack>

        <VStack w='100%' spacing='14px' align='start'>
            {model?.composition_model_ids
                ? <>
                    <Text fontSize='20px'>Список моделей композиции</Text>
                    <UnorderedList fontWeight={400}>
                        {model?.composition_model_ids
                            .map((id: string) => modelsList.find((mx: IModel) => mx._id === id))
                            .map((mx: IModel | undefined, i: number) => <Link key={i} href={`/dash/model?model_id=${mx?._id}`}>
                                <ListItem>{mx?.filename}</ListItem>
                            </Link>)}
                    </UnorderedList>
                </>
                : arrToChunks(Object.keys(model.model_params.params), 4).map((chunk: string[], i: number) => <HStack key={i} w='100%' justify='space-between' align='start'>
                    {chunk.map((x: string, j: number) => <VStack key={j} justify='start' align='start' spacing='6px' w='24%' pos='relative'>
                        <Text>{x}</Text>
                        {/* <Text opacity={0.5} fontWeight={400} fontSize='12px' pos='absolute' right={0}>{x.type}</Text> */}
                        <Input w='100%' defaultValue={model.model_params.params[x]} isDisabled={true} />
                    </VStack>)}
                </HStack>)}
        </VStack>

        {model.status === 'Training'
            ? <VStack w='100%'>
                <Alert status='info'>
                    <AlertIcon />
                    Модель ещё обучается!
                </Alert>
            </VStack>
            : <>
                <Text fontSize='30px' mt='30px' mb='-10px'>Reports</Text>
                <Accordion w='100%' allowMultiple>
                    {model.metrics_report_ids.map((report: string, i: number) => <AccordionItem key={i}>
                        {(({ isExpanded }) => <>
                            <AccordionButton w='100%' onClick={() => {
                                if (isExpanded) return;

                                api.get('/reports?report_id=' + report, { headers: { Authorization } })
                                    .then(res => setReports((s: any) => {
                                        console.log(res.data.body);
                                        const init = structuredClone(s);
                                        init[report] = res.data.body;
                                        return init;
                                    }));
                            }} bg={i % 2 === 0 && model.metrics_report_ids.length > 2 ? 'main.200' : 'none'} justifyContent='space-between'>
                                <Text>{report}</Text>
                                <AccordionIcon />
                            </AccordionButton>

                            <AccordionPanel>
                                {reports[report]
                                    ? <VStack>
                                        <SimpleGrid
                                            columns={Object
                                                .values(reports[report])
                                                .filter((value: any) => typeof value !== 'object')
                                                .length}
                                        >
                                            {Object.keys(reports[report])
                                                .filter((key: string) => typeof reports[report][key] !== 'object')
                                                .map((key: string, i: number) => <Text key={i} p='6px' border='1px solid lightgray' textAlign='center'>{key}</Text>)}
                                            {Object.values(reports[report])
                                                .filter((value: any) => typeof value !== 'object')
                                                .map((value: any, i: number) => <Text key={i} p='6px' border='1px solid lightgray' textAlign='center' fontWeight={400}>{Math.round(value * 10000) / 10000}</Text>)}
                                        </SimpleGrid>

                                        <ResponsiveContainer width='100%' height='500px' style={{ fontWeight: 400, marginLeft: '-40px' }}>
                                            {/* <BarChart data={reports[report].fpr.map((x: number) => ({ name: 'fpr', value: x }))}>
                                                <CartesianGrid strokeDasharray="3 3" />
                                                <XAxis dataKey="name" />
                                                <YAxis />
                                                <ChartTooltip />
                                                <Bar dataKey="value" fill="#6f97e5" barSize={40} />
                                            </BarChart> */}

                                            <LineChart width={500} height={300} data={reports[report].fpr.map((x: number) => ({ name: 'fpr', value: x }))} style={{ fontWeight: 400 }}>
                                                <XAxis dataKey="name" />
                                                <YAxis />
                                                <CartesianGrid strokeDasharray="3 3" />
                                                <Line type="monotone" dataKey="value" stroke="#8884d8" />
                                                <Line type="monotone" dataKey="value" stroke="#82ca9d" />
                                            </LineChart>
                                        </ResponsiveContainer>
                                    </VStack>
                                    : <Spinner size='md' />}
                            </AccordionPanel>
                        </>)}
                    </AccordionItem>)}
                </Accordion>
            </>}

        <Modal isOpen={isOpenDelete} onClose={onCloseDelete}>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalHeader>Удаление модели</ModalHeader>
                <ModalBody>
                    <Text>Вы уверены, что хотите удалить модель <b>{model.filename}</b>?</Text>
                </ModalBody>
                <ModalFooter>
                    <HStack spacing='12px'>
                        <Button onClick={onCloseDelete}>Оставить</Button>
                        <Button bg='red.500' onClick={() => {
                            api.delete('/model?model_id=' + model._id, { headers: { Authorization } })
                                .then(() => {
                                    onCloseDelete();
                                    successToast(toast, `Датафрейм ${model.filename} удалён!`);
                                    router.push('/dash');
                                })
                                .catch(err => errToast(toast, err));
                        }}>Удалить</Button>
                    </HStack>
                </ModalFooter>
            </ModalContent>
        </Modal>

        <Modal isOpen={isOpenPredict} onClose={onClosePredict}>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalHeader>Предсказать</ModalHeader>

                <ModalBody>
                    <Select>
                        {DFsList.map((df: IDataframe, i: number) => <option key={i} value={df._id}>{df.filename}</option>)}
                    </Select>

                    <FormControl display='flex' alignItems='center'>
                        <FormLabel htmlFor='apply-pipeline' mb='0'>Apply pipeline?</FormLabel>
                        <Switch defaultChecked id='apply-pipeline' />
                    </FormControl>
                </ModalBody>

                <ModalFooter>
                    <DefaultButton onClick={() => {
                        const applyPipeline = document.getElementById('apply-pipeline') as HTMLInputElement;

                        api.put(`/model/processing/predict?model_id=${model._id}&dataframe_id=${model.dataframe_id}&prediction_name=pre_${encodeURIComponent(model.filename)}&apply_pipeline=${applyPipeline?.checked.toString()}`, {}, { headers: { Authorization } })
                            .then(res => {
                                onClosePredict();
                                successToast(toast, res.data.message);
                            })
                            .catch(err => errToast(toast, err));
                    }}>Предсказать</DefaultButton>
                </ModalFooter>
            </ModalContent>
        </Modal>
    </Suspense> : <Spinner size='xl' />
}
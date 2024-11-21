'use client';

import { Accordion, AccordionButton, AccordionItem, AccordionPanel, Box, Button, Flex, HStack, Icon, IconButton, Modal, ModalBody, ModalCloseButton, ModalContent, ModalOverlay, Select, SimpleGrid, Text, useDisclosure, useToast, VStack } from "@chakra-ui/react";
import { AddButton, DefaultButton } from "@/components/Common";
import { setCurrentModel, setDataframes, setModels, setPredictions, setTree } from "@/redux/dataframeSlice";
import { IDataframe, IModel, ISimpleDataframe } from "@/utils/types";
import { Icons } from "@/components";
import { useDispatch, useSelector } from "@/redux/hooks";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { api, errToast } from "@/utils/misc";
import { FaChevronDown, FaChevronLeft, FaChevronUp } from "react-icons/fa6";
import { ComposeCreateModal, DataframeUploadModal, ModelCreateModal } from "@/components/dash";
import { GoDot, GoDotFill } from "react-icons/go";
import Draggable from "react-draggable";
import Link from "next/link";
import { AxiosResponse } from "axios";

const TreeNode = ({ sdf, parents, misc }: { sdf: ISimpleDataframe, parents: string[], misc: any }) => {
    const { dfID, modelID, toast, Authorization, rootHovered, setRootHovered, updTree, router, modelsList } = misc;

    const queryIsCurrent = dfID === sdf.id;
    const currentModelIsChild = modelsList.find((model: IModel) => model._id === modelID)?.dataframe_id === sdf.id;
    const lastChildParents = JSON.parse(document.getElementById('tree_' + dfID)?.innerHTML ?? '[]');

    const [show, setShow] = useState(currentModelIsChild);

    return <VStack w='100%' align='start' spacing='4px'>
        <Draggable
            axis={parents.length > 0 ? 'both' : 'none'}
            position={{ x: 0, y: 0 }}
            onStart={(e: any) => {
                e.stopPropagation();
                e.preventDefault();
            }}
            onDrag={(e: any) => setRootHovered(e.pageX < 70)}
            onStop={() => {
                if (rootHovered) api.put(`/dataframe/edit/move_to_root?dataframe_id=${sdf.id}&new_filename=rooted_${sdf.filename}`, {}, { headers: { Authorization } })
                    .then(() => {
                        setRootHovered(false);
                        updTree();
                    })
                    .catch(err => {
                        setRootHovered(false);
                        errToast(toast, err);
                    });
            }}
        >
            <HStack
                pos='relative'
                spacing='10px'
                p='6px 12px'
                onClick={() => {
                    if (sdf.children.length <= 0) return router.push('/dash/dataframe?dataframe_id=' + sdf.id);

                    if (!(queryIsCurrent || lastChildParents.includes(sdf.filename) || show)) setShow(true);
                    else {
                        if (queryIsCurrent) setShow(s => !s);
                        else router.push('/dash/dataframe?dataframe_id=' + sdf.id);
                    }
                }}
                border='1px solid'
                borderRadius='8px'
                borderColor={currentModelIsChild ? 'main.400' : 'transparent'}
                color={queryIsCurrent || lastChildParents.includes(sdf.filename) ? 'main.400' : 'black'}
                fontWeight={queryIsCurrent ? 600 : 400}
                _hover={{ cursor: 'pointer', color: queryIsCurrent ? 'main.400' : 'main.300' }}
                transition='0.1s'
            >
                <Box w='100%' h='100%' bg={queryIsCurrent ? 'main.200' : 'main.100'} pos='absolute' borderRadius='10px' left={0} zIndex={1} />
                {parents.length > 0 && <Box borderRadius='0 0 0 5px' borderBottom='1px solid rgba(0,0,0,0.25)' borderLeft='1px solid rgba(0,0,0,0.25)' pos='absolute' top='-21px' left='-23px' w='24px' h='38px' />}
                {parents.length > 1 && <Box borderLeft='1px solid rgba(0,0,0,0.25)' pos='absolute' top='-21px' left={`-${(parents.length - 1) * 40 + 23}px`} w='24px' h='34px' />}

                <Icon zIndex={1} as={sdf.children.length > 0 ? (show || lastChildParents.includes(sdf.filename)) ? FaChevronDown : FaChevronUp : queryIsCurrent ? GoDotFill : GoDot} boxSize='10px' transform={`scale(${sdf.children.length > 0 ? 1 : 1.7})`} />
                <Text zIndex={1} userSelect='none'>{sdf.filename}</Text>
            </HStack>
        </Draggable>

        <MetaTree parents={parents} sdf={sdf} />
        {(lastChildParents.includes(sdf.filename) || show) && sdf.children.length > 0 && <Box pl='40px'><Tree treeData={sdf.children} parents={[...parents, sdf.filename]} misc={misc} /></Box>}
    </VStack>
};

const MetaTree = ({ parents, sdf }: { parents: string[], sdf: ISimpleDataframe }) => <>
    {sdf.children.map((child: ISimpleDataframe, i: number) => <Box key={i} pos='absolute'>
        <MetaTree parents={[...parents, sdf.filename]} sdf={child} />
        <span id={`tree_${child.id}`} style={{ display: 'none' }}>{JSON.stringify([...parents, sdf.filename])}</span>
    </Box>)}
</>;

const Tree = ({ treeData, parents, misc }: { treeData: ISimpleDataframe[], parents: string[], misc: any }) => <VStack w='100%' align='start' spacing='4px' fontWeight={400}>
    {treeData.map((sdf: ISimpleDataframe) => <TreeNode sdf={sdf} key={sdf.id} parents={parents} misc={misc} />)}
</VStack>;

export function LeftMenu() {
    const dispatch = useDispatch();
    const toast = useToast();
    const router = useRouter();
    const pathname = usePathname();
    const query = useSearchParams();
    const [rootHovered, setRootHovered] = useState(false);
    const { Authorization } = useSelector(state => state.misc);
    const { DFsList, modelsList, tree, predictionList, currentModel } = useSelector(state => state.dataframe);
    const { isOpen: isOpenModel, onOpen: onOpenModel, onClose: onCloseModel } = useDisclosure();
    const { isOpen: isOpenCompose, onOpen: onOpenCompose, onClose: onCloseCompose } = useDisclosure();
    const { isOpen: isOpenUpload, onOpen: onOpenUpload, onClose: onCloseUpload } = useDisclosure();

    const [modelCreateStep, setModelCreateStep] = useState(0);
    const [modelCreateSelectedDF, setModelCreateSelectedDF] = useState('');

    const dfID = query.get('dataframe_id');
    const modelID = query.get('model_id');

    console.log("dfID" + dfID);
    console.log("modelID:" + modelID); ///////////////////////////////////////////////////////////

    const predID = query.get('prediction_id');

    const updTree = useCallback(() => {
        api.get('/dataframe/metadata/trees', { headers: { Authorization } }).then(res => dispatch(setTree(res.data)));
    }, [Authorization, dispatch]);

    useEffect(() => {
        if (!Authorization) return;

        api.get('/dataframe/metadata/all', { headers: { Authorization } })
            .then(res => dispatch(setDataframes(res.data)))
            .catch(err => {
                console.error(err);
                router.push('/');
            });

        updTree();

        if (dfID) {
            dispatch(setPredictions([]));
            api.get('/model/metadata/by_dataframe?dataframe_id=' + dfID, { headers: { Authorization } })
                .then(res => dispatch(setModels(res.data)))
                .catch(err => errToast(toast, err));
        } else if (modelID) api.get('/model/metadata?model_id=' + modelID, { headers: { Authorization } })
            .then((res: AxiosResponse) => {
                dispatch(setCurrentModel(res.data));
                dispatch(setPredictions(res.data.model_prediction_ids.map((pred: string) => ({ prediction_id: pred, model_id: res.data._id }))));

                api.get('/model/metadata/by_dataframe?dataframe_id=' + res.data.dataframe_id, { headers: { Authorization } })
                    .then(res => dispatch(setModels(res.data)))
                    .catch(err => errToast(toast, err));
            })
            .catch(err => errToast(toast, err));
    }, [dispatch, router, Authorization, toast, pathname, dfID, updTree, modelID]);

    return <VStack minW='420px' w='22vw' p='16px' h='100%' borderRadius='16px' bg='main.100' className='noScrollBar' spacing='20px' align='start' overflowY='auto' color='black'>
        <Accordion w='100%' defaultIndex={[0, 1, 2]} allowMultiple>
            <AccordionItem border='none'>
                {({ isExpanded }) => <>
                    <AccordionButton fontWeight={600} borderRadius='6px' _hover={{}}>
                        <HStack spacing='0px'>
                            <Text fontSize='24px' letterSpacing='1px'>Датафреймы</Text>
                            <Icons isExpanded={isExpanded} />
                        </HStack>
                    </AccordionButton>

                    <AccordionPanel display='flex' flexDirection='column' gap='20px' p={0} pos='relative'>
                        <AddButton onClick={onOpenUpload}>Загрузить датафрейм</AddButton>
                        {/* <Box w='30vw' h='100%' bg='main.200' pos='absolute' top='-20px' left='-50px' opacity={Number(rootHovered)} transition='0.2s' /> */}

                        <VStack w='100%' align='start' pb='12px' bg={rootHovered ? 'main.200' : 'none'} transition='0.2s' overflowX='auto'>
                            <Tree treeData={tree} parents={[]} misc={{
                                toast, Authorization, rootHovered, setRootHovered,
                                dfID, updTree, router, modelsList, modelID: query.get('model_id')
                            }} />
                        </VStack>
                    </AccordionPanel>
                </>}
            </AccordionItem>

            <AccordionItem border='none'>
                {({ isExpanded }) => <>
                    <AccordionButton fontWeight={600} borderRadius='6px' _hover={{}} pt='16px'>
                        <HStack spacing={0}>
                            <Text fontSize='24px' letterSpacing='1px'>Модели</Text>
                            <Icons isExpanded={isExpanded} />
                        </HStack>
                    </AccordionButton>

                    <AccordionPanel display='flex' flexDirection='column' gap='20px' p={0} pb='16px'>
                        {pathname.includes('/dash')
                            ? <>
                                <VStack align='start' spacing='18px'>
                                    <HStack spacing='16px'>
                                        <AddButton onClick={() => {
                                            setModelCreateStep(0);
                                            onOpenModel();
                                        }}>Создать модель</AddButton>
                                        {/* <DefaultButton onClick={() => alert('1233')}>Открыть все метрики</DefaultButton> */}
                                    </HStack>

                                    <VStack w='100%' spacing={0} borderRadius={6}>
                                        <HStack w='100%' px='4px' justify='space-between' bg='main.100'>
                                            {['Модель', 'Тип задачи', 'Статус'].map((x: string, i: number) => <Text key={i} w='33%' fontSize='16px' letterSpacing='1px' textAlign='center' lineHeight='100%' py='8px'>{x}</Text>)}
                                        </HStack>

                                        <VStack w='100%' maxH='250px' py='4px' align='space-between' bg='white' spacing='4px' overflowX='hidden' pos='relative'>
                                            {modelsList.filter((x: IModel) => !x.is_composition).map((x: IModel, i: number) => <Link key={i} href={'/dash/model?model_id=' + x._id}>
                                                <HStack pl='4px' justify='space-between' color={modelID === x._id ? 'main.400' : 'black'} _hover={{ cursor: 'pointer', bg: 'main.200' }} transition='0.05s'>
                                                    {[x.filename, x.task_type, x.status].map((y: string, j: number) => <Text key={j} w='33%' color={modelID === x._id || (j === 0 && currentModel?.composition_model_ids?.includes(x._id)) ? 'main.400' : 'black'} border='1px solid' borderColor={j === 0 && currentModel?.composition_model_ids?.includes(x._id) ? 'main.400' : 'transparent'} bg={modelID === x._id && j === 0 ? 'main.200' : 'none'} borderRadius='8px' fontSize='16px' textAlign='center' fontWeight={300} lineHeight='16px' py='8px' letterSpacing='1px'>{y}</Text>)}
                                                </HStack>
                                            </Link>)}
                                        </VStack>
                                    </VStack>
                                </VStack>

                                <VStack align='start' spacing='18px'>
                                    {/* @ts-ignore */}
                                    <AddButton isDisabled={modelsList.length <= 0} onClick={onOpenCompose}>Создать композицию</AddButton>

                                    <VStack w='100%' spacing={0} borderRadius={6}>
                                        <HStack w='100%' px='4px' justify='space-between' bg='main.100'>
                                            {['Композиция', 'Тип задачи', 'Статус'].map((x: string, i: number) => <Text key={i} w='33%' fontSize='16px' letterSpacing='1px' textAlign='center' lineHeight='100%' pb='8px'>{x}</Text>)}
                                        </HStack>

                                        <VStack w='100%' maxH='250px' py='4px' align='space-between' bg='white' spacing='4px' overflowX='hidden' pos='relative'>
                                            {modelsList.filter((x: IModel) => x.is_composition).map((x: IModel, i: number) => <Link key={i} href={'/dash/model?model_id=' + x._id}>
                                                <HStack pl='4px' justify='space-between' color={modelID === x._id ? 'main.300' : 'black'} _hover={{ cursor: 'pointer', bg: 'main.200' }} transition='0.05s'>
                                                    {[x.filename, x.task_type, x.status].map((y: string, j: number) => <Text key={j} w='33%' bg={modelID === x._id && j === 0 ? 'main.200' : 'none'} borderRadius='8px' fontSize='16px' textAlign='center' fontWeight={300} lineHeight='16px' py='8px' letterSpacing='1px'>{y}</Text>)}
                                                </HStack>
                                            </Link>)}
                                        </VStack>
                                    </VStack>
                                </VStack>
                            </>
                            : <VStack align='start' opacity={0.2}>
                                <HStack spacing='12px'>
                                    <AddButton onClick={() => { }}>Создать модель</AddButton>
                                </HStack>
                                <AddButton onClick={() => { }}>Создать композицию</AddButton>
                            </VStack>}
                    </AccordionPanel>
                </>}
            </AccordionItem>

            <AccordionItem border='none'>
                {({ isExpanded }) => <>
                    <AccordionButton fontWeight={600} borderRadius='6px' _hover={{}} pt='16px'>
                        <HStack spacing={0}>
                            <Text fontSize='24px' letterSpacing='1px'>Предсказания</Text>
                            <Icons isExpanded={isExpanded} />
                        </HStack>
                    </AccordionButton>

                    <AccordionPanel p='10px 0 0 0' pb='16px'>
                        {predictionList.length > 0
                            ? <VStack bg='white' borderRadius={6} spacing={0} overflowX='auto' align='start' w='100%'>
                                <HStack pl='8px'>
                                    {['Name', 'ID'].map((x: string, i: number) => <Text key={i} w='205px' fontSize='16px' letterSpacing='1px' lineHeight='100%' py='8px'>{x}</Text>)}
                                </HStack>

                                {predictionList.map((pred: any, i) => <Link key={i} href={`/dash/prediction?prediction_id=${pred.prediction_id}&model_id=${pred.model_id}`}>
                                    <HStack pl='8px' justify='space-between' bg={predID === pred.prediction_id ? 'main.100' : 'none'} color={predID === pred.prediction_id ? 'main.400' : 'black'} _hover={{ cursor: 'pointer', color: 'main.400' }} transition='0.05s'>
                                        {['Prediction_'+(i+1),pred.prediction_id].map((y: string, j: number) => <Text key={j} w='205px' fontSize='16px' textAlign='left' fontWeight={300} lineHeight='16px' py='12px' letterSpacing='1px'>{y}</Text>)}
                                    </HStack>
                                </Link>)}
                            </VStack>
                            : <Flex w='100%' p='8px 12px' borderRadius={6} bg='white' h='48px' justify='center' align='center'>
                                <Text fontWeight={400} letterSpacing='1px'>Здесь появятся ваши предсказания</Text>
                            </Flex>}
                    </AccordionPanel>
                </>}
            </AccordionItem>
        </Accordion>

        <Modal isOpen={isOpenModel} onClose={onCloseModel} closeOnOverlayClick={false} size='6xl'>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalCloseButton boxSize='40px' transform='scale(1.5)' color='main.400' />

                <ModalBody bg='main.100'>
                    {modelCreateStep === 1 && <IconButton
                        icon={<FaChevronLeft />}
                        fontSize='24px'
                        aria-label='go back to df selection'
                        bg='none'
                        color='main.400'
                        pos='absolute'
                        variant='outline'
                        onClick={() => setModelCreateStep(0)}
                    />}

                    {modelCreateStep === 0
                        ? <VStack align='start' py='20px' spacing='20px'>
                            <Text fontSize='20px' fontWeight={600}>Выберите датафрейм, на основе которого вы хотите создать модель</Text>
                            <Select w='35%' placeholder='❓ Select dataframe' onChange={(e: any) => setModelCreateSelectedDF(e.target.value)}>
                                {DFsList.map((df: IDataframe, i: number) => <option key={i} value={df._id}>{df.filename}</option>)}
                            </Select>
                            <DefaultButton onClick={() => {
                                router.push('/dash/dataframe?dataframe_id=' + modelCreateSelectedDF);
                                setModelCreateStep(1);
                            }}>Далее</DefaultButton>
                        </VStack>
                        : <ModelCreateModal dfID={modelCreateSelectedDF} onClose={onCloseModel} />}
                </ModalBody>
            </ModalContent>
        </Modal>

        <Modal isOpen={isOpenCompose} onClose={onCloseCompose} closeOnOverlayClick={false} size='3xl'>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalCloseButton boxSize='40px' transform='scale(1.5)' color='main.400' />

                <ModalBody bg='main.100'>
                    <ComposeCreateModal onClose={onCloseCompose} />
                </ModalBody>
            </ModalContent>
        </Modal>

        <Modal isOpen={isOpenUpload} onClose={onCloseUpload} closeOnOverlayClick={false} size='2xl'>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalCloseButton boxSize='40px' transform='scale(1.5)' color='main.400' />

                <ModalBody bg='main.100'>
                    <DataframeUploadModal onClose={onCloseUpload} />
                </ModalBody>
            </ModalContent>
        </Modal>
    </VStack>
}
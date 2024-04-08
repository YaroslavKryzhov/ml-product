'use client';

import { useDispatch, useSelector } from "@/redux/hooks";
import { VStack, Text, Drawer, DrawerBody, DrawerContent, DrawerHeader, DrawerOverlay, Flex, Icon, useDisclosure, Select, IconButton, HStack, Switch, Tooltip } from "@chakra-ui/react";
import { GoWorkflow } from 'react-icons/go';
import { useState, useEffect, useCallback } from 'react';
import { IDataframe, IJob, IModel } from "@/utils/types";
import { api, ease, getCustomDate } from "@/utils/misc";
import { DefaultButton } from ".";
import { FaChevronRight } from 'react-icons/fa6';
import { IoReload } from 'react-icons/io5';
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { setJobs } from "@/redux/dataframeSlice";
import { Easing, animate } from "framer-motion";

const colors = {
    'errored': 'red',
    'running': 'orange',
    'complete': 'green'
};

export function JobsMenu() {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const query = useSearchParams();
    const dispatch = useDispatch();
    const [mode, setMode] = useState('All');
    const { Authorization } = useSelector(state => state.misc);
    const { DFsList, modelsList, jobs } = useSelector(state => state.dataframe);

    const upd = useCallback(() => {
        api.get('/background_jobs/all', { headers: { Authorization } }).then(res => dispatch(setJobs(res.data)));
    }, [Authorization, dispatch]);

    useEffect(() => {
        if (!Authorization) return;
        upd();
        if (query.has('dataframe_id')) setMode(query.get('dataframe_id') ?? 'All');
    }, [Authorization, dispatch, query, upd]);

    const filteredJobs = (mode === 'All' ? jobs : jobs.filter((job: IJob) => job.object_id === mode)).toReversed();

    return <>
        <Flex
            pos='fixed' bottom='5vh' right='3vw' zIndex={10} opacity={0.75} justify='center' align='center' color='white' bg='main.400' borderRadius='200px' p='20px' transition='0.2s'
            _hover={{ cursor: 'pointer', bg: 'main.300', opacity: 1 }}
            onClick={() => {
                upd();
                onOpen();
            }}
            boxShadow='0px 0px 10px 0px rgba(111, 151, 229, 1)'
        >
            <Icon as={GoWorkflow} boxSize='30px' />
        </Flex>

        <Drawer
            isOpen={isOpen}
            placement='right'
            onClose={onClose}
            size='md'
        >
            <DrawerOverlay />
            <DrawerContent>
                <DrawerHeader bg='main.100'>
                    <HStack>
                        {/* <Tooltip label='Закрыть меню'> */}
                            <IconButton icon={<FaChevronRight />} onClick={onClose} fontSize='24px' aria-label='close jobs menu' bg='none' color='main.400' />
                        {/* </Tooltip> */}
                        <Tooltip label='Обновить список'>
                            <IconButton icon={<IoReload id='updButton' />} onClick={() => {
                                upd();
                                animate('#updButton', { transform: ['rotate(0deg)', 'rotate(360deg)'] }, { duration: 1, ease: ease as Easing });
                            }} fontSize='28px' aria-label='close jobs menu' bg='none' color='main.400' />
                        </Tooltip>

                        {/* <Switch isChecked={showOrphans} onChange={() => setShowOrphans(s => !s)} />
                        <Text fontSize='14px'>Показывать удалённые</Text> */}
                    </HStack>
                </DrawerHeader>

                <DrawerBody bg='main.100'>
                    <VStack w='100%' spacing='16px'>
                        <Select value={mode} bg='white' onChange={(e: any) => setMode(e.target.value)}>
                            <option value='All'>All</option>
                            {DFsList.map((df: IDataframe, i: number) => <option key={i} value={df._id}>{df.filename}</option>)}
                        </Select>

                        {filteredJobs.length > 0
                            ? filteredJobs.map((job: IJob, i: number) => {
                                const color = colors[job.status as keyof typeof colors];

                                return <VStack key={i} w='100%' bg='white' align='start' p='20px' borderRadius='15px' spacing='18px' pos='relative'>
                                    <Text pos='absolute' top='20px' right='20px' bg={color + '.300'} textAlign='center' p='10px 20px' borderRadius='200px' fontSize='16px' color='white'>{job.status}</Text>

                                    <VStack w='100%' align='start' spacing='12px' fontWeight={400}>
                                        <Text fontSize='22px' fontWeight={600}>{job.object_type}&apos;s Job</Text>
                                        <VStack align='start' borderLeft='2px solid' borderColor='main.300' py='4px' pl='10px'>
                                            <Text><b>Object name:</b> {DFsList.find((df: IDataframe) => df._id === job.object_id)?.filename ?? modelsList.find((model: IModel) => model._id === job.object_id)?.filename ?? job._id}</Text>
                                            <Text><b>Type:</b> {job.type}</Text>
                                            <Text><b>Started at:</b> {getCustomDate(job.started_at)}</Text>
                                            <Text><b>Finished at:</b> {getCustomDate(job.finished_at)}</Text>
                                        </VStack>
                                    </VStack>

                                    {(job.object_type === 'dataframe' ? DFsList.find((df: IDataframe) => df._id === job.object_id) : modelsList.find((model: IModel) => model._id === job.object_id))
                                        ? <Link href={'/dash/dataframe?dataframe_id=' + job.object_id}>
                                            <DefaultButton onClick={onClose}>Перейти к {job.object_type === 'dataframe' ? 'датафрейму' : 'модели'}</DefaultButton>
                                        </Link>
                                        : <Flex p='10px 20px' bg='orange.500' opacity={0.5} borderRadius='10px'><Text color='white' fontSize='14px'>Объект не найден</Text></Flex>}

                                    {job.input_params.method_params && <VStack w='100%' align='start' spacing='6px' fontWeight={400}>
                                        <Text fontSize='22px' fontWeight={600}>Params</Text>

                                        {job.input_params.method_params.map((method: any, i: number) => <VStack key={i} align='start' spacing='4px'>
                                            {Object.keys(method).map((key: string, j: number) => <Text key={j}>{key}: {method[key]}</Text>)}
                                        </VStack>)}
                                    </VStack>}

                                    {job.status !== 'running' && <VStack w='100%' align='start' spacing='10px' fontWeight={400}>
                                        <Text fontSize='22px' fontWeight={600} color={color + '.400'}>Output</Text>
                                        <Text borderLeft='2px solid' borderColor={color + '.300'} pl='10px'>{job.output_message}</Text>
                                    </VStack>}
                                </VStack>;
                            })
                            : <Text>no jobs for selected dataframe</Text>}
                    </VStack>
                </DrawerBody>
            </DrawerContent>
        </Drawer>
    </>
}
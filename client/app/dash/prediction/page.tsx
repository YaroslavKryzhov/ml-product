'use client';

import { Button, Divider, Flex, HStack, Icon, IconButton, Input, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, ModalOverlay, SimpleGrid, Spinner, Stack, Text, useDisclosure, useToast, VStack } from "@chakra-ui/react";
import { BiSolidRightArrow } from "react-icons/bi";
import { DefaultButton } from "@/components/Common";
import { HiOutlineDownload } from "react-icons/hi";
import { api, errToast, getCustomDate, successToast } from "@/utils/misc";
import { nextPage, prevPage, setCurrentValues, setPage } from "@/redux/dataframeSlice";
import { IPrediction } from "@/utils/types";
import { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "@/redux/hooks";
import { useRouter, useSearchParams } from "next/navigation";
import { DeleteIconButton } from "@/components";
import { Suspense } from 'react';
import { FaCheck } from "react-icons/fa6";

export default function DF_selected() {
    const [newFilename, setNewFilename] = useState('');
    const { isOpen: isOpenDelete, onOpen: onOpenDelete, onClose: onCloseDelete } = useDisclosure();
    const { page, currentValues, pagesCount } = useSelector(state => state.dataframe);
    const dispatch = useDispatch();
    const query = useSearchParams()!;
    const toast = useToast();
    const router = useRouter();
    const { Authorization } = useSelector(state => state.misc);

    const prediction_id = query.get('prediction_id');
    const [saveLoading, setSaveLoading] = useState(false);
    const [dataframe, setDataframe] = useState<IPrediction | null>(null);

    const updateDFContent = useCallback((page: number) => {
        api.get(`/dataframe/content?dataframe_id=${prediction_id}&page=${page + 1}&rows_on_page=20`, { headers: { Authorization } })
            .then(res => dispatch(setCurrentValues(res.data)))
            .catch(err => errToast(toast, err));
    }, [Authorization, dispatch, toast, prediction_id]);

    useEffect(() => {
        if (!Authorization) return;
        updateDFContent(0);

        api.get('/dataframe/metadata?dataframe_id=' + prediction_id, { headers: { Authorization } })
            .then(res => {
                setDataframe(res.data);
                setNewFilename(res.data.filename);
            });
    }, [Authorization, prediction_id, updateDFContent]);

    return dataframe ? <Suspense fallback={<></>}>
        <HStack spacing='8px' fontSize='18px' fontWeight={400} p='10px 14px' borderRadius='10px' bg='main.100'>
            {document.getElementById('tree_' + prediction_id) &&
                JSON.parse(document.getElementById('tree_' + prediction_id)?.innerHTML ?? '[]').map((parent: string, i: string) => <HStack key={i} spacing='8px'>
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
                            // dispatch(renameDataframe([dataframe.filename, newFilename]));
                        })
                        .catch(err => errToast(toast, err));
                }} />}

                <Text ml='18px' fontSize='14px' letterSpacing='0.5px' fontWeight={300} opacity={0.5}>Создано {getCustomDate(dataframe.created_at)}</Text>
            </VStack>

            <HStack spacing={0}>
                {/* @ts-ignore */}
                <DefaultButton isLoading={saveLoading} onClick={() => {
                    setSaveLoading(true);
                    api.put(`/dataframe/edit/move_to_active?model_id=${query.get('model_id')}&dataframe_id=${prediction_id}&new_filename=active_${encodeURIComponent(dataframe.filename)}`, {}, { headers: { Authorization } })
                        .then(res => {
                            router.push('/dash/dataframe?dataframe_id=' + res.data._id);
                        })
                        .catch(err => errToast(toast, err));
                }}>Сохранить как новый датафрейм</DefaultButton>

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

        <VStack w='100%' spacing='14px' align='start' bg='main.100' borderRadius={6} p='14px'>
            <VStack w='100%' spacing='24px' align='start' overflowX='auto'>
                <HStack spacing={0} align='start'>
                    {Object.keys(currentValues).map((x: string, i: number) => {
                        return <VStack w='max-content' key={i} spacing={0} borderTop='1px solid' borderLeft={i === 0 ? '1px solid' : 'none'} borderBottom='1px solid' borderRight='1px solid' borderColor='gray.400'>
                            <VStack w='100%' align='start' p='10px' bg='white'>
                                <Text>{x}</Text>
                            </VStack>

                            <VStack w='100%' fontSize='16px' spacing='4px' bg='white' borderTop='1px solid' borderColor='gray.400'>
                                {currentValues[x] && currentValues[x].map((value: string, i: number) => <VStack key={i} w='100%' h='30px'>
                                    <Divider w='100%' borderColor={i > 0 ? 'gray.400' : 'transparent'} />
                                    <Text w='100%' px='10px' fontFamily='Roboto Mono Variable' fontSize='13px' fontWeight={400} color='black'>{isNaN(parseFloat(value)) ? value : Math.round(parseFloat(value) * 10000) / 10000}</Text>
                                </VStack>)}
                            </VStack>
                        </VStack>;
                    })}
                </HStack>
            </VStack>

            <SimpleGrid columns={17} spacing='8px'>
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
            </SimpleGrid>
        </VStack>

        <Modal isOpen={isOpenDelete} onClose={onCloseDelete}>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalHeader>Удаление предсказания</ModalHeader>
                <ModalBody>
                    <Text>Вы уверены, что хотите удалить предсказание <b>{dataframe.filename}</b>?</Text>
                </ModalBody>
                <ModalFooter>
                    <HStack spacing='12px'>
                        <Button onClick={onCloseDelete}>Оставить</Button>
                        <Button bg='red.500' onClick={() => {
                            api.delete(`/dataframe/prediction?prediction_id=${dataframe._id}&model_id=${dataframe.parent_id}`, { headers: { Authorization } }).then(res => {
                                onCloseDelete();
                                if (res.status === 200) {
                                    successToast(toast, `Предсказание ${dataframe.filename} удалено!`);
                                    router.push('/dash');
                                } else errToast(toast, res);
                            });
                        }}>Удалить</Button>
                    </HStack>
                </ModalFooter>
            </ModalContent>
        </Modal>
    </Suspense> : <Flex w='100%' h='400px' justify='center' align='center'><Spinner size='xl' colorScheme='blue' transform='scale(3)' /></Flex>
}
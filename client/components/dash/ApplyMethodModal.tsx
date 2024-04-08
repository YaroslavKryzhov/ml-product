'use client';
import { Accordion, AccordionButton, AccordionIcon, AccordionItem, AccordionPanel, Checkbox, HStack, Input, Text, useToast, VStack } from "@chakra-ui/react";
import { DefaultButton } from "@/components/Common";
import { useState } from "react";
import { checkFeature, deselectMethod, selectMethod } from "@/redux/methodApplySlice";
import { useDispatch, useSelector } from "@/redux/hooks";
import { IAppliedMethod, IRawMethod, methods } from "@/utils/types";
import { api, errToast, successToast } from "@/utils/misc";
import { useSearchParams } from "next/navigation";
import { setJobs } from "@/redux/dataframeSlice";
import { AppliedMethodTypes } from "@/utils/enums";

export function ApplyMethodModal({ features, df_name, onClose }: { features: any[], df_name: string, onClose: any }) {
    const dispatch = useDispatch();
    const toast = useToast();
    const query = useSearchParams();
    const { res } = useSelector(state => state.methodApply);
    const { Authorization } = useSelector(state => state.misc);
    const [selectedMethod, setSelectedMethod] = useState<IRawMethod | null>(null);

    return <VStack w='100%' align='start' py='20px' spacing='20px'>
        <Text fontSize='30px' fontWeight={700} letterSpacing='1px'>Методы</Text>
        <Text fontWeight={400} fontSize='14px'>Можно выбрать удалить все дублированные записи из датафрейма, улучшая тем самым качество данных и избавляясь от возможных искажений в анализе.</Text>

        <VStack w='100%' align='start' spacing='20px'>
            <HStack w='100%' justify='space-between'>
                <VStack w='70%' align='start' spacing='14px'>
                    <VStack w='90%' align='start'>
                        <Text>Название нового датафрейма</Text>
                        <Input w='100%' borderColor='gray' _hover={{ borderColor: 'gray.400' }} defaultValue={`${df_name}_modified`} id='modifiedDFname' />
                    </VStack>

                    <Accordion w='100%' defaultIndex={[0]} allowMultiple>
                        {Object.values(AppliedMethodTypes)
                            // .filter((mType: string) => methods.filter((method: IRawMethod) => method.type === mType).length > 0)
                            .map((mType: string, i: number) => <AccordionItem key={i}>
                                <AccordionButton>
                                    <HStack spacing='6px' fontWeight={600}>
                                        <AccordionIcon />
                                        <Text>{mType}</Text>
                                    </HStack>
                                </AccordionButton>

                                <AccordionPanel>
                                    <VStack align='start'>
                                        {methods
                                            .filter((method: IRawMethod) => method.type === mType)
                                            .map((method: IRawMethod, i: number) => {
                                                const isSelected = () => res.findIndex((m: IAppliedMethod) => m.method_name === method.method_name) > -1;

                                                return <VStack key={i}>
                                                    <HStack userSelect='none' fontWeight={selectedMethod?.method_name === method.method_name ? 600 : 400} color={selectedMethod?.method_name === method.method_name ? 'main.400' : 'black'} spacing='10px'>
                                                        <Checkbox isChecked={isSelected()} key={i} onChange={() => {
                                                            if (isSelected()) {
                                                                dispatch(deselectMethod(method));
                                                                setSelectedMethod(null);
                                                            } else {
                                                                dispatch(selectMethod(method));
                                                                setSelectedMethod(method);
                                                            }
                                                        }} />
                                                        <Text _hover={{ cursor: 'pointer', color: 'main.400' }} transition='0.1s' userSelect='none' onClick={() => {
                                                            setSelectedMethod(method);
                                                            if (!isSelected()) dispatch(selectMethod(method));
                                                        }}>{method.literal}</Text>
                                                    </HStack>
                                                    {selectedMethod?.method_name === method.method_name && method.method_name === 'fill_custom_value' && <Input id='customValue' placeholder='Custom value to fill with' />}
                                                </VStack>;
                                            })}
                                    </VStack>
                                </AccordionPanel>
                            </AccordionItem>)}
                    </Accordion>

                    {/* @ts-ignore */}
                    <DefaultButton isDisabled={res.length <= 0} mt='10px' onClick={() => {
                        api.post(
                            '/dataframe/edit/apply_method?' + `dataframe_id=${query.get('dataframe_id')}&new_filename=${(document.getElementById('modifiedDFname') as HTMLInputElement | undefined)?.value ?? ''}`,
                            // TODO: custom value in params
                            res.map((m: IAppliedMethod) => ({ method_name: m.method_name, columns: m.columns, params: {} })),
                            { headers: { Authorization } }
                        )
                            .then(res => {
                                onClose();
                                successToast(toast, res.data.message);
                                api.get('/background_jobs/all', { headers: { Authorization } }).then(res => dispatch(setJobs(res.data)));
                            })
                            .catch(err => errToast(toast, err));
                    }}>Применить методы</DefaultButton>
                </VStack>

                {selectedMethod && <VStack w='100%' align='start' bg='white' p='14px' borderRadius='6px' overflow='auto'>
                    <Text fontWeight={600}>Применить метод <span style={{ color: '#5385E5' }}>{selectedMethod.method_name}</span> к признакам</Text>
                    {features.map((feature: string, i: number) => {
                        const typeApplied = res.findIndex((d: IAppliedMethod) =>
                            d.method_name !== selectedMethod.method_name &&
                            d.type as unknown === selectedMethod.type &&
                            d.columns.includes(feature)
                        ) > -1;

                        return <Checkbox key={i} opacity={typeApplied ? 0.5 : 1} isChecked={res.find((d: IAppliedMethod) => d.method_name === selectedMethod.method_name)?.columns.includes(feature) ?? false} onChange={() => {
                            if (typeApplied) errToast(toast, `Метод типа ${selectedMethod.type} уже применён к этому признаку!`);
                            else dispatch(checkFeature({ method: selectedMethod, feature }));
                        }}>{feature}</Checkbox>;
                    })}
                </VStack>}
            </HStack>
        </VStack>
    </VStack>
}
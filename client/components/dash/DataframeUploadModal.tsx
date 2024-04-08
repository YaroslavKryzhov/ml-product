'use client';

import { Input, Text, useToast, VStack } from "@chakra-ui/react";
import { ChangeEvent, useRef, useState } from "react";
import { DefaultButton } from "@/components/Common";
import { api, errToast, genHash, successToast } from "@/utils/misc";
import { addDataframe } from "@/redux/dataframeSlice";
import { useDispatch, useSelector } from "@/redux/hooks";
import { useRouter } from "next/navigation";

export function DataframeUploadModal({ onClose }: { onClose: any }) {
    const [initName, setInitName] = useState('');
    const [newDfName, setNewDfName] = useState('');
    const file = useRef(new FormData());
    const dispatch = useDispatch();
    const toast = useToast();
    const router = useRouter();
    const { Authorization } = useSelector(state => state.misc);

    return <VStack w='100%' align='start' py='20px' spacing='20px'>
        <Text fontSize='30px' fontWeight={700} letterSpacing='1px'>Методы</Text>

        <VStack align='start' spacing='30px'>
            <VStack align='start' spacing='8px'>
                <Text letterSpacing='1px'>Название</Text>
                <Input value={newDfName} onChange={(e: ChangeEvent<HTMLInputElement>) => setNewDfName(e.target.value)} placeholder='Введите название датафрейма' _placeholder={{ color: 'rgb(140, 156, 176)' }} w='250px' borderColor='rgb(235, 241, 248)' />
            </VStack>

            <label className="input-file">
                <input type='file' onChange={(e: ChangeEvent<HTMLInputElement>) => {
                    if (e.target.files) {
                        setInitName(e.target.files[0].name);
                        setNewDfName(e.target.files[0].name);
                        file.current.append('file', e.target.files[0]);
                    }
                }} />
                <span style={{ border: 'dashed 3px', borderRadius: '100px', padding: '20px 50px', borderColor: '#5385E5', opacity: initName.length > 0 ? 1 : 0.6, fontSize: '14px', color: 'rgba(0,0,0,0.8)', fontWeight: 500 }}>
                    {initName.length > 0
                        ? <span style={{ fontSize: '17px' }} className='mainBlueColor'>{initName}</span>
                        : <span>Перетащите файл или нажмите чтобы <span className='mainBlueColor'>загрузить</span></span>}
                </span>
            </label>

            {/* @ts-ignore */}
            <DefaultButton isDisabled={newDfName.length <= 0} onClick={() => {
                api
                    .post(
                        '/dataframe?filename=' + (newDfName.length > 0 ? newDfName : genHash(10)),
                        file.current,
                        {
                            headers: {
                                'Content-Type': 'multipart/form-data',
                                Authorization
                            }
                        }
                    )
                    .then(res => {
                        if (res.status === 200) {
                            successToast(toast, `Датафрейм ${res.data.filename} загружен!`);
                            dispatch(addDataframe(res.data));
                            router.push('/dash/dataframe?dataframe_id=' + res.data._id);
                            onClose();
                        } else errToast(toast, res);
                    })
                    .catch(err => errToast(toast, err));
                // setHave(true);
            }}>Загрузить</DefaultButton>
        </VStack>
    </VStack>
}
'use client';

import {
    HStack, Input, InputGroup, InputRightElement, Stack, Text, VStack, useDisclosure, Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    Button,
    useToast,
    Flex,
    Icon,
    IconButton
} from "@chakra-ui/react";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { api, errToast } from "@/utils/misc";
import { setToken } from "@/redux/miscSlice";
import { useDispatch } from "@/redux/hooks";
import { DefaultButton } from "@/components/Common";
import { FaRegEye, FaRegEyeSlash } from "react-icons/fa6";

const inputStyles = (error: boolean) => ({
    w: '100%',
    borderRadius: 6,
    p: '8px 16px',
    focusBorderColor: 'main.400',
    transition: '0.3s',
    borderColor: error ? 'error.400' : "#e2e2e2",
    _placeholder: {
        color: error ? 'error.200' : 'main.500',
        fontSize: '13px',
        lineHeight: '16px'
    }
});

function authenticate(username: string, password: string) {
    return api.post('/auth/login', `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
}

const Form = (
    { authData, error, setError, setAuthData }:
        { authData: string[], error: boolean, setError: (_: boolean) => void, setAuthData: (_: any) => void }
) => {
    const [reveal, setReveal] = useState(false);

    return <VStack w='100%' pos='relative'>
        {!error && authData[1].length > 0 &&
            <IconButton pos='absolute' bottom='2px' right='2px' zIndex={1} _hover={{ cursor: 'pointer' }} _active={{ color: 'blue.600' }} onClick={() => setReveal(s => !s)} bg='none' icon={reveal ? <FaRegEye /> : <FaRegEyeSlash />} fontSize='18px' color='main.400' aria-label='reveal' />}

        {['Почта', 'Пароль'].map((field: string, i) => <InputGroup key={i} justifyContent='center'>
            <Input type={i === 0 || reveal ? 'text' : 'password'} onFocus={() => setError(false)} value={authData[i]} onChange={event => setAuthData((s: string[]) => {
                if (i === 0) return [event.target.value, s[1]];
                else return [s[0], event.target.value];
            })} placeholder={error ? 'Неверные данные' : field} {...inputStyles(error)} />

            <InputRightElement transition='0.3s' opacity={error ? 1 : 0}>
                <svg width='16' height='17' viewBox='0 0 16 17' fill='none' xmlns='http://www.w3.org/2000/svg'>
                    <g clipPath='url(#clip0_715_43623)'>
                        <path d='M1 8.5C1 4.63401 4.13401 1.5 8 1.5C11.866 1.5 15 4.63401 15 8.5C15 12.366 11.866 15.5 8 15.5C4.13401 15.5 1 12.366 1 8.5Z' stroke='#FF2222' strokeWidth='2' />
                        <rect x='7' y='10.5' width='2' height='2' rx='1' fill='#FF2222' />
                        <line x1='8' y1='5.5' x2='8' y2='8.5' stroke='#FF2222' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' />
                    </g>
                    <defs>
                        <clipPath id='clip0_715_43623'>
                            <rect width='16' height='16' fill='white' transform='translate(0 0.5)' />
                        </clipPath>
                    </defs>
                </svg>
            </InputRightElement>
        </InputGroup>)}
    </VStack>;
};

export default function AuthPage() {
    const dispatch = useDispatch();
    const router = useRouter();
    const toast = useToast();
    const [error, setError] = useState(false);
    const [authData, setAuthData] = useState(['', '']);
    const [loading, setLoading] = useState(false);
    const { isOpen, onOpen, onClose } = useDisclosure();

    const auth = useCallback(() => {
        setLoading(true);
        authenticate(authData[0], authData[1])
            .then(res => {
                localStorage.setItem('ml_token', res.data.access_token);
                dispatch(setToken(res.data.access_token));
                router.replace('/dash');
            })
            .catch(() => {
                setLoading(false);
                setError(true);
                setAuthData([authData[0], '']);
                setTimeout(() => setError(false), 2000);
            });
    }, [authData, dispatch, router]);

    useEffect(() => {
        router.prefetch('/dash');
        window.onkeydown = (e: any) => {
            if (e.key === 'Enter') auth();
        }
    }, [auth, router]);

    return <>
        <VStack p='24px' w='max-content' borderRadius={6} spacing='16px' boxShadow='0px 4px 16px 0px rgba(0, 0, 0, 0.15)'>
            <Form error={error} setError={setError} authData={authData} setAuthData={setAuthData} />

            <HStack w='100%' spacing='16px'>
                {/* @ts-ignore */}
                <DefaultButton onClick={auth} h='32px' w='96px' fontWeight={400} isLoading={loading}>Войти</DefaultButton>

                <Flex onClick={onOpen} h='32px' w='135px' borderRadius={6} border='solid 1px' borderColor='main.400' justify='center' align='center' _hover={{ cursor: 'pointer' }}>
                    <Text color='main.400' fontSize='14px'>Регистрация</Text>
                </Flex>
            </HStack>
        </VStack>

        <Modal isCentered isOpen={isOpen} onClose={onClose}>
            <ModalOverlay backdropFilter='blur(2px)' />
            <ModalContent>
                <ModalHeader>Регистрация</ModalHeader>
                <ModalCloseButton />
                <ModalBody display='flex' flexDir='row' justifyContent='center'>
                    <Form error={error} setError={setError} authData={authData} setAuthData={setAuthData} />
                </ModalBody>

                <ModalFooter>
                    {/* @ts-ignore */}
                    <DefaultButton isLoading={loading} onClick={() => {
                        setLoading(true);
                        api.post('/auth/register', { email: authData[0], password: authData[1] })
                            .then(auth)
                            .catch(err => {
                                errToast(toast, err);
                                setLoading(false);
                            });
                    }}>Зарегистрироваться</DefaultButton>
                </ModalFooter>
            </ModalContent>
        </Modal>
    </>
}

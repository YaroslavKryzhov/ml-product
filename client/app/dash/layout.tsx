'use client';
import { LeftMenu } from "@/components/dash";
import { Button, HStack, VStack } from "@chakra-ui/react";
import { JobsMenu } from '@/components/Common';
import Link from "next/link";

export const dynamic = 'force-dynamic';

export default function DashLayout({ children }: { children: React.ReactNode }) {
    return <HStack w='100vw' minH='100vh' p='20px' align='start' spacing='1vw' fontWeight={600}>
        <LeftMenu />
        <JobsMenu />

        <VStack py='20px' spacing='24px' align='start' minW='900px' w='74vw' overflowX='auto'>{children}</VStack>

        <Link href='/'>
            <Button
                variant='outline' pos='fixed' top='20px' right='30px' colorScheme='blue'
                fontWeight={400} opacity={0.5} _hover={{ opacity: 1 }} onClick={() => localStorage.removeItem('ml_token')}
            >Выйти</Button>
        </Link>
    </HStack>
}

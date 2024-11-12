import { ReactNode } from "react";
import { Button, HStack, Icon, Text } from "@chakra-ui/react";
import { FaPlus } from "react-icons/fa6";

export const AddButton = (
    { children, onClick, ...rest }: { children: ReactNode, onClick: () => void, rest?: any }
) => <Button {...rest} onClick={onClick} border='1px solid' borderColor='main.400' bg='none' borderRadius='6px' p='9px 30px'>
        <HStack spacing='9px' color='main.400'>
            <Icon as={FaPlus} boxSize='12px' transform='translateY(-1px)' />
            <Text fontSize='14px' lineHeight='14px' transform='translateY(1px)'>{children}</Text>
        </HStack>
    </Button>;

export const DefaultButton = (
    { children, onClick, ...rest }: { children: ReactNode, onClick: () => void, rest?: any }
) => <Button {...rest} onClick={onClick} bg='main.400' borderRadius='6px' p='9px 30px' color='white' transition='0.1s' _hover={{ bg: 'main.300' }}>
        <Text fontSize='14px'>{children}</Text>
    </Button>;
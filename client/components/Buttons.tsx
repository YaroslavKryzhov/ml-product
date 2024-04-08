import { FaRegTrashAlt } from "react-icons/fa";
import { IconButton } from "@chakra-ui/react";

export function DeleteIconButton({ exec }: { exec: () => void }) {
    return <IconButton aria-label='delete' icon={<FaRegTrashAlt />} fontSize='25px' color='main.400' bg='none' onClick={exec} _hover={{ cursor: 'pointer' }} _active={{}} />
}
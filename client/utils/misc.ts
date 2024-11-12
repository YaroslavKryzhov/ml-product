import axios from "axios";

export const ease = [0.410, 0.030, 0.000, 0.995];

// export const baseURL = true
//     ? 'http://127.0.0.1:8006/api/v1'
//     : 'http://demo-ml-app.winnerok.tk:8006/api/v1';
export const baseURL = 'http://127.0.0.1:8006/api/v1';


export const api = {
    get: async (url: string, config: any = {}) => await axios.get(baseURL + url, config),
    post: async (url: string, body: any, config: any = {}) => await axios.post(baseURL + url, body, config),
    put: async (url: string, body: any = {}, config: any = {}) => await axios.put(baseURL + url, body, config),
    delete: async (url: string, config: any = {}) => await axios.delete(baseURL + url, config)
};

export function arrToChunks(array: any[], size: number) {
    const res = [];
    for (let i = 0; i < array.length; i += size) {
        const chunk = array.slice(i, i + size);
        res.push(chunk);
    }
    return res;
}

export function getCustomDate(init: string | undefined) {
    if (!init) return '';
    const date = new Date(init);
    const dd = (x: number) => x < 10 ? `0${x}` : `${x}`;
    return `${dd(date.getUTCDate())}.${dd(date.getUTCMonth() + 1)}.${dd(date.getUTCFullYear())} в ${dd(date.getUTCHours() + 3)}:${dd(date.getUTCMinutes())}`;
}

export const errToast = (toast: any, err: any) => {
    console.error(err);

    if (typeof err === 'string') toast({
        title: 'Ошибка',
        description: err,
        status: 'error',
        duration: 5000,
        isClosable: true
    });
    else if (err.response) toast({
        title: err.response.statusText ?? 'Ошибка',
        description: err.response.data.detail[0]?.msg ?? err.response.data.detail,
        status: 'error',
        duration: 5000,
        isClosable: true
    });
}

export const successToast = (toast: any, text: any) => {
    toast({
        title: 'Успешно',
        description: text,
        status: 'success',
        duration: 6000,
        isClosable: true
    });
}

export function genHash(length: number) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < length; i++) result += characters.charAt(Math.floor(Math.random() * characters.length));
    return result;
}
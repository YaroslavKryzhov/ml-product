'use client';

import { setIsLaptop, setToken } from "@/redux/miscSlice";
import { useCallback, useEffect, useRef } from "react";
import { useDispatch, useSelector } from '@/redux/hooks';
import { useRouter, useSearchParams } from "next/navigation";
import { api, ease, errToast } from "@/utils/misc";
import { useToast } from "@chakra-ui/react";
import { motion } from 'framer-motion';
import Centrifuge from 'centrifuge';
import { setDataframes, setModels, setTree, updateJob } from "@/redux/dataframeSlice";

export function Launcher() {
    const dispatch = useDispatch();
    const router = useRouter();
    const toast = useToast();
    const query = useSearchParams();
    const ws = useRef<Centrifuge | null>(null);
    const { isLaptop, Authorization } = useSelector(state => state.misc);

    useEffect(() => {
        dispatch(setIsLaptop(!window.matchMedia("(max-width: 600px)").matches));

        try {
            const token = localStorage.getItem('ml_token') ?? '';
            dispatch(setToken(token));

            api.get('/auth/centrifugo_token', { headers: { Authorization: `Bearer ${token}` } }).then(res => {
                if (ws.current) return;

                ws.current = new Centrifuge("ws://demo-ml-app.winnerok.tk:8006/centrifugo/connection/websocket");
                ws.current.setToken(res.data.token);

                ws.current.on('connect', (ctx: any) => {
                    console.log("connected", ctx);
                });

                ws.current.on('disconnect', (ctx: any) => {
                    console.log("disconnected", ctx);
                });

                ws.current.subscribe("INFO#" + res.data.user_id, (ctx: any) => {
                    toast({ status: 'info', title: 'Job update', description: 'Check the jobs menu in the bottom right corner!', duration: 5000, isClosable: true })
                    dispatch(updateJob(ctx.data));

                    console.log(ctx.data);
                    
                    api.get('/dataframe/metadata/trees', { headers: { Authorization: `Bearer ${token}` } }).then(res => dispatch(setTree(res.data)));
                    
                    // TODO: && ctx.data.object_type === 'model'
                    if (query.has('dataframe_id')) api.get('/model/metadata/by_dataframe?dataframe_id=' + query.get('dataframe_id'), { headers: { Authorization: `Bearer ${token}` } })
                        .then(res => dispatch(setModels(res.data)))
                        .catch(err => errToast(toast, err));
                });

                ws.current.connect();
            }).catch(() => { });
        } catch (_) {
            router.push('/');
        }
    }, [router, dispatch, toast, Authorization, query]);

    return <>
        <motion.div
            style={{ width: '100vw', height: '100vh', position: 'fixed', top: 0, left: 0, zIndex: 10000, background: 'white', pointerEvents: 'none' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: isLaptop === null ? 1 : 0 }}
            transition={{ delay: 0.2, duration: 0.2, ease }}
        />
    </>
}
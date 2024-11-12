'use client';
import { CacheProvider } from '@chakra-ui/next-js';
import { checkboxAnatomy } from '@chakra-ui/anatomy';
import { ChakraProvider, defineStyleConfig, extendTheme, createMultiStyleConfigHelpers } from '@chakra-ui/react';
import { Provider } from "@/redux/provider";
import '@fontsource-variable/roboto-mono';

const { definePartsStyle, defineMultiStyleConfig } = createMultiStyleConfigHelpers(checkboxAnatomy.keys);

export function Providers({ children }: { children: React.ReactNode }) {
    return <Provider>
        <CacheProvider>
            <ChakraProvider theme={extendTheme({
                colors: {
                    main: {
                        100: '#F2F9FB',
                        200: '#D6E1F8',
                        300: '#6f97e5',
                        400: '#5385E5',
                        500: '#8C9CB0'
                    },
                    error: {
                        200: '#f56a6a',
                        400: '#FF0202'
                    }
                },
                components: {
                    Text: defineStyleConfig({
                        baseStyle: {
                            lineHeight: '100%'
                        }
                    }),
                    Checkbox: defineMultiStyleConfig({
                        baseStyle: definePartsStyle({
                            control: {
                                borderRadius: '6px',
                                outline: '1px solid #d9d9d9',
                                _checked: {
                                    bg: '#5385E5'
                                }
                            }
                        }),
                        defaultProps: {
                            size: 'lg'
                        }
                    })
                }
            })}>
                {children}
            </ChakraProvider>
        </CacheProvider>
    </Provider>
}
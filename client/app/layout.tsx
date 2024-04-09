import '@/app/globals.css';
import { Providers } from "@/app/providers";
import { Launcher } from "@/components/Common";
import type { Metadata } from "next";
import localFont from 'next/font/local';

export const metadata: Metadata = {
    description: 'ML Builder',
    title: 'Конструктор ML'
}

const circe = localFont({ src: './CirceRounded-Regular.woff2' });

export default function RootLayout({ children }: { children: React.ReactNode }) {
    return <html lang='en'>
        <body className={circe.className}>
            <Providers>
                <Launcher />

                <main style={{ alignItems: 'center', display: 'flex', flexDirection: 'column', justifyContent: 'center', minHeight: '90vh', width: '100%' }}>
                    {children}
                </main>
            </Providers>
        </body>
    </html>
}

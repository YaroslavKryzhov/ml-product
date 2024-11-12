'use client';

export function Icons({ isExpanded }: { isExpanded: boolean }) {
    return <svg width='40' height='30' viewBox='0 0 40 30' fill='none' xmlns='http://www.w3.org/2000/svg'>
        <path d={isExpanded ? 'M30 20L20 10L10 20' : 'M10 10L20 20L30 10'} stroke='#8C9CB0' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' />
    </svg>;
}
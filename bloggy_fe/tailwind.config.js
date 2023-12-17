/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
    content: [
        './index.html',
        '../bloggy/templates/**/*.html',
        './src/**/*.{vue,js,ts,jsx,tsx,json}',
        './src/*.{vue,js,ts,jsx,tsx,json}',
        "./node_modules/flowbite/**/*.js"
    ],
    theme: {
        extend: {
            colors: {
                'primary': '#068bea',
                'secondary': '#394455'
            },
            screens: {
                'sm': '640px',
                'md': '768px',
                'lg': '1024px',
                'xl': '1200px',
                '2xl': '1200px',
                // '2xl': '1320px',
            },
            fontFamily: {
                // sans: ['Inter var', ...defaultTheme.fontFamily.sans],
                // sans: ['Albert Sans', 'Outfit', 'ui-sans-serif', 'system-ui', ...defaultTheme.fontFamily.sans],
                // serif: ['Albert Sans', 'Outfit', 'ui-serif', 'Georgia', ...defaultTheme.fontFamily.serif],
                // display: ['Playfair Display', 'Outfit', ...defaultTheme.fontFamily.sans],
                // body: ['Albert Sans', 'Outfit', ...defaultTheme.fontFamily.sans],
                // playfair: ['Playfair Display', ...defaultTheme.fontFamily.sans],
            },
        },
    },
    plugins: [
        require('flowbite-typography'),
        require('flowbite/plugin'),
        require('@tailwindcss/typography'),
    ],
}
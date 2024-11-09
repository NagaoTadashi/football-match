// https://nuxt.com/docs/api/configuration/nuxt-config
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify';

export default defineNuxtConfig({
    compatibilityDate: '2024-04-03',
    devtools: { enabled: true },
    ssr: false,
    app: {
        head: {
            title: 'Web League',
            meta: [
                { charset: 'utf-8' },
                {
                    name: 'viewport',
                    content: 'width=device-width, initial-scale=1',
                },
            ],
            link: [
                { rel: 'icon', type: 'image/png', href: '/favicon.png' }, // これを追記する
            ],
        },
    },
    build: {
        transpile: ['vuetify'],
    },
    modules: [
        (_options, nuxt) => {
            nuxt.hooks.hook('vite:extendConfig', (config) => {
                // @ts-expect-error
                config.plugins.push(vuetify({ autoImport: true }));
            });
        },
        'nuxt-vuefire',
    ],
    vite: {
        vue: {
            template: {
                transformAssetUrls,
            },
        },
    },
    runtimeConfig: {
        public: {
            apiUrl: process.env.NUXT_PUBLIC_API_URL || '',
        },
    },
    vuefire: {
        auth: {
            enabled: true,
        },
        config: {
            projectName: process.env.PROJECT_NAME,
            projectId: process.env.PROJECT_ID,
            projectNumber: process.env.PROJECT_NUMBER,
            apiKey: process.env.API_KEY,
            authDomain: process.env.AUTH_DOMAIN,
            storageBucket: process.env.STORAGE_BUCKET,
            messagingSenderId: process.env.MESSAGING_SENDER_ID,
            appId: process.env.APP_ID,
            measurementId: process.env.MEASUREMENT_ID,
        },
    },
});

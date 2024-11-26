<script setup>
import { ref } from 'vue';

const visible = ref(false);

const isChrome = ref(false);

// Chromeで開くリンクのURL
const chromeLink = 'googlechrome://web-league.com/'; // ログインページのURLに置き換え

// 初期化時にブラウザ判定
if (typeof window !== 'undefined') {
    const userAgent = navigator.userAgent;
    const isIOS = /iPhone|iPad|iPod/.test(userAgent); // iOS端末かどうかを判定
    const isChromeOnIOS = /CriOS/.test(userAgent); // iOSのChromeを判定

    // iOSでない場合、Chromeを検出
    if (!isIOS) {
        isChrome.value =
            /Chrome/.test(userAgent) &&
            /Google Inc/.test(navigator.vendor) &&
            !/Edg/.test(userAgent); // EdgeブラウザもChromeベースなので除外
    } else {
        // iOSの場合、CriOSが含まれていればChromeとみなす
        isChrome.value = isChromeOnIOS;
    }
}
</script>

<template>
    <div>
        <div class="text-center mx-auto my-6" max-width="230" text>
            <h1><v-icon>mdi-soccer</v-icon> Web League</h1>
        </div>

        <div v-if="!isChrome">
            <div class="text-center">
                <v-btn
                    :href="chromeLink"
                    target="_blank"
                    class="no-uppercase"
                    prepend-icon="mdi-google-chrome"
                    text="Chromeで開く"
                ></v-btn>
            </div>
        </div>
        <div v-else>
            <v-card
                class="mx-auto pa-12 pb-8"
                elevation="8"
                max-width="450"
                rounded="lg"
            >
                <v-card class="mb-12" color="surface-variant" variant="tonal">
                    <v-card-text class="text-medium-emphasis text-caption">
                        <v-icon>mdi-information-outline</v-icon>
                        本サービスはチーム単位での利用を想定しています。チームごとに1つのGoogleアカウントを用意し、ログインしてください。
                    </v-card-text>
                </v-card>

                <slot />
            </v-card>
        </div>
    </div>
</template>

<style>
.no-uppercase {
    text-transform: none;
}
</style>

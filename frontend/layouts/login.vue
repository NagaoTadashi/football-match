<script setup>
import { ref } from 'vue';

const visible = ref(false);
</script>

<template>
    <div>
        <div>
            <div class="text-center mx-auto my-6" max-width="228" text>
                <h1><v-icon>mdi-soccer</v-icon> Football Match</h1>
            </div>

            <v-card
                class="mx-auto pa-12 pb-8"
                elevation="8"
                max-width="448"
                rounded="lg"
            >
                <v-card class="mb-12" color="surface-variant" variant="tonal">
                    <v-card-text class="text-medium-emphasis text-caption">
                        <v-icon>mdi-information-outline</v-icon>
                        チームで1つのGoogleアカウントを用意してください
                    </v-card-text>
                </v-card>

                <slot />
            </v-card>
        </div>
    </div>
</template>

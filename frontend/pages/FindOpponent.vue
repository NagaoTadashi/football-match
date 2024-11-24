<script setup>
import { shallowRef } from 'vue';
import { useDisplay } from 'vuetify';

const user = await getCurrentUser();
const idToken = await user.getIdToken();

const runtimeConfig = useRuntimeConfig();

const { smAndUp } = useDisplay();

const teamsDialog = ref(false);
const applicationsDialog = ref(false);
const cancelDialog = ref(false);
const xsErrorDialog = ref(false);
const mdErrorDialog = ref(false);

const cancelApplicationId = ref(null);

const search = shallowRef('');

const applications = ref([]);

const img_url =
    'https://cdn.pixabay.com/photo/2015/07/02/00/08/football-828218_1280.jpg';

const { data: registeredTeams } = await useFetch(
    `${runtimeConfig.public.apiUrl}/registered_teams/`,
    {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${idToken}`,
            'Content-Type': 'application/json',
        },
    }
);

const { data: teamInfo } = await useFetch(
    `${runtimeConfig.public.apiUrl}/team_info/`,
    {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${idToken}`,
            'Content-Type': 'application/json',
        },
    }
);

const { data: recruitments } = await useFetch(
    `${runtimeConfig.public.apiUrl}/other_team_recruitments/`,
    {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${idToken}`,
            'Content-Type': 'application/json',
        },
    }
);

recruitments.value = recruitments.value.map((item) => ({
    ...item,
    isApplied: false,
}));

const postApplication = async (recruitment_id) => {
    const postedApplication = await $fetch(
        `${runtimeConfig.public.apiUrl}/application/`,
        {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${idToken}`,
                'Content-Type': 'application/json',
            },
            body: {
                recruitment_id: recruitment_id,
            },
        }
    );

    if (postedApplication === null) {
        if (smAndUp.value) {
            mdErrorDialog.value = true;
        } else {
            xsErrorDialog.value = true;
        }

        recruitments.value = recruitments.value.filter(
            (recruitment) => recruitment.id !== recruitment_id
        );
    }
};

const search = shallowRef('');

const img_url =
    'https://cdn.pixabay.com/photo/2015/07/02/00/08/football-828218_1280.jpg';
</script>

<template>
    <div v-if="teamInfo === null">
        <v-empty-state
            class="d-flex align-center justify-center"
            style="min-height: 300px"
            icon="mdi-tshirt-crew"
            title="チーム情報が登録されていません"
        >
            <template #text>
                「<v-icon left>mdi-tshirt-crew</v-icon>
                チーム情報」より登録してください
            </template>
        </v-empty-state>
    </div>
    <div v-else>
        <div
            v-if="recruitments.length === 0"
            class="d-flex align-center justify-center"
            style="min-height: 300px"
        >
            <v-empty-state
                icon="mdi-account-search"
                title="申し込み可能な試合はありません"
            >
            </v-empty-state>
        </div>
        <div v-else>
            <template v-if="smAndUp">
                <v-data-iterator
                    :items="recruitments"
                    :items-per-page="3"
                    :search="search"
                >
                    <template v-slot:header>
                        <v-toolbar class="px-2">
                            <v-text-field
                                v-model="search"
                                density="comfortable"
                                placeholder="Search"
                                prepend-inner-icon="mdi-magnify"
                                style="max-width: 300px"
                                variant="solo"
                                clearable
                                hide-details
                            ></v-text-field>
                            <v-spacer></v-spacer>

                            <v-btn
                                prepend-icon="mdi-list-box-outline"
                                elevation="5"
                                @click="teamsDialog = true"
                                >登録チーム一覧
                            </v-btn>

                            <v-dialog v-model="teamsDialog" max-width="450">
                                <v-card>
                                    <v-card-title>登録チーム</v-card-title>

                                    <v-divider></v-divider>
                                    <v-virtual-scroll
                                        :items="registeredTeams"
                                        height="300"
                                        item-height="50"
                                    >
                                        <template v-slot:default="{ item }">
                                            <v-list-item>
                                                <v-list-item-title>{{
                                                    item.name
                                                }}</v-list-item-title>
                                                <v-list-item-subtitle>
                                                    {{ item.prefecture }} |
                                                    {{ item.category }} |
                                                    {{ item.league }}
                                                </v-list-item-subtitle>
                                                <template v-slot:append>
                                                    <a
                                                        v-if="
                                                            item.instagram_user_name
                                                        "
                                                        :href="`https://www.instagram.com/${item.instagram_user_name}/`"
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                    >
                                                        <img
                                                            src="../public/icons8-インスタグラム.svg"
                                                            width="40"
                                                            height="40"
                                                            style="
                                                                vertical-align: middle;
                                                            "
                                                    /></a>
                                                    <a
                                                        v-if="item.X_user_name"
                                                        :href="`https://x.com/${item.X_user_name}/`"
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                    >
                                                        <img
                                                            src="../public/icons8-ツイッターx.svg"
                                                            width="40"
                                                            height="40"
                                                            style="
                                                                vertical-align: middle;
                                                            "
                                                    /></a>
                                                </template>
                                            </v-list-item>
                                        </template>
                                    </v-virtual-scroll>
                                    <template v-slot:actions>
                                        <v-btn
                                            class="ms-auto"
                                            color="primary"
                                            variant="tonal"
                                            text="閉じる"
                                            @click="teamsDialog = false"
                                        ></v-btn>
                                    </template>
                                </v-card>
                            </v-dialog>
                        </v-toolbar>
                    </template>

                    <template v-slot:default="{ items }">
                        <v-container class="pa-2" fluid>
                            <v-row dense>
                                <v-col
                                    v-for="item in items"
                                    :key="item.title"
                                    cols="12"
                                    md="4"
                                >
                                    <v-card class="pb-3" border flat>
                                        <v-img :src="img_url">
                                            <div class="d-flex justify-end">
                                                <a
                                                    v-if="
                                                        item.raw
                                                            .instagram_user_name
                                                    "
                                                    :href="`https://www.instagram.com/${item.raw.instagram_user_name}/`"
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                >
                                                    <img
                                                        src="../public/icons8-インスタグラム.svg"
                                                        width="50"
                                                        height="50"
                                                        style="
                                                            vertical-align: middle;
                                                        "
                                                /></a>
                                                <a
                                                    v-if="item.raw.X_user_name"
                                                    :href="`https://x.com/${item.raw.X_user_name}/`"
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                >
                                                    <img
                                                        src="../public/icons8-ツイッターx.svg"
                                                        width="50"
                                                        height="50"
                                                        style="
                                                            vertical-align: middle;
                                                        "
                                                /></a>
                                            </div>
                                        </v-img>

                                        <v-card-item>
                                            <v-card-title>
                                                vs {{ item.raw.name }}
                                            </v-card-title>

                                            <v-card-subtitle>
                                                {{ item.raw.prefecture }} |
                                                {{ item.raw.category }} |
                                                {{ item.raw.league }}
                                            </v-card-subtitle>

                                            <v-card-subtitle>
                                                <v-icon
                                                    >mdi-calendar-month</v-icon
                                                >
                                                {{ item.raw.year }}年{{
                                                    item.raw.month
                                                }}月{{ item.raw.day }}日
                                            </v-card-subtitle>
                                            <v-card-subtitle>
                                                <v-icon>
                                                    mdi-clock-time-eight-outline
                                                </v-icon>
                                                {{ item.raw.start_time }}
                                                ~
                                                {{ item.raw.end_time }}
                                            </v-card-subtitle>

                                            <v-card-subtitle
                                                ><v-icon>
                                                    mdi-map-marker-outline</v-icon
                                                >{{
                                                    item.raw.location
                                                }}</v-card-subtitle
                                            >
                                        </v-card-item>

                                        <div
                                            class="d-flex justify-space-between px-4"
                                        >
                                            <div
                                                class="d-flex align-center text-caption text-medium-emphasis me-1"
                                            ></div>

                                            <v-btn
                                                class="text-none"
                                                size="small"
                                                :disabled="item.isApplied"
                                                :prepend-icon="
                                                    item.isApplied
                                                        ? 'mdi-check'
                                                        : ''
                                                "
                                                :color="
                                                    item.isApplied
                                                        ? 'success'
                                                        : ''
                                                "
                                                :text="
                                                    item.isApplied
                                                        ? '申し込み済'
                                                        : '申し込む'
                                                "
                                                border
                                                flat
                                                @click="
                                                    postApplication(
                                                        item.raw.id
                                                    );
                                                    item.isApplied = true;
                                                "
                                            >
                                            </v-btn>
                                        </div>
                                    </v-card>
                                </v-col>
                            </v-row>
                        </v-container>
                    </template>

                    <template
                        v-slot:footer="{ page, pageCount, prevPage, nextPage }"
                    >
                        <div class="d-flex align-center justify-center pa-4">
                            <v-btn
                                :disabled="page === 1"
                                density="comfortable"
                                icon="mdi-arrow-left"
                                variant="tonal"
                                rounded
                                @click="prevPage"
                            ></v-btn>

                            <div class="mx-2 text-caption">
                                Page {{ page }} of {{ pageCount }}
                            </div>

                            <v-btn
                                :disabled="page >= pageCount"
                                density="comfortable"
                                icon="mdi-arrow-right"
                                variant="tonal"
                                rounded
                                @click="nextPage"
                            ></v-btn>
                        </div>
                    </template>
                </v-data-iterator>
            </template>

            <template v-else>
                <v-data-iterator
                    :items="recruitments"
                    :items-per-page="3"
                    :search="search"
                >
                    <template v-slot:header>
                        <v-toolbar class="px-2">
                            <v-btn icon="mdi-magnify" elevation="5"></v-btn>

                            <v-spacer></v-spacer>

                            <v-btn
                                prepend-icon="mdi-list-box-outline"
                                elevation="5"
                                @click="teamsDialog = true"
                                >登録チーム一覧
                            </v-btn>

                            <v-dialog v-model="teamsDialog" max-width="450">
                                <v-card>
                                    <v-card-title>登録チーム</v-card-title>

                                    <v-divider></v-divider>
                                    <v-virtual-scroll
                                        :items="registeredTeams"
                                        height="300"
                                        item-height="50"
                                    >
                                        <template v-slot:default="{ item }">
                                            <v-list-item>
                                                <v-list-item-title>{{
                                                    item.name
                                                }}</v-list-item-title>
                                                <v-list-item-subtitle>
                                                    {{ item.prefecture }} |
                                                    {{ item.category }} |
                                                    {{ item.league }}
                                                </v-list-item-subtitle>
                                                <template v-slot:append>
                                                    <a
                                                        v-if="
                                                            item.instagram_user_name
                                                        "
                                                        :href="`https://www.instagram.com/${item.instagram_user_name}/`"
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                    >
                                                        <img
                                                            src="../public/icons8-インスタグラム.svg"
                                                            width="40"
                                                            height="40"
                                                            style="
                                                                vertical-align: middle;
                                                            "
                                                    /></a>
                                                    <a
                                                        v-if="item.X_user_name"
                                                        :href="`https://x.com/${item.X_user_name}/`"
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                    >
                                                        <img
                                                            src="../public/icons8-ツイッターx.svg"
                                                            width="40"
                                                            height="40"
                                                            style="
                                                                vertical-align: middle;
                                                            "
                                                    /></a>
                                                </template>
                                            </v-list-item>
                                        </template>
                                    </v-virtual-scroll>
                                    <template v-slot:actions>
                                        <v-btn
                                            class="ms-auto"
                                            color="primary"
                                            variant="tonal"
                                            text="閉じる"
                                            @click="teamsDialog = false"
                                        ></v-btn>
                                    </template>
                                </v-card>
                            </v-dialog>
                        </v-toolbar>
                    </template>

                    <template v-slot:default="{ items }">
                        <v-container class="pa-2" fluid>
                            <v-row dense>
                                <v-col
                                    v-for="item in items"
                                    :key="item.title"
                                    cols="12"
                                    xs="12"
                                >
                                    <v-card class="pb-3" border flat>
                                        <v-img :src="img_url">
                                            <div class="d-flex justify-end">
                                                <a
                                                    v-if="
                                                        item.raw
                                                            .instagram_user_name
                                                    "
                                                    :href="`https://www.instagram.com/${item.raw.instagram_user_name}/`"
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                >
                                                    <img
                                                        src="../public/icons8-インスタグラム.svg"
                                                        width="50"
                                                        height="50"
                                                        style="
                                                            vertical-align: middle;
                                                        "
                                                /></a>
                                                <a
                                                    v-if="item.raw.X_user_name"
                                                    :href="`https://x.com/${item.raw.X_user_name}/`"
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                >
                                                    <img
                                                        src="../public/icons8-ツイッターx.svg"
                                                        width="50"
                                                        height="50"
                                                        style="
                                                            vertical-align: middle;
                                                        "
                                                /></a>
                                            </div>
                                        </v-img>

                                        <v-card-item>
                                            <v-card-title>
                                                vs {{ item.raw.name }}
                                            </v-card-title>

                                            <v-card-subtitle>
                                                {{ item.raw.prefecture }} |
                                                {{ item.raw.category }} |
                                                {{ item.raw.league }}
                                            </v-card-subtitle>

                                            <v-card-subtitle>
                                                <v-icon
                                                    >mdi-calendar-month</v-icon
                                                >
                                                {{ item.raw.year }}年{{
                                                    item.raw.month
                                                }}月{{ item.raw.day }}日
                                            </v-card-subtitle>
                                            <v-card-subtitle>
                                                <v-icon>
                                                    mdi-clock-time-eight-outline
                                                </v-icon>
                                                {{ item.raw.start_time }}
                                                ~
                                                {{ item.raw.end_time }}
                                            </v-card-subtitle>

                                            <v-card-subtitle
                                                ><v-icon>
                                                    mdi-map-marker-outline</v-icon
                                                >{{
                                                    item.raw.location
                                                }}</v-card-subtitle
                                            >
                                        </v-card-item>

                                        <div
                                            class="d-flex justify-space-between px-4"
                                        >
                                            <div
                                                class="d-flex align-center text-caption text-medium-emphasis me-1"
                                            ></div>

                                            <v-btn
                                                class="text-none"
                                                size="small"
                                                :disabled="item.isApplied"
                                                :prepend-icon="
                                                    item.isApplied
                                                        ? 'mdi-check'
                                                        : ''
                                                "
                                                :color="
                                                    item.isApplied
                                                        ? 'success'
                                                        : ''
                                                "
                                                :text="
                                                    item.isApplied
                                                        ? '申し込み済'
                                                        : '申し込む'
                                                "
                                                border
                                                flat
                                                @click="
                                                    postApplication(
                                                        item.raw.id
                                                    );
                                                    item.isApplied = true;
                                                "
                                            >
                                            </v-btn>
                                        </div>
                                    </v-card>
                                </v-col>
                            </v-row>
                        </v-container>
                    </template>
                </v-data-iterator>
            </template>
        </div>

        <v-dialog v-model="mdErrorDialog" max-width="520">
            <v-card>
                <v-card-item>
                    <v-card-title
                        ><v-icon>mdi-alert-circle-outline</v-icon
                        >この募集は直前で削除 or
                        申し込みされました</v-card-title
                    >
                </v-card-item>
                <v-card-actions>
                    <v-btn color="primary" @click="mdErrorDialog = false"
                        >閉じる</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="xsErrorDialog" max-width="350">
            <v-card>
                <v-card-item>
                    <v-card-title
                        ><v-icon>mdi-alert-circle-outline</v-icon
                        >申し込みできませんでした</v-card-title
                    >
                    <v-card-subtitle>
                        この募集は直前で削除 or 申し込みされました
                    </v-card-subtitle>
                </v-card-item>
                <v-card-actions>
                    <v-btn color="primary" @click="xsErrorDialog = false"
                        >閉じる</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

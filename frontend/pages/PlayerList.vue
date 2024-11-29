<script setup>
import { nextTick, ref, watch } from 'vue';
import { useDisplay } from 'vuetify';

const user = await getCurrentUser();
const idToken = await user.getIdToken();

const runtimeConfig = useRuntimeConfig();

const { smAndUp } = useDisplay();

const { data: players } = await useFetch(
    `${runtimeConfig.public.apiUrl}/players/`,
    {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${idToken}`,
            'Content-Type': 'application/json',
        },
    }
);

const dialog = ref(false);
const deleteDialog = ref(false);
const headers = ref([
    { title: '背番号', align: 'start', key: 'number' },
    { title: 'ポジション', key: 'position', sortable: false },
    { title: '名前', key: 'namae', sortable: false },
    // { title: 'Name', key: 'name', sortable: false },
    { title: '身長(cm)', key: 'height', sortable: false },
    { title: '体重(kg)', key: 'weight', sortable: false },
    { title: '前所属', key: 'previous_team', sortable: false },
    { title: '', key: 'actions', sortable: false },
]);

const positions = ['GK', 'DF', 'MF', 'FW'];

const min_height = ref(0);
const max_height = ref(250);
const min_weight = ref(0);
const max_weight = ref(100);

const playerId = ref(-1);
const editedPlayerIndex = ref(-1);
const editedPlayer = ref({
    position: '',
    number: null,
    namae: '',
    // name: '',
    height: null,
    weight: null,
    previous_team: '',
});
const defaultItem = ref({
    position: '',
    number: null,
    namae: '',
    // name: '',
    height: null,
    weight: null,
    previous_team: '',
});

async function registerPlayer() {
    const registeredPlayer = await $fetch(
        `${runtimeConfig.public.apiUrl}/players/`,
        {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${idToken}`,
                'Content-Type': 'application/json',
            },
            body: editedPlayer.value,
        }
    );

    players.value.push(registeredPlayer);
}

async function postEdit(id) {
    const editedPlayerInfo = await $fetch(
        `${runtimeConfig.public.apiUrl}/players/${id}/`,
        {
            method: 'PUT',
            body: editedPlayer.value,
        }
    );

    Object.assign(players.value[editedPlayerIndex.value], editedPlayerInfo);
}

async function postDelete(id) {
    await $fetch(`${runtimeConfig.public.apiUrl}/players/${id}/`, {
        method: 'DELETE',
    });

    players.value = players.value.filter((player) => player.id !== id);
}

function editPlayer(item) {
    playerId.value = item.id;
    editedPlayerIndex.value = players.value.indexOf(item);
    editedPlayer.value = Object.assign({}, item);
    dialog.value = true;
}

function close() {
    dialog.value = false;
    nextTick(() => {
        editedPlayer.value = Object.assign({}, defaultItem.value);
        playerId.value = -1;
        editedPlayerIndex.value = -1;
    });
}

async function register() {
    if (editedPlayerIndex.value > -1) {
        await postEdit(playerId.value);
    } else {
        await registerPlayer();
    }
    close();
}

function deletePlayer(item) {
    playerId.value = item.id;
    deleteDialog.value = true;
}

function closeDeleteDialog() {
    deleteDialog.value = false;
    nextTick(() => {
        playerId.value = -1;
    });
}

function deletePlayerConfirm() {
    postDelete(playerId.value);
    closeDeleteDialog();
}

watch(dialog, (val) => {
    val || close();
});

watch(deleteDialog, (val) => {
    val || closeDeleteDialog();
});

const isValid = computed(() => {
    return (
        editedPlayer.value.position &&
        editedPlayer.value.number &&
        editedPlayer.value.namae &&
        // editedPlayer.value.name &&
        editedPlayer.value.height &&
        editedPlayer.value.weight &&
        editedPlayer.value.previous_team
    );
});
</script>

<template>
    <div>
        <!-- PC・タブレット用 -->

        <template v-if="smAndUp">
            <v-data-table
                :headers="headers"
                :items="players"
                :sort-by="[{ key: 'number', order: 'asc' }]"
            >
                <template v-slot:top>
                    <v-toolbar class="px-2">
                        <v-toolbar-title>選手一覧</v-toolbar-title>
                        <v-divider class="mx-4" inset vertical></v-divider>

                        <v-spacer></v-spacer>

                        <!-- 選手を登録ボタン -->
                        <v-btn
                            prepend-icon="mdi-account-plus"
                            elevation="5"
                            @click="dialog = true"
                        >
                            選手を登録
                        </v-btn>
                    </v-toolbar>
                </template>
                <template v-slot:[`item.actions`]="{ item }">
                    <v-icon
                        color="#4CAF50"
                        class="me-2"
                        @click="editPlayer(item)"
                        v-tooltip:top="'編集'"
                    >
                        mdi-pencil
                    </v-icon>
                    <v-icon
                        color="#F44336"
                        class="me-2"
                        @click="deletePlayer(item)"
                        v-tooltip:top="'削除'"
                    >
                        mdi-delete
                    </v-icon>
                </template>
                <template v-slot:no-data> 選手が登録されていません </template>
            </v-data-table>

            <!-- ダイアログ類 -->

            <!-- 選手を登録ダイアログ -->
            <v-dialog v-model="dialog" max-width="500px">
                <v-card prepend-icon="mdi-account" title="選手情報">
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" md="4" sm="6">
                                    <v-select
                                        v-model="editedPlayer.position"
                                        label="ポジション"
                                        :items="positions"
                                    ></v-select>
                                </v-col>
                                <v-col cols="12" md="4" sm="6">
                                    <v-number-input
                                        v-model="editedPlayer.number"
                                        label="背番号"
                                        :min="1"
                                        control-variant="stacked"
                                    >
                                    </v-number-input>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-responsive
                                        class="mx-auto"
                                        max-width="344"
                                    >
                                        <v-text-field
                                            v-model="editedPlayer.namae"
                                            label="名前"
                                            clearable
                                        ></v-text-field>
                                    </v-responsive>
                                </v-col>
                                <v-responsive class="mx-auto" max-width="344">
                                    <v-col>
                                        <v-text-field
                                            v-model="editedPlayer.name"
                                            label="Name"
                                            clearable
                                        ></v-text-field>
                                    </v-col>
                                </v-responsive>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-slider
                                        v-model="editedPlayer.height"
                                        :step="1"
                                        :max="max_height"
                                        :min="min_height"
                                        class="align-center"
                                        hide-details
                                        label="身長"
                                    >
                                        <template v-slot:append>
                                            <v-text-field
                                                v-model="editedPlayer.height"
                                                density="compact"
                                                style="width: 75px"
                                                type="number"
                                                hide-details
                                                single-line
                                            ></v-text-field>
                                        </template>
                                    </v-slider>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-slider
                                        v-model="editedPlayer.weight"
                                        :step="1"
                                        :max="max_weight"
                                        :min="min_weight"
                                        class="align-center"
                                        hide-details
                                        label="体重"
                                    >
                                        <template v-slot:append>
                                            <v-text-field
                                                v-model="editedPlayer.weight"
                                                density="compact"
                                                style="width: 75px"
                                                type="number"
                                                hide-details
                                                single-line
                                            ></v-text-field>
                                        </template>
                                    </v-slider>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col>
                                    <v-text-field
                                        v-model="editedPlayer.previous_team"
                                        label="前所属"
                                        clearable
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn text="キャンセル" variant="plain" @click="close">
                        </v-btn>

                        <v-btn
                            color="primary"
                            text="保存"
                            variant="tonal"
                            @click="register"
                            :disabled="!isValid"
                        >
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <!-- 削除確認ダイアログ -->
            <v-dialog v-model="deleteDialog" max-width="500px">
                <v-card
                    prepend-icon="mdi-alert-circle-outline"
                    title="この選手情報を削除してもよろしいですか？"
                >
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            text="キャンセル"
                            variant="plain"
                            @click="closeDeleteDialog()"
                        ></v-btn>
                        <v-btn
                            color="primary"
                            text="OK"
                            variant="tonal"
                            @click="deletePlayerConfirm()"
                        ></v-btn>
                        <v-spacer></v-spacer>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </template>

        <!-- スマホ用 -->

        <template v-else>
            <v-data-iterator :items="players" items-per-page="-1">
                <template v-slot:header>
                    <v-app-bar class="px-2" :elevation="1">
                        <v-col cols="2"></v-col>

                        <v-col class="d-flex justify-space-around">
                            <v-app-bar-title class="text-center"
                                >選手一覧</v-app-bar-title
                            >
                        </v-col>

                        <v-col cols="2" class="d-flex justify-end">
                            <!-- 選手を登録ボタン -->
                            <v-btn
                                icon="mdi-account-plus"
                                elevation="5"
                                @click="dialog = true"
                            >
                            </v-btn>
                        </v-col>
                    </v-app-bar>
                </template>

                <!-- 登録済みの選手一覧 -->

                <template v-slot:default="{ items }">
                    <v-container class="pa-2" fluid>
                        <v-row dense>
                            <v-col
                                v-for="item in items"
                                :key="item.title"
                                cols="12"
                                xs="12"
                            >
                                <v-card>
                                    <v-row align="center" no-gutters>
                                        <v-card-item>
                                            <v-card-title>
                                                {{ item.raw.position }}
                                                {{ item.raw.number }}
                                                {{ item.raw.namae }}
                                            </v-card-title>

                                            <!-- <v-card-title>
                                                {{ item.raw.namae }}
                                                {{ item.raw.name }}
                                            </v-card-title> -->

                                            <v-card-subtitle>
                                                身長/体重：
                                                {{ item.raw.height }}cm/{{
                                                    item.raw.weight
                                                }}kg
                                            </v-card-subtitle>

                                            <v-card-subtitle>
                                                前所属：
                                                {{ item.raw.previous_team }}
                                            </v-card-subtitle>
                                        </v-card-item>

                                        <v-spacer></v-spacer>

                                        <!-- 削除ボタン -->
                                        <v-card-actions
                                            class="d-flex justify-end"
                                        >
                                            <v-icon
                                                color="#4CAF50"
                                                class="me-2"
                                                @click="editPlayer(item.raw)"
                                                v-tooltip:top="'編集'"
                                            >
                                                mdi-pencil
                                            </v-icon>
                                            <v-icon
                                                color="#F44336"
                                                class="me-2"
                                                @click="deletePlayer(item.raw)"
                                                >mdi-delete</v-icon
                                            >
                                        </v-card-actions>
                                    </v-row>
                                </v-card>
                            </v-col>
                        </v-row>
                    </v-container>
                </template>
            </v-data-iterator>

            <!-- ダイアログ類 -->

            <!-- 選手を登録ダイアログ -->
            <v-dialog v-model="dialog" max-width="500px">
                <v-card prepend-icon="mdi-account" title="選手情報">
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="6">
                                    <v-select
                                        v-model="editedPlayer.position"
                                        label="ポジション"
                                        :items="positions"
                                        density="comfortable"
                                    ></v-select>
                                </v-col>
                                <v-col cols="6">
                                    <v-number-input
                                        v-model="editedPlayer.number"
                                        label="背番号"
                                        :min="1"
                                        control-variant="stacked"
                                        density="comfortable"
                                    >
                                    </v-number-input>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field
                                        v-model="editedPlayer.namae"
                                        label="名前を入力"
                                        clearable
                                        density="comfortable"
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                            <!-- <v-row>
                                <v-col cols="12">
                                    <v-text-field
                                        v-model="editedPlayer.name"
                                        label="ローマ字で入力"
                                        clearable
                                        density="comfortable"
                                    ></v-text-field>
                                </v-col>
                            </v-row> -->
                            <v-row>
                                <v-col cols="12">
                                    <v-slider
                                        v-model="editedPlayer.height"
                                        :step="1"
                                        :max="max_height"
                                        :min="min_height"
                                        class="align-center"
                                        hide-details
                                        label="身長"
                                    >
                                        <template v-slot:append>
                                            <v-text-field
                                                v-model="editedPlayer.height"
                                                density="comfortable"
                                                style="width: 75px"
                                                type="number"
                                                hide-details
                                                single-line
                                            ></v-text-field>
                                        </template>
                                    </v-slider>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col cols="12">
                                    <v-slider
                                        v-model="editedPlayer.weight"
                                        :step="1"
                                        :max="max_weight"
                                        :min="min_weight"
                                        class="align-center"
                                        hide-details
                                        label="体重"
                                    >
                                        <template v-slot:append>
                                            <v-text-field
                                                v-model="editedPlayer.weight"
                                                density="comfortable"
                                                style="width: 75px"
                                                type="number"
                                                hide-details
                                                single-line
                                            ></v-text-field>
                                        </template>
                                    </v-slider>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field
                                        v-model="editedPlayer.previous_team"
                                        label="前所属チームを入力"
                                        clearable
                                        density="comfortable"
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn
                            text="キャンセル"
                            variant="plain"
                            @click="close()"
                        >
                        </v-btn>

                        <v-btn
                            color="primary"
                            text="保存"
                            variant="tonal"
                            @click="register()"
                            :disabled="!isValid"
                        >
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <!-- 削除確認ダイアログ -->
            <v-dialog v-model="deleteDialog" max-width="370px">
                <v-card
                    prepend-icon="mdi-alert-circle-outline"
                    title="この選手情報を削除しますか？"
                >
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            text="いいえ"
                            variant="plain"
                            @click="closeDeleteDialog()"
                        ></v-btn>
                        <v-btn
                            color="primary"
                            text="はい"
                            variant="tonal"
                            @click="deletePlayerConfirm()"
                        ></v-btn>
                        <v-spacer></v-spacer>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </template>
    </div>
</template>

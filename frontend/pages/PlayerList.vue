<script setup>
import { nextTick, ref, watch } from 'vue';

const user = await getCurrentUser();
const idToken = await user.getIdToken();

const runtimeConfig = useRuntimeConfig();

const { data: players } = await useFetch(
    `${runtimeConfig.public.apiUrl}/players`,
    {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${idToken}`,
            'Content-Type': 'application/json',
        },
    }
);

const dialog = ref(false);
const dialogDelete = ref(false);
const headers = ref([
    { title: '背番号', align: 'start', key: 'number' },
    { title: 'ポジション', key: 'position', sortable: false },
    { title: '名前', key: 'namae', sortable: false },
    { title: 'Name', key: 'name', sortable: false },
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

const itemId = ref(-1);
const editedIndex = ref(-1);
const editedItem = ref({
    position: '',
    number: null,
    namae: '',
    name: '',
    height: null,
    weight: null,
    previous_team: '',
});
const defaultItem = ref({
    position: '',
    number: null,
    namae: '',
    name: '',
    height: null,
    weight: null,
    previous_team: '',
});

async function registerPlayer() {
    const registeredPlayer = await $fetch(
        `${runtimeConfig.public.apiUrl}/players`,
        {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${idToken}`,
                'Content-Type': 'application/json',
            },
            body: editedItem.value,
        }
    );

    players.value.push(registeredPlayer);
}

async function editPlayer(id) {
    const editedPlayer = await $fetch(
        `${runtimeConfig.public.apiUrl}/players/${id}`,
        {
            method: 'PUT',
            body: editedItem.value,
        }
    );

    Object.assign(players.value[editedIndex.value], editedPlayer);
}

async function deletePlayer(id) {
    await $fetch(`${runtimeConfig.public.apiUrl}/players/${id}`, {
        method: 'DELETE',
    });

    players.value = players.value.filter((player) => player.id !== id);
}

function editItem(item) {
    itemId.value = item.id;
    editedIndex.value = players.value.indexOf(item);
    editedItem.value = Object.assign({}, item);
    dialog.value = true;
}

function close() {
    dialog.value = false;
    nextTick(() => {
        editedItem.value = Object.assign({}, defaultItem.value);
        itemId.value = -1;
        editedIndex.value = -1;
    });
}

async function save() {
    if (editedIndex.value > -1) {
        await editPlayer(itemId.value);
    } else {
        await registerPlayer();
    }
    close();
}

function deleteItem(item) {
    itemId.value = item.id;
    dialogDelete.value = true;
}

function closeDelete() {
    dialogDelete.value = false;
    nextTick(() => {
        itemId.value = -1;
    });
}

function deleteItemConfirm() {
    deletePlayer(itemId.value);
    closeDelete();
}

watch(dialog, (val) => {
    val || close();
});

watch(dialogDelete, (val) => {
    val || closeDelete();
});

const isValid = computed(() => {
    return (
        editedItem.value.position &&
        editedItem.value.number &&
        editedItem.value.namae &&
        editedItem.value.name &&
        editedItem.value.height &&
        editedItem.value.weight &&
        editedItem.value.previous_team
    );
});
</script>

<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="players"
            :sort-by="[{ key: 'number', order: 'asc' }]"
        >
            <template v-slot:top>
                <v-toolbar flat>
                    <v-toolbar-title>選手一覧</v-toolbar-title>
                    <v-divider class="mx-4" inset vertical></v-divider>
                    <v-spacer></v-spacer>

                    <v-btn
                        prepend-icon="mdi-account-plus"
                        elevation="5"
                        @click="dialog = true"
                    >
                        選手を登録
                    </v-btn>

                    <v-dialog v-model="dialog" max-width="500px">
                        <v-card prepend-icon="mdi-account" title="選手情報">
                            <v-card-text>
                                <v-container>
                                    <v-row>
                                        <v-col cols="12" md="4" sm="6">
                                            <v-select
                                                v-model="editedItem.position"
                                                label="ポジション"
                                                :items="positions"
                                            ></v-select>
                                        </v-col>
                                        <v-col cols="12" md="4" sm="6">
                                            <v-number-input
                                                v-model="editedItem.number"
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
                                                    v-model="editedItem.namae"
                                                    label="名前"
                                                    clearable
                                                ></v-text-field>
                                            </v-responsive>
                                        </v-col>
                                        <v-responsive
                                            class="mx-auto"
                                            max-width="344"
                                        >
                                            <v-col>
                                                <v-text-field
                                                    v-model="editedItem.name"
                                                    label="Name"
                                                    clearable
                                                ></v-text-field>
                                            </v-col>
                                        </v-responsive>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <v-slider
                                                v-model="editedItem.height"
                                                :step="1"
                                                :max="max_height"
                                                :min="min_height"
                                                class="align-center"
                                                hide-details
                                                label="身長"
                                            >
                                                <template v-slot:append>
                                                    <v-text-field
                                                        v-model="
                                                            editedItem.height
                                                        "
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
                                                v-model="editedItem.weight"
                                                :step="1"
                                                :max="max_weight"
                                                :min="min_weight"
                                                class="align-center"
                                                hide-details
                                                label="体重"
                                            >
                                                <template v-slot:append>
                                                    <v-text-field
                                                        v-model="
                                                            editedItem.weight
                                                        "
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
                                                v-model="
                                                    editedItem.previous_team
                                                "
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

                                <v-btn
                                    text="キャンセル"
                                    variant="plain"
                                    @click="close"
                                >
                                </v-btn>

                                <v-btn
                                    color="primary"
                                    text="保存"
                                    variant="tonal"
                                    @click="save"
                                    :disabled="!isValid"
                                >
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                    <v-dialog v-model="dialogDelete" max-width="500px">
                        <v-card
                            prepend-icon="mdi-alert-circle-outline"
                            title="この選手情報を削除してもよろしいですか？"
                        >
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    text="キャンセル"
                                    variant="plain"
                                    @click="closeDelete"
                                ></v-btn>
                                <v-btn
                                    color="primary"
                                    text="OK"
                                    variant="tonal"
                                    @click="deleteItemConfirm"
                                ></v-btn>
                                <v-spacer></v-spacer>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </v-toolbar>
            </template>
            <template v-slot:[`item.actions`]="{ item }">
                <v-icon
                    color="#4CAF50"
                    class="me-2"
                    @click="editItem(item)"
                    v-tooltip:top="'編集'"
                >
                    mdi-pencil
                </v-icon>
                <v-icon
                    color="#F44336"
                    class="me-2"
                    @click="deleteItem(item)"
                    v-tooltip:top="'削除'"
                >
                    mdi-delete
                </v-icon>
            </template>
            <template v-slot:no-data> 選手が登録されていません </template>
        </v-data-table>
    </div>
</template>

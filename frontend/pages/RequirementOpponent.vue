<script setup>
import { nextTick, ref, watch } from 'vue';
import { useDisplay } from 'vuetify';

const user = await getCurrentUser();
const idToken = await user.getIdToken();

const runtimeConfig = useRuntimeConfig();

const { smAndUp } = useDisplay();

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
    `${runtimeConfig.public.apiUrl}/my_team_recruitments/`,
    {
        method: 'GET',
        headers: {
            Authorization: `Bearer ${idToken}`,
            'Content-Type': 'application/json',
        },
    }
);

const selectedRegion = ref('');
const selectedPrefecture = ref('');

const regions = {
    '北海道・東北': [
        '北海道',
        '青森県',
        '岩手県',
        '宮城県',
        '秋田県',
        '山形県',
        '福島県',
    ],
    関東: [
        '茨城県',
        '栃木県',
        '群馬県',
        '埼玉県',
        '千葉県',
        '東京都',
        '神奈川県',
    ],
    中部: [
        '新潟県',
        '富山県',
        '石川県',
        '福井県',
        '山梨県',
        '長野県',
        '岐阜県',
        '静岡県',
        '愛知県',
    ],
    近畿: [
        '三重県',
        '滋賀県',
        '京都府',
        '大阪府',
        '兵庫県',
        '奈良県',
        '和歌山県',
    ],
    中国: ['鳥取県', '島根県', '岡山県', '広島県', '山口県'],
    四国: ['徳島県', '香川県', '愛媛県', '高知県'],
    '九州・沖縄': [
        '福岡県',
        '佐賀県',
        '長崎県',
        '熊本県',
        '大分県',
        '宮崎県',
        '鹿児島県',
        '沖縄県',
    ],
};

const regionsList = Object.keys(regions);

const grounds = {
    福岡県: [
        {
            title: '福岡フットボールセンター',
            url: 'https://fukuoka-ffc.com/',
        },
        {
            title: 'その他のグラウンド',
            url: 'https://www3.11489.jp/fukuoka/user/Home#divSearch',
        },
    ],
    佐賀県: [
        {
            title: '小城市フットボールセンター',
            url: 'https://labola.jp/r/shop/3311/calendar_week/',
        },
        {
            title: 'FOOTBALL PARK SAGA YAMATO',
            url: 'https://sagayamato-footballpark.com/main/4.html',
        },
        {
            title: 'その他のグラウンド',
            url: 'https://yoyaku.city.saga.lg.jp/web/(S(pvaqi2rg12pvov45ruf4rs55))/Wg_KoukyouShisetsuYoyakuMoushikomi.aspx',
        },
    ],
    長崎県: [
        {
            title: '長崎県スポーツ協会人工芝グラウンド',
            url: 'https://nagasakikensportss.wixsite.com/shinkoukai',
        },
        {
            title: 'その他のグラウンド(県内全域)',
            url: 'https://nelcs.ne.jp/Facilityrsv/Smartphone/4200042/user/home/index.php5',
        },
        {
            title: 'その他のグラウンド(長崎市内のみ)',
            url: 'https://www.11489.jp/NagasakiCity/Web/Home/WgR_ModeSelect',
        },
    ],
    熊本県: [
        {
            title: 'COSMOSフィールド',
            url: 'https://cosmos-kfc.com/field/',
        },
        {
            title: 'くまトヨスポーツパーク多目的競技場',
            url: 'https://yoyaku.town.kumamoto-kashima.lg.jp/content/asp/ShisetuIchiran.asp',
        },
        {
            title: '益城町陸上競技場',
            url: 'https://www.town.mashiki.lg.jp/contents/sisetuyoyaku_pac/asp/ShisetuIchiran.asp',
        },
        {
            title: 'その他のグラウンド',
            url: 'https://www.yoyakuma.jp/reserve_j/rsv_rj/Portal_i/pindex.asp',
        },
    ],
    大分県: [
        {
            title: '大分県サッカー協会人工芝グラウンド',
            url: 'https://oita-s-c.resv.jp/reserve/calendar.php?x=1731748018',
        },
        {
            title: 'その他のグラウンド',
            url: 'https://www.pa-reserve.jp/eap-rjt/rsv_rj/Core_i/init.asp?KLCD=449999&SBT=1&Target=_Top&LCD=',
        },
    ],
    宮崎県: [
        {
            title: '新富町フットボールセンター',
            url: 'https://miyazaki-fa.net/football-center',
        },
        {
            title: '宮崎県総合運動公園',
            url: 'https://www.miyazaki-spokyo.jp/reserve/',
        },
        {
            title: 'アミノバイタルトレーニングセンター',
            url: 'https://dapo-3.dapo.jp/seahorse/webform.php?id=39400',
        },
        {
            title: '大塚原運動広場',
            url: 'http://toweb.city.kobayashi.lg.jp/yoyakukanri/',
        },
        {
            title: 'その他のグラウンド',
            url: 'https://www.11489.jp/Miyazaki/web/(S(saqkp2f322blz2555yz0ii55))/Wg_ModeSelect.aspx',
        },
    ],
    鹿児島県: [
        {
            title: '鹿児島県立サッカー・ラグビー場',
            url: 'https://www.spm-cloud.com/user/seika/soccer-rugby/',
        },
        {
            title: 'その他のグラウンド',
            url: 'https://k2.p-kashikan.jp/kagoshima-city/index.php',
        },
    ],
};

const postDialog = ref(false);
const reservationDialog = ref(false);
const dialogDelete = ref(false);

const headers = ref([
    { title: '状態', align: 'start', key: 'status' },
    { title: '年', key: 'year', sortable: false },
    { title: '月', key: 'month', sortable: false },
    { title: '日', key: 'day', sortable: false },
    { title: '開始', key: 'start_time', sortable: false },
    { title: '終了', key: 'end_time', sortable: false },
    { title: '場所', key: 'location', sortable: false },
    { title: '', key: 'actions', sortable: false },
]);

const itemId = ref(-1);
const editedItem = ref({
    year: null,
    month: null,
    day: null,
    start_time: '',
    end_time: '',
    location: '',
});
const defaultItem = ref({
    year: null,
    month: null,
    day: null,
    start_time: '',
    end_time: '',
    location: '',
});

async function postRecruitment() {
    const postedRecruitment = await $fetch(
        `${runtimeConfig.public.apiUrl}/recruitments/`,
        {
            method: 'POST',
            headers: {
                Authorization: `Bearer ${idToken}`,
                'Content-Type': 'application/json',
            },
            body: editedItem.value,
        }
    );
    recruitments.value.push(postedRecruitment);
}

async function deleteRecruitment(id) {
    await $fetch(`${runtimeConfig.public.apiUrl}/recruitments/${id}/`, {
        method: 'DELETE',
    });

    recruitments.value = recruitments.value.filter(
        (recruitment) => recruitment.id !== id
    );
}

function close() {
    postDialog.value = false;
    nextTick(() => {
        editedItem.value = Object.assign({}, defaultItem.value);
        itemId.value = -1;
    });
}

function post() {
    postRecruitment();
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
    deleteRecruitment(itemId.value);
    closeDelete();
}

const goToUrl = (url) => {
    window.open(url, '_blank');
};

const currentYear = new Date().getFullYear();
const yearOptions = [currentYear, currentYear + 1];

const monthOptions = Array.from({ length: 12 }, (_, i) => i + 1);

const dayOptions = Array.from({ length: 31 }, (_, i) => i + 1);

// 1時間間隔で時間を生成する関数
const generateTimeOptions = () => {
    const times = [];
    for (let hour = 0; hour < 24; hour++) {
        // 時間を "HH:00" 形式にフォーマット
        const formattedTime = `${String(hour).padStart(2, '0')}:00`;
        times.push(formattedTime);
    }
    return times;
};

const timeOptions = generateTimeOptions();

watch(postDialog, (val) => {
    val || close();
});
watch(dialogDelete, (val) => {
    val || closeDelete();
});

const isValid = computed(() => {
    return (
        editedItem.value.year &&
        editedItem.value.month &&
        editedItem.value.day &&
        editedItem.value.start_time &&
        editedItem.value.end_time &&
        editedItem.value.location
    );
});
</script>

<template>
    <!-- チーム情報が登録されていない場合 -->

    <div v-if="teamInfo === null">
        <v-empty-state
            class="d-flex align-center justify-center"
            style="min-height: 300px"
            icon="mdi-tshirt-crew"
            title="チーム情報が登録されていません"
        >
            <template #text>
                「<v-icon left>mdi-tshirt-crew</v-icon>
                チーム情報」より、まずはじめにチーム情報を登録してください
            </template>
        </v-empty-state>
    </div>

    <!-- チーム情報が登録されている場合 -->

    <div v-else>
        <!-- PC・タブレット用 -->

        <template v-if="smAndUp">
            <v-data-table
                :headers="headers"
                :items="recruitments"
                :sort-by="[
                    { key: 'year', order: 'desc' },
                    { key: 'month', order: 'desc' },
                    { key: 'day', order: 'desc' },
                ]"
            >
                <template v-slot:top>
                    <v-toolbar class="px-2">
                        <v-toolbar-title>投稿済みの募集一覧</v-toolbar-title>
                        <v-divider class="mx-4" inset vertical></v-divider>
                        <v-spacer></v-spacer>

                        <!-- 募集を投稿ボタン -->
                        <v-btn
                            prepend-icon="mdi-text-box-plus-outline"
                            elevation="5"
                            @click="postDialog = true"
                        >
                            募集を投稿
                        </v-btn>
                    </v-toolbar>
                </template>

                <!-- 削除ボタン -->
                <template v-slot:[`item.actions`]="{ item }">
                    <v-icon
                        v-if="item.status === '募集中'"
                        color="#F44336"
                        class="me-2"
                        @click="deleteItem(item)"
                        v-tooltip:top="'削除'"
                    >
                        mdi-delete
                    </v-icon>
                </template>
                <template v-slot:no-data> 募集が投稿されていません </template>
            </v-data-table>

            <!-- ダイアログ類 -->

            <!-- 募集投稿ダイアログ -->
            <v-dialog v-model="postDialog" max-width="500px">
                <v-card prepend-icon="mdi-form-select" title="募集内容">
                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col class="d-flex align-center">
                                    <v-icon>mdi-soccer-field</v-icon>
                                </v-col>
                                <v-col cols="10" md="10" sm="7"
                                    ><v-btn
                                        evaluation="10"
                                        @click="reservationDialog = true"
                                    >
                                        グラウンドを予約
                                    </v-btn>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col class="d-flex align-center">
                                    <v-icon>mdi-map-marker-outline</v-icon>
                                </v-col>
                                <v-col cols="10" md="10" sm="7">
                                    <v-text-field
                                        v-model="editedItem.location"
                                        hide-details="auto"
                                        label="開催場所を入力"
                                        clearable
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col class="d-flex align-center">
                                    <v-icon> mdi-calendar-month </v-icon>
                                </v-col>
                                <v-col md="4" sm="7">
                                    <v-select
                                        v-model="editedItem.year"
                                        label="年"
                                        :items="yearOptions"
                                    />
                                </v-col>
                                <v-col md="3" sm="7">
                                    <v-select
                                        v-model="editedItem.month"
                                        label="月"
                                        :items="monthOptions"
                                    />
                                </v-col>
                                <v-col md="3" sm="7">
                                    <v-select
                                        v-model="editedItem.day"
                                        label="日"
                                        :items="dayOptions"
                                    />
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col class="d-flex align-center">
                                    <v-icon>
                                        mdi-clock-time-eight-outline
                                    </v-icon>
                                </v-col>
                                <v-col cols="5" md="5" sm="7">
                                    <v-select
                                        v-model="editedItem.start_time"
                                        label="開始時間"
                                        :items="timeOptions"
                                    />
                                </v-col>
                                <v-col cols="5" md="5" sm="7">
                                    <v-select
                                        v-model="editedItem.end_time"
                                        label="終了時間"
                                        :items="timeOptions"
                                    />
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
                            text="投稿"
                            variant="tonal"
                            @click="post"
                            :disabled="!isValid"
                        >
                        </v-btn>
                    </v-card-actions>
                </v-card>

                <!-- グラウンドを予約ダイアログ -->
                <v-dialog v-model="reservationDialog" max-width="450">
                    <v-card>
                        <v-card-item>
                            <v-row>
                                <v-col cols="12" md="6" sm="6">
                                    <v-select
                                        :items="regionsList"
                                        label="地域を選択"
                                        v-model="selectedRegion"
                                    ></v-select>
                                </v-col>
                                <v-col cols="12" md="6" sm="6">
                                    <v-select
                                        label="都道府県を選択"
                                        :items="regions[selectedRegion]"
                                        v-model="selectedPrefecture"
                                    ></v-select>
                                </v-col>
                            </v-row>

                            <v-divider></v-divider>
                        </v-card-item>

                        <v-virtual-scroll
                            :items="grounds[selectedPrefecture]"
                            height="150"
                            item-height="50"
                        >
                            <template v-slot:default="{ item }">
                                <v-list-item>
                                    <v-list-item-title>{{
                                        item.title
                                    }}</v-list-item-title>
                                    <template v-slot:append>
                                        <v-btn @click="goToUrl(item.url)"
                                            >予約ページへ</v-btn
                                        >
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
                                @click="reservationDialog = false"
                            ></v-btn>
                        </template>
                    </v-card>
                </v-dialog>
            </v-dialog>

            <!-- 投稿消去確認ダイアログ -->
            <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card
                    prepend-icon="mdi-alert-circle-outline"
                    title="この募集投稿を削除してもよろしいですか？"
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
        </template>

        <!-- スマホ用 -->

        <template v-else>
            <v-data-iterator :items="recruitments" items-per-page="-1">
                <template v-slot:header>
                    <v-app-bar class="px-2" :elevation="1">
                        <v-app-bar-title class="text-center"
                            >対戦相手を募集</v-app-bar-title
                        >

                        <!-- 募集を投稿ボタン -->
                        <v-btn
                            icon="mdi-text-box-plus-outline"
                            elevation="5"
                            @click="postDialog = true"
                        ></v-btn>
                    </v-app-bar>
                </template>

                <!-- 投稿済みの募集一覧 -->

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
                                            <v-icon>mdi-calendar-month</v-icon>
                                            {{ item.raw.year }}年{{
                                                item.raw.month
                                            }}月{{ item.raw.day }}日

                                            <br />

                                            <v-icon
                                                >mdi-clock-time-eight-outline</v-icon
                                            >
                                            {{ item.raw.start_time }} ~
                                            {{ item.raw.end_time }}

                                            <br />

                                            <v-icon
                                                >mdi-map-marker-outline</v-icon
                                            >
                                            {{ item.raw.location }}
                                        </v-card-item>

                                        <v-spacer></v-spacer>

                                        <!-- 削除ボタン -->
                                        <v-card-actions
                                            class="d-flex justify-end"
                                        >
                                            <v-icon
                                                v-if="
                                                    item.raw.status === '募集中'
                                                "
                                                color="#F44336"
                                                class="me-2"
                                                size="large"
                                                @click="deleteItem(item.raw)"
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

            <!-- 募集投稿ダイアログ -->
            <v-dialog v-model="postDialog" max-width="550px">
                <v-card prepend-icon="mdi-form-select" title="募集内容">
                    <v-card-text>
                        <v-row>
                            <v-col cols="12"
                                ><v-btn
                                    evaluation="10"
                                    @click="reservationDialog = true"
                                >
                                    グラウンドを予約
                                </v-btn>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedItem.location"
                                    hide-details="auto"
                                    label="開催場所を入力"
                                    clearable
                                    density="comfortable"
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="4">
                                <v-select
                                    v-model="editedItem.year"
                                    label="年"
                                    :items="yearOptions"
                                    density="comfortable"
                                />
                            </v-col>
                            <v-col cols="4">
                                <v-select
                                    v-model="editedItem.month"
                                    label="月"
                                    :items="monthOptions"
                                    density="comfortable"
                                />
                            </v-col>
                            <v-col cols="4">
                                <v-select
                                    v-model="editedItem.day"
                                    label="日"
                                    :items="dayOptions"
                                    density="comfortable"
                                />
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="6">
                                <v-select
                                    v-model="editedItem.start_time"
                                    label="開始時間"
                                    :items="timeOptions"
                                    density="comfortable"
                                />
                            </v-col>
                            <v-col cols="6">
                                <v-select
                                    v-model="editedItem.end_time"
                                    label="終了時間"
                                    :items="timeOptions"
                                    density="comfortable"
                                />
                            </v-col>
                        </v-row>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn text="キャンセル" variant="plain" @click="close">
                        </v-btn>

                        <v-btn
                            color="primary"
                            text="投稿"
                            variant="tonal"
                            @click="post"
                            :disabled="!isValid"
                        >
                        </v-btn>
                    </v-card-actions>
                </v-card>

                <!-- グラウンドを予約ダイアログ -->
                <v-dialog v-model="reservationDialog" max-width="370">
                    <v-card>
                        <v-card-item>
                            <v-row>
                                <v-col cols="6">
                                    <v-select
                                        :items="regionsList"
                                        label="地域を選択"
                                        v-model="selectedRegion"
                                        density="comfortable"
                                    ></v-select>
                                </v-col>
                                <v-col cols="6">
                                    <v-select
                                        :items="regions[selectedRegion]"
                                        label="都道府県を選択"
                                        v-model="selectedPrefecture"
                                        density="comfortable"
                                    ></v-select>
                                </v-col>
                            </v-row>

                            <v-divider></v-divider>
                        </v-card-item>

                        <v-virtual-scroll
                            :items="grounds[selectedPrefecture]"
                            height="150"
                            item-height="50"
                        >
                            <template v-slot:default="{ item }">
                                <v-list-item>
                                    <v-list-item-title>{{
                                        item.title
                                    }}</v-list-item-title>
                                    <template v-slot:append>
                                        <v-icon
                                            icon="mdi-open-in-new"
                                            @click="goToUrl(item.url)"
                                        ></v-icon>
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
                                @click="reservationDialog = false"
                            ></v-btn>
                        </template>
                    </v-card>
                </v-dialog>
            </v-dialog>

            <!-- 投稿消去確認ログ -->
            <v-dialog v-model="dialogDelete" max-width="330px">
                <v-card
                    prepend-icon="mdi-alert-circle-outline"
                    title="この投稿を削除しますか？"
                >
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            text="いいえ"
                            variant="plain"
                            @click="closeDelete"
                        ></v-btn>
                        <v-btn
                            color="primary"
                            text="はい"
                            variant="tonal"
                            @click="deleteItemConfirm"
                        ></v-btn>
                        <v-spacer></v-spacer>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </template>
    </div>
</template>

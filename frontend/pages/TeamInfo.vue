<script setup>
import RegisterButton from '~/components/pages/teaminfo/RegisterButton.vue';

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

const editTeamInfoDialog = ref(false);

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

const category = ['社会人', '大学', '高校', '中学', '小学'];

const isValid = computed(() => {
    return (
        editedTeamInfo.value.name &&
        editedTeamInfo.value.region &&
        editedTeamInfo.value.prefecture &&
        editedTeamInfo.value.category &&
        editedTeamInfo.value.league
    );
});

const editedTeamInfo = ref({
    id: teamInfo.value.id,
    name: teamInfo.value.name,
    region: teamInfo.value.region,
    prefecture: teamInfo.value.prefecture,
    category: teamInfo.value.category,
    league: teamInfo.value.league,
    instagram_user_name: teamInfo.value.instagram_user_name,
    X_user_name: teamInfo.value.X_user_name,
});

async function postEdit(id) {
    const updatedTeamInfo = await $fetch(
        `${runtimeConfig.public.apiUrl}/team_info/${id}/`,
        {
            method: 'PUT',
            body: editedTeamInfo.value,
        }
    );
    if (updatedTeamInfo) {
        editTeamInfoDialog.value = false;

        teamInfo.value = editedTeamInfo.value;
    }
}

function closeEditTeamInfoDialog() {
    editTeamInfoDialog.value = false;
    editedTeamInfo.value = teamInfo.value;
}

function handleTeamInfoRegisterd(newTeamInfo) {
    teamInfo.value = newTeamInfo;
}
</script>

<template>
    <!-- チーム情報が登録されていない場合 -->

    <div v-if="teamInfo === null">
        <v-empty-state
            class="d-flex align-center justify-center"
            style="min-height: 300px"
            icon="mdi-tshirt-crew"
            title="チーム情報が登録されていません"
            text="下記のボタンからチーム情報を登録してください"
            ><RegisterButton
                :idToken="idToken"
                :apiUrl="runtimeConfig.public.apiUrl"
                @TeamInfoRegisterd="handleTeamInfoRegisterd"
            />
        </v-empty-state>
    </div>

    <!-- チーム情報が登録されている場合 -->

    <div v-else>
        <!-- PC・タブレット用 -->

        <template v-if="smAndUp">
            <v-row>
                <v-col cols="12" class="d-flex align-end justify-end">
                    <!-- チーム情報編集ボタン -->
                    <v-btn
                        prepend-icon="mdi-text-box-edit-outline"
                        elevation="5"
                        @click="editTeamInfoDialog = true"
                        >チーム情報を編集</v-btn
                    >
                </v-col>
            </v-row>

            <v-row justify="center">
                <v-col cols="12" sm="12" md="12">
                    <v-card>
                        <v-row no-gutters>
                            <v-col cols="12" sm="6" md="6">
                                <v-card-title class="text-h4">{{
                                    teamInfo.name
                                }}</v-card-title>
                                <br />

                                <v-card-subtitle class="text-h6" opacity="100"
                                    >地域・・・{{
                                        teamInfo.region
                                    }}</v-card-subtitle
                                >
                                <br />

                                <v-card-subtitle class="text-h6" opacity="100"
                                    >都道府県・・・{{
                                        teamInfo.prefecture
                                    }}</v-card-subtitle
                                >
                                <br />

                                <v-card-subtitle class="text-h6" opacity="100"
                                    >カテゴリ・・・{{
                                        teamInfo.category
                                    }}</v-card-subtitle
                                >
                                <br />

                                <v-card-subtitle class="text-h6" opacity="100"
                                    >所属リーグ・・・{{
                                        teamInfo.league
                                    }}</v-card-subtitle
                                >
                                <br />

                                <v-card-subtitle class="text-h6" opacity="100"
                                    >SNSアカウント・・・<a
                                        v-if="teamInfo.instagram_user_name"
                                        :href="`https://www.instagram.com/${teamInfo.instagram_user_name}/`"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        <img
                                            src="../public/icons8-インスタグラム.svg"
                                            width="50"
                                            height="50"
                                            style="vertical-align: middle"
                                    /></a>
                                    <a
                                        v-if="teamInfo.X_user_name"
                                        :href="`https://x.com/${teamInfo.X_user_name}/`"
                                        target="_blank"
                                        rel="noopener noreferrer"
                                    >
                                        <img
                                            src="../public/icons8-ツイッターx.svg"
                                            width="50"
                                            height="50"
                                            style="vertical-align: middle"
                                    /></a>
                                </v-card-subtitle>
                            </v-col>

                            <v-col cols="12" sm="6" md="6">
                                <v-img
                                    src="https://cdn.pixabay.com/photo/2015/07/02/00/08/football-828218_1280.jpg"
                                    class="fill-height"
                                ></v-img>
                            </v-col>
                        </v-row>
                    </v-card>
                </v-col>
            </v-row>

            <!-- ダイアログ類 -->

            <!-- チーム情報編集ダイアログ -->
            <v-dialog v-model="editTeamInfoDialog" max-width="600">
                <v-card prepend-icon="mdi-tshirt-crew" title="チーム情報">
                    <v-card-text>
                        <v-row dense>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedTeamInfo.name"
                                    label="チーム名を入力"
                                    :rules="[required]"
                                    clearable
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="6">
                                <v-select
                                    v-model="editedTeamInfo.region"
                                    :items="regionsList"
                                    label="地域を選択"
                                ></v-select>
                            </v-col>
                            <v-col cols="6">
                                <v-select
                                    v-model="editedTeamInfo.prefecture"
                                    :items="regions[editedTeamInfo.region]"
                                    label="都道府県を選択"
                                ></v-select>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="6">
                                <v-select
                                    v-model="editedTeamInfo.category"
                                    :items="category"
                                    label="カテゴリを選択"
                                ></v-select>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedTeamInfo.league"
                                    label="所属リーグを入力"
                                    clearable
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="2">
                                <img
                                    src="../public/icons8-インスタグラム.svg"
                                    width="50"
                                    height="50"
                                    style="vertical-align: middle"
                                />
                            </v-col>
                            <v-col cols="10">
                                <v-text-field
                                    v-model="editedTeamInfo.instagram_user_name"
                                    label="ユーザー名を入力"
                                    clearable
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">
                                <img
                                    src="../public/icons8-ツイッターx.svg"
                                    width="50"
                                    height="50"
                                    style="vertical-align: middle"
                                />
                            </v-col>
                            <v-col cols="10">
                                <v-text-field
                                    v-model="editedTeamInfo.X_user_name"
                                    label="ユーザー名を入力"
                                    clearable
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn
                            text="キャンセル"
                            variant="plain"
                            @click="closeEditTeamInfoDialog()"
                        ></v-btn>

                        <v-btn
                            color="primary"
                            text="保存"
                            variant="tonal"
                            @click="postEdit(editedTeamInfo.id)"
                            :disabled="!isValid"
                        ></v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </template>

        <!-- スマホ用 -->

        <template v-else>
            <v-app-bar class="px-2" :elevation="1">
                <v-col cols="2"></v-col>

                <v-col class="d-flex justify-space-around">
                    <v-app-bar-title class="text-center"
                        >チーム情報</v-app-bar-title
                    >
                </v-col>

                <v-col cols="2" class="d-flex justify-end">
                    <!-- チーム情報編集ボタン -->
                    <v-btn
                        icon="mdi-text-box-edit-outline"
                        elevation="5"
                        @click="editTeamInfoDialog = true"
                    ></v-btn>
                </v-col>
            </v-app-bar>

            <v-row justify="center">
                <v-col cols="12" xs="12">
                    <v-card>
                        <v-img
                            src="https://cdn.pixabay.com/photo/2015/07/02/00/08/football-828218_1280.jpg"
                            class="fill-height"
                        ></v-img>

                        <v-card-item>
                            <v-card-title class="text-h5">{{
                                teamInfo.name
                            }}</v-card-title>
                            <br />

                            <v-card-subtitle class="text-h7" opacity="100"
                                >地域・・・{{
                                    teamInfo.region
                                }}</v-card-subtitle
                            >
                            <br />

                            <v-card-subtitle class="text-h7" opacity="100"
                                >都道府県・・・{{
                                    teamInfo.prefecture
                                }}</v-card-subtitle
                            >
                            <br />

                            <v-card-subtitle class="text-h7" opacity="100"
                                >カテゴリ・・・{{
                                    teamInfo.category
                                }}</v-card-subtitle
                            >
                            <br />

                            <v-card-subtitle class="text-h7" opacity="100"
                                >所属リーグ・・・{{
                                    teamInfo.league
                                }}</v-card-subtitle
                            >
                            <br />

                            <v-card-subtitle class="text-h7" opacity="100"
                                >SNSアカウント・・・<a
                                    v-if="teamInfo.instagram_user_name"
                                    :href="`https://www.instagram.com/${teamInfo.instagram_user_name}/`"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    <img
                                        src="../public/icons8-インスタグラム.svg"
                                        width="30"
                                        height="30"
                                        style="vertical-align: middle"
                                /></a>
                                <a
                                    v-if="teamInfo.X_user_name"
                                    :href="`https://x.com/${teamInfo.X_user_name}/`"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    <img
                                        src="../public/icons8-ツイッターx.svg"
                                        width="30"
                                        height="30"
                                        style="vertical-align: middle"
                                /></a>
                            </v-card-subtitle>
                        </v-card-item>
                    </v-card>
                </v-col>
            </v-row>

            <!-- ダイアログ類 -->

            <!-- チーム情報編集ダイアログ -->
            <v-dialog v-model="editTeamInfoDialog" max-width="600">
                <v-card prepend-icon="mdi-tshirt-crew" title="チーム情報">
                    <v-card-text>
                        <v-row dense>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedTeamInfo.name"
                                    label="チーム名を入力"
                                    :rules="[required]"
                                    clearable
                                    density="comfortable"
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="6">
                                <v-select
                                    v-model="editedTeamInfo.region"
                                    :items="regionsList"
                                    label="地域を選択"
                                    density="comfortable"
                                ></v-select>
                            </v-col>
                            <v-col cols="6">
                                <v-select
                                    v-model="editedTeamInfo.prefecture"
                                    :items="regions[editedTeamInfo.region]"
                                    label="都道府県を選択"
                                    density="comfortable"
                                ></v-select>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="6">
                                <v-select
                                    v-model="editedTeamInfo.category"
                                    :items="category"
                                    label="カテゴリを選択"
                                    density="comfortable"
                                ></v-select>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    v-model="editedTeamInfo.league"
                                    label="所属リーグを入力"
                                    clearable
                                    density="comfortable"
                                ></v-text-field>
                            </v-col>
                        </v-row>

                        <v-row>
                            <v-col cols="2">
                                <img
                                    src="../public/icons8-インスタグラム.svg"
                                    width="50"
                                    height="50"
                                    style="vertical-align: middle"
                                />
                            </v-col>
                            <v-col cols="10">
                                <v-text-field
                                    v-model="editedTeamInfo.instagram_user_name"
                                    label="ユーザー名を入力"
                                    clearable
                                    density="comfortable"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col cols="2">
                                <img
                                    src="../public/icons8-ツイッターx.svg"
                                    width="50"
                                    height="50"
                                    style="vertical-align: middle"
                                />
                            </v-col>
                            <v-col cols="10">
                                <v-text-field
                                    v-model="editedTeamInfo.X_user_name"
                                    label="ユーザー名を入力"
                                    clearable
                                    density="comfortable"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                        <v-spacer></v-spacer>

                        <v-btn
                            text="キャンセル"
                            variant="plain"
                            @click="closeEditTeamInfoDialog()"
                        ></v-btn>

                        <v-btn
                            color="primary"
                            text="保存"
                            variant="tonal"
                            @click="postEdit(editedTeamInfo.id)"
                            :disabled="!isValid"
                        ></v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </template>
    </div>
</template>

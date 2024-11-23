<script setup>
import RegisterButton from '~/components/pages/teaminfo/RegisterButton.vue';
import EditButton from '~/components/pages/teaminfo/EditButton.vue';
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

function handleTeamInfoRegisterd(newTeamInfo) {
    teamInfo.value = newTeamInfo;
}

function handleTeamInfoEdited(updatedTeamInfo) {
    teamInfo.value = updatedTeamInfo;
}
</script>

<template>
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

    <div v-else>
        <v-row class="d-flex align-end justify-end">
            <EditButton
                :idToken="idToken"
                :teamInfo="teamInfo"
                :apiUrl="runtimeConfig.public.apiUrl"
                @TeamInfoEdited="handleTeamInfoEdited"
            />
        </v-row>

        <template v-if="smAndUp">
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
        </template>

        <template v-else>
            <v-row justify="center">
                <v-col cols="12" xs="12">
                    <v-card>
                        <v-img
                            src="https://cdn.pixabay.com/photo/2015/07/02/00/08/football-828218_1280.jpg"
                            class="fill-height"
                        ></v-img>

                        <v-card-title class="text-h5">{{
                            teamInfo.name
                        }}</v-card-title>
                        <br />

                        <v-card-subtitle class="text-h7" opacity="100"
                            >地域・・・{{ teamInfo.region }}</v-card-subtitle
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
                    </v-card>
                </v-col>
            </v-row>
        </template>
    </div>
</template>

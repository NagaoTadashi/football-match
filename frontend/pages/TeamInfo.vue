<script setup>
import RegisterButton from '~/components/pages/teaminfo/RegisterButton.vue';
import EditButton from '~/components/pages/teaminfo/EditButton.vue';

const user = await getCurrentUser();
const idToken = await user.getIdToken();

const runtimeConfig = useRuntimeConfig();

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

console.log(teamInfo.value);
</script>

<template>
    <div>
        <div v-if="teamInfo === null">
            <v-empty-state
                class="d-flex align-center justify-center"
                style="min-height: 300px"
                icon="mdi-tshirt-crew"
                title="チーム情報が登録されていません"
                text="まずはじめに下記のボタンをクリックしてチーム情報を登録してください"
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

            <v-row justify="center">
                <v-col cols="12" sm="20" md="20">
                    <v-card>
                        <v-row no-gutters>
                            <v-col cols="12" sm="6">
                                <v-card-title class="text-h4">{{
                                    teamInfo.name
                                }}</v-card-title>
                                <br />

                                <v-card-subtitle class="text-h6"
                                    >地域:
                                    {{ teamInfo.region }}</v-card-subtitle
                                >
                                <br />

                                <v-card-subtitle class="text-h6"
                                    >都道府県:
                                    {{ teamInfo.prefecture }}</v-card-subtitle
                                >
                                <br />

                                <v-card-subtitle class="text-h6"
                                    >カテゴリ:
                                    {{ teamInfo.category }}</v-card-subtitle
                                >
                                <br />

                                <v-card-subtitle class="text-h6"
                                    >所属リーグ:
                                    {{ teamInfo.league }}</v-card-subtitle
                                >
                                <br />

                                <v-card-subtitle class="text-h6"
                                    >SNSアカウント:
                                    <a
                                        v-if="teamInfo.instagram_user_name"
                                        :href="`https://www.instagram.com/${teamInfo.instagram_user_name}/`"
                                        target="_blank"
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
                                    >
                                        <img
                                            src="../public/icons8-ツイッターx.svg"
                                            width="50"
                                            height="50"
                                            style="vertical-align: middle"
                                    /></a>
                                </v-card-subtitle>
                            </v-col>
                            <v-col cols="12" sm="6">
                                <v-img
                                    src="https://cdn.pixabay.com/photo/2015/07/02/00/08/football-828218_1280.jpg"
                                    class="fill-height"
                                ></v-img>
                            </v-col>
                        </v-row>
                    </v-card>
                </v-col>
            </v-row>
        </div>
    </div>
</template>

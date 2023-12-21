<template>
    <div class="relative z-10 max-w-screen-sm">
        <p v-if="userStore.user" class="fVeafc in">Hi {{ userStore.user.username }}</p>
        <p v-else class="fVeafc">unauthenticated</p>
        <h1 class="kKxhrq">
            基于大语言模型
            <br>
            法律问答系统
        </h1>
        <p class="kRTmDC">
            登录或注册使用大语言模型进行法律问答
        </p>
        <div class="uQxNj" v-if="userStore.user">
            <button @click="logout" class="ieMfVH" :disabled="loading">
                <span class="fKlELC" :class="{ loading: loading }">
                    Log out
                </span>
                <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="jjoFVh"
                    :class="{ loading: loading }">
                    <g fill="none" stroke-width="1.5" stroke-linecap="round" class="faEWLr"
                        style="stroke: var(--icon-color);">
                        <circle stroke-opacity=".2" cx="8" cy="8" r="6"></circle>
                        <circle cx="8" cy="8" r="6" class="VFMrX"></circle>
                    </g>
                </svg>
            </button>
        </div>
        <div class="uQxNj" v-else>
            <NuxtLink class="bQRHNT" to="/login">
                <span class="fKlELC">
                    Login
                    <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="taKtSf">
                        <path class="chevron" d="M8 13L13 8L8 3" stroke-width="1.5" stroke-linecap="square"
                            stroke-linejoin="round"></path>
                        <path class="stem" d="M12 8L2 8" stroke-width="1.5"></path>
                    </svg>
                </span>
            </NuxtLink>
            <NuxtLink to="/register">
                <button class="ieMfVH">
                    <span class="fKlELC">
                        Sign up
                    </span>
                </button>
            </NuxtLink>
    </div>
</div></template>

<script setup lang="ts">
import useUserStore from '~/stores/auth';
const userStore = useUserStore()
watchEffect(async () => {
    if (userStore.user) {
        await navigateTo('/conv')
    }
});


const loading = ref(false)

const logout = async () => {
    loading.value = true
    await userStore.logout()
}
</script>
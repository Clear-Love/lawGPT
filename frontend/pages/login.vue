<template>
  <div class="DaoRb">
    <h1 class="eSHwvX">登 录</h1>
    <form @submit.prevent="login">
      <ErrorAlert :error-msg="authError" @clearError="clearError" />
      <div class="jGQTZC">
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="text" placeholder="用户名或邮箱" v-model="username" />
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="password" placeholder="密码" v-model="password" />
          </div>
        </label>
      </div>
      <div class="jGQTZC">
        <button class="gZMQdu" type="submit" :disabled="loading">
          <div class="bjhGPG" :class="{loading: loading}">登 录</div>
          <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="jjoFVh" :class="{loading: loading}">
            <g fill="none" stroke-width="1.5" stroke-linecap="round" class="faEWLr" style="stroke: var(--icon-color);">
              <circle stroke-opacity=".2" cx="8" cy="8" r="6"></circle>
              <circle cx="8" cy="8" r="6" class="VFMrX"></circle>
            </g>
          </svg>
        </button>
        <NuxtLink to="/forgot-password" class="fTZPOV">忘记密码？</NuxtLink>
      </div>
    </form>
    <div class="jGQTZC">
      <p class="dEDhcH">还没有账号？</p>
      <NuxtLink to="/register">
        <button class="lcqpaS">
          <div class="bjhGPG">注册新账号</div>
        </button>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import useUserStore from '~/stores/auth';
import type { OAuth2PasswordRequestForm } from '~/types/auth/user';
definePageMeta({
  layout: "auth",
})
useHead({
  title: 'Login'
})
const userStore = useUserStore()
const loading = ref(false)
const authError = ref('')
const username = ref('')
const password = ref('')

watchEffect(async () => {
  if (userStore.user) {
    await navigateTo('/conv')
  }
});

const login = async () => {
  if (!username.value) return authError.value = '请输入用户名或邮箱';
  if (!password.value) return authError.value = '请输入密码';
  if (password.value.length < 6 || username.value.length > 32) {
    return authError.value = '密码长度应在6-32位'
  }
  loading.value = true
  try {
    await userStore.login({
      username: username.value,
      password: password.value
    } as OAuth2PasswordRequestForm)
    await userStore.fetchUserme()
    navigateTo('/conv')
  }catch (error) {
    loading.value = false
    authError.value = '用户名或密码错误'
    setTimeout(() => {
      authError.value = ''
    }, 5000)
  }
}

const clearError = () => {
  authError.value = '';
};
</script>

<template>
  <div class="DaoRb">
    <h1 class="eSHwvX">注 册</h1>
    <form @submit.prevent="handleClick">
        <ErrorAlert :error-msg="authError" @clearError="clearError" />
        <SuccessAlert :success-msg="authSuccess" @clearSuccess="clearSuccess" />
        <div class="jGQTZC">
          <label class="iJLvzO">
            <div class="fdCSlG">
              <input class="cmCuLh" type="text" placeholder="邮箱" v-model="email"/>
            </div>
          </label>
        </div>
        <div class="jGQTZC">
          <button class="gZMQdu" type="button" :disabled="loading">
            <div class="bjhGPG" :class="{ loading: loading }">获取验证码</div>
            <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="jjoFVh" :class="{ loading: loading }">
              <g fill="none" stroke-width="1.5" stroke-linecap="round" class="faEWLr" style="stroke: var(--icon-color);">
                <circle stroke-opacity=".2" cx="8" cy="8" r="6"></circle>
                <circle cx="8" cy="8" r="6" class="VFMrX"></circle>
              </g>
            </svg>
          </button>
        </div>
    </form>
    <form @submit.prevent="register" v-if="valid">
      <ErrorAlert :error-msg="authError" @clearError="clearError" />
      <SuccessAlert :success-msg="authSuccess" @clearSuccess="clearSuccess" />
      <div class="jGQTZC">
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="text" placeholder="用户名" v-model="username" />
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="password" placeholder="密码" v-model="password" />
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="password" placeholder="确认密码" v-model="repassword" />
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="text" placeholder="验证码" v-model="code" />
          </div>
        </label>
      </div>
      <div class="jGQTZC">
        <button class="gZMQdu" type="submit" :disabled="loading">
          <div class="bjhGPG" :class="{loading: loading}">注 册</div>
          <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="jjoFVh" :class="{loading: loading}">
            <g fill="none" stroke-width="1.5" stroke-linecap="round" class="faEWLr" style="stroke: var(--icon-color);">
              <circle stroke-opacity=".2" cx="8" cy="8" r="6"></circle>
              <circle cx="8" cy="8" r="6" class="VFMrX"></circle>
            </g>
          </svg>
        </button>
        <button class="gZMQdu" type="button" @click="back">
          <div class="bjhGPG" :class="{ loading: loading }">返回</div>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import useUserStore from '~/stores/auth';
import type { ErrorResponse } from '~/types';
import type { registerRequest, validEmailRequest } from '~/types/auth/user';

definePageMeta({
  layout: "auth"
})
useHead({
  title: 'Register'
})
const email = ref('')
const password = ref('')
const username = ref('')
const code = ref('')
const repassword = ref('')
const loading = ref(false)
const valid = ref(false);
const authError = ref('')
const authSuccess = ref('')
const userStore = useUserStore()
watchEffect(async () => {
  if (userStore.user) {
    await navigateTo('/')
  }
});

function validEmail(email: string): boolean {
  // 正则表达式模式用于验证电子邮件地址
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  // 使用正则表达式模式测试电子邮件地址
  return pattern.test(email)
}

async function handleClick() {
  if (!validEmail(email.value)) {
    return authError.value = '请输入正确的邮件地址'
  }
  loading.value = true
  await fetch(
    '/api/auth/sendValidEmail',
    {
      method: "post",
      body: JSON.stringify({
          email: email.value,
        } as validEmailRequest)
    }
  ).then(response => {
    if (response.ok) {
      valid.value = true
      authSuccess.value = `邮件发送成功`
      setTimeout(() => {
        authSuccess.value = ''
      }, 5000)
    } else {
      console.log(response)
      return response.json().then((data: ErrorResponse) => {
        const detail = data.detail;
        authError.value = detail
        setTimeout(() => {
          authSuccess.value = ''
        }, 5000)
      });
    }
  }).catch((e) => {
    console.log(e)
    authError.value = "网络错误"
  });
  loading.value = false
}



const register = async () => {
  if (!username.value) return authError.value = '请输入用户名';
  if (!email.value) return authError.value = '请输入邮箱';
  if (!password.value) return authError.value = '请输入密码';
  if (!repassword.value) return authError.value = '请确认密码';
  if (username.value.length < 4 || username.value.length > 12) {
    return authError.value = '用户名长度应在4-16位'
  }
  if (password.value.length < 6 || username.value.length > 32) {
    return authError.value = '密码长度应在6-32位'
  }
  if (password.value !== repassword.value) return authError.value = '输入密码不一致';
  if (!code.value) return authError.value = '请输入验证码';
  loading.value = true
  await fetch(
    '/api/auth/register',
    {
      method: "post",
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        code: code.value,
      } as registerRequest)
    }
  ).then(response =>{
    if (response.ok) {
      authSuccess.value = `注册成功，返回登录页面`
      setTimeout(() => {
        authSuccess.value = ''
        navigateTo('/login')
      }, 2000)
    } else {
      response.json().then((data: ErrorResponse) => {
        const detail = data.detail;
        authError.value = detail
        setTimeout(() => {
          authSuccess.value = ''
        }, 5000)
      });
    }
  }).catch((e) => {
      console.log(e)
      authError.value = "网络错误"
    });
  loading.value = false
}

function back() {
  valid.value = false
}

const clearError = () => {
  authError.value = ''
}

const clearSuccess = () => {
  authSuccess.value = '';
};
</script>

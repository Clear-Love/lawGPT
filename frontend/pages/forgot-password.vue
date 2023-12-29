<template>
  <div class="DaoRb">
    <h1 class="eSHwvX">{{ valid? "设定新密码": "忘记密码" }}</h1>
    <form @submit.prevent="resetPassword" v-if="!valid">
      <ErrorAlert :error-msg="authError" @clearError="clearError" />
      <SuccessAlert :success-msg="authSuccess" @clearSuccess="clearSuccess" />
      <div class="jGQTZC">
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="text" placeholder="电子邮件地址" v-model="email">
          </div>
        </label>
      </div>
      <button class="gZMQdu" type="submit" :disabled="loading">
        <div class="bjhGPG" :class="{loading: loading}">验 证</div>
        <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="jjoFVh" :class="{loading: loading}">
          <g fill="none" stroke-width="1.5" stroke-linecap="round" class="faEWLr" style="stroke: var(--icon-color);">
            <circle stroke-opacity=".2" cx="8" cy="8" r="6"></circle>
            <circle cx="8" cy="8" r="6" class="VFMrX"></circle>
          </g>
        </svg>
      </button>
    </form>
    <form @submit.prevent="updatepassword" v-if="valid">
      <ErrorAlert :error-msg="authError" @clearError="clearError" />
      <SuccessAlert :success-msg="authSuccess" @clearSuccess="clearSuccess" />
      <div class="jGQTZC">
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="password" placeholder="密码" v-model="password" />
          </div>
        </label>
        <label class="iJLvzO">
          <div class="fdCSlG">
            <input class="cmCuLh" type="password" placeholder="确认密码" v-model="passwordConfirm" />
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
          <div class="bjhGPG" :class="{ loading: loading }">保存</div>
          <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="jjoFVh" :class="{ loading: loading }">
            <g fill="none" stroke-width="1.5" stroke-linecap="round" class="faEWLr" style="stroke: var(--icon-color);">
              <circle stroke-opacity=".2" cx="8" cy="8" r="6"></circle>
              <circle cx="8" cy="8" r="6" class="VFMrX"></circle>
            </g>
          </svg>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import type { ErrorResponse } from '~/types/api';
import type { resetPasswordRequest, validEmailRequest } from '~/types/auth/user';
definePageMeta({
  layout: "auth"
})
useHead({
  title: 'Forgot Password'
})
const valid = ref(false)
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const loading = ref(false)
const authSuccess = ref('')
const authError = ref('')
const code = ref('')

const resetPassword = async () => {
  loading.value = true
  await fetch(
    '/api/auth/sendResetEmail',
    {
      method: "post",
      body: JSON.stringify({
        email: email.value,
      } as validEmailRequest)
    }
  ).then(
    response => {
      if (response.ok) {
        loading.value = false
        authSuccess.value = `成功发送验证邮件`
        valid.value = true
        setTimeout(() => {
          authSuccess.value = ''
        }, 5000)
      }else {
        response.json().then((data: ErrorResponse) => {
          authError.value = data.detail
          setTimeout(() => {
            authError.value = ''
          }, 5000)
        })
      }
    }
  ).catch((e) => {
    console.log(e)
    authError.value = "网络错误"
  })
  loading.value = false
}
  

const updatepassword = async () => {
  if (password.value !== passwordConfirm.value) return authError.value = '两次输入密码不一致';
  if (code.value.length != 6) return authError.value = '请输入六位验证码'
  if (!email.value) return authError.value = '请验证邮箱后再修改密码'
  loading.value = true
  await fetch(
    '/api/auth/reset',
    {
      method: "post",
      body: JSON.stringify({
        email: email.value,
        password: password.value,
        code: code.value
      } as resetPasswordRequest)
    }
  ).then(response => {
    if (response.ok) {
      authSuccess.value = `密码修改成功`
      setTimeout(() => {
        authSuccess.value = ''
        navigateTo('/login')
      }, 2000)
    }else {
      response.json().then((data: ErrorResponse) => {
        authError.value = data.detail
        setTimeout(() => {
          authError.value = ''
        }, 5000)
      })
    }
  }).catch((e) => {
    authError.value = "网络错误"
    console.log(e)
  })
  loading.value = false
}

const clearError = () => {
  authError.value = '';
};

const clearSuccess = () => {
  authSuccess.value = '';
};
</script>

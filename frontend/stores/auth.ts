import { defineStore } from 'pinia';
import { clearCookie } from '@/utils/auth';
import type { OAuth2PasswordRequestForm, UserResponse } from '~/types/auth/user';

const useUserStore = defineStore('user',() => {
    const user = ref<UserResponse>(getUser());

    function getUser() {
        const data = localStorage.getItem('user')
        return data? JSON.parse(data) : null
    }
    async function login(data: OAuth2PasswordRequestForm) {
        try {
            await $fetch.raw(
                '/api/auth/login', {
                    method: "post",
                    body: data,
                }
            );
        }catch(err){
            clearCookie()
            throw err
        }
    }

    async function logout() {
        try {
            localStorage.removeItem('user')
            user.value = getUser()
            clearCookie()
            await $fetch(
                '/api/auth/logout', 
                {
                method: "post",
            }
            );
        } catch (err) {
            throw err
        }
    }

    async function fetchUserme() {
        const data = await $fetch(
            '/api/auth/user/me'
        ) as UserResponse
        localStorage.setItem('user', JSON.stringify(data));
        user.value = getUser()
    }

    return {
        user,
        login,
        logout,
        fetchUserme,
    }
});

export default useUserStore;

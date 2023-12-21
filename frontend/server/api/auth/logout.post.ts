import { errorHandler, setResStatus } from "~/server/utils/h3";
import { AuthResponse } from "~/types/auth/user";


export default defineEventHandler(async (event) => {
    try {
        const headers = getHeaders(event);
        const axiosInstance = createAxiosInstance({
            responseType: "json",
            timeout: 1000 * 20,
            timeoutErrorMessage: "**Network connection timed out. Please try again**",
            baseURL: useRuntimeConfig().baseUrl,
            headers: headers
        })
        console.log(process.env.NUXT_BASE_URL)
        const response = await axiosInstance.post<AuthResponse>('/api/auth/logout')
        setResStatus(event, response.status, response.statusText);
        return response.data;
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});

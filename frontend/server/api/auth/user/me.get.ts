import { errorHandler, setResStatus } from "~/server/utils/h3";
import { UserResponse } from "~/types/auth/user";


export default defineEventHandler(async (event) => {
    try {
        const headers = getHeaders(event);
        const axiosInstance = createAxiosInstance({
                responseType: "json",
                timeout: 1000 * 20,
                timeoutErrorMessage: "**Network connection timed out. Please try again**",
                baseURL: process.env.NUXT_BASE_URL,
                headers: headers
            })
        const response = await axiosInstance.get<UserResponse>('/api/auth/user/me')
        setResStatus(event, response.status, response.statusText);
        return response.data
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});

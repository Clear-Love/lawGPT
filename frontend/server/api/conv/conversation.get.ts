import { errorHandler, setResStatus } from "~/server/utils/h3";
import { ConversationItem } from "~/types";
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
        const response = await axiosInstance.get<ConversationItem[]>('/api/conv/conversation')
        setResStatus(event, response.status, response.statusText);
        return response.data;
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});
import { errorHandler, setResStatus } from "~/server/utils/h3";
import { ConversationHistory } from "~/types";


export default defineEventHandler(async (event) => {
    try {
        const conversation_id = getRouterParam(event, 'uuid')
        const headers = getHeaders(event);
        const axiosInstance = createAxiosInstance({
            responseType: "json",
            timeout: 1000 * 20,
            timeoutErrorMessage: "**Network connection timed out. Please try again**",
            baseURL: useRuntimeConfig().baseUrl,
            headers: headers
        })
        const response = await axiosInstance.get<ConversationHistory>(`/api/conv/messages/${conversation_id}`);
        setResStatus(event, response.status, response.statusText);
        return response.data;
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});
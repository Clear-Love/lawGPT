import { errorHandler, setResStatus } from "~/server/utils/h3";
import { ChatMessage, ChatMessageItem } from "~/types";


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
        const body = (await readBody(event)) as ChatMessage;
        const response = await axiosInstance.post<ChatMessageItem>(`/api/conv/newmessage/${conversation_id}`, body);
        setResStatus(event, response.status, response.statusText);
        return response.data;
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});
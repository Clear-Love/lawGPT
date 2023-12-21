import { errorHandler, setResStatus } from "~/server/utils/h3";
import { ConversationItem, CreateConversationRequest } from "~/types";


export default defineEventHandler(async (event) => {
    try {
        const headers = getHeaders(event);
        headers['Content-Type'] = 'application/json'
        const axiosInstance = createAxiosInstance({
            responseType: "json",
            timeout: 1000 * 20,
            timeoutErrorMessage: "**Network connection timed out. Please try again**",
            baseURL: useRuntimeConfig().baseUrl,
            headers: headers
        })
        const body = (await readBody(event)) as CreateConversationRequest;
        const response = await axiosInstance.post<ConversationItem>('/api/conv/new', body)
        setResStatus(event, response.status, response.statusText);
        return response.data;
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});
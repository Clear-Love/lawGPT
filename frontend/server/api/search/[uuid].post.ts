import { errorHandler, setResStatus } from "~/server/utils/h3";
import { ChatCompletionRequest, SearchResponse } from "~/types";


export default defineEventHandler(async (event) => {
    try {
        const conversation_id = getRouterParam(event, 'uuid')
        const headers = getHeaders(event);
        headers['Content-Type'] = 'application/json'
        const axiosInstance = createAxiosInstance({
            responseType: "json",
            timeout: 1000 * 20,
            timeoutErrorMessage: "**Network connection timed out. Please try again**",
            baseURL: useRuntimeConfig().baseUrl,
            headers: headers
        })
        const body = (await readBody(event)) as ChatCompletionRequest;
        const response = await axiosInstance.post<SearchResponse>(`/api/search/${conversation_id}`, body);
        setResStatus(event, response.status, response.statusText);
        return response.data;
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});
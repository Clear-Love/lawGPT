import { errorHandler, setResStatus } from "~/server/utils/h3";
import { AuthResponse, registerRequest } from "~/types/auth/user";


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
        const body = (await readBody(event)) as registerRequest;
        const response = await axiosInstance.post<AuthResponse>('/api/auth/register', body)
        setResStatus(event, response.status, response.statusText);
        return response.data;
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});
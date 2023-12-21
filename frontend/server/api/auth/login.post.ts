import { errorHandler, setResStatus } from "~/server/utils/h3";
import { AuthResponse, OAuth2PasswordRequestForm} from "~/types/auth/user";

const axiosInstance = createAxiosInstance({
    responseType: "json",
    timeout: 1000 * 20,
    timeoutErrorMessage: "**Network connection timed out. Please try again**",
    baseURL: useRuntimeConfig().baseUrl,
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
})
export default defineEventHandler(async (event) => {
    try {
        const body = (await readBody(event)) as OAuth2PasswordRequestForm;
        const response = await axiosInstance.post<AuthResponse>('/api/auth/login', createFormData(body))
        setResStatus(event, response.status, response.statusText);
        const cookies = response.headers['set-cookie'] || []
        for (const cookie of cookies) {
            appendResponseHeader(event, 'set-cookie', cookie)
        }
        return response.data
    } catch (e: any) {
        return await errorHandler(event, e);
    }
});

// 创建 FormData 对象并填充数据
function createFormData(data: OAuth2PasswordRequestForm): FormData {
    const formData = new FormData();
    Object.entries(data).forEach(([key, value]) => {
        if (value !== null && value !== undefined) {
            formData.set(key, value);
        }
    });
    
    return formData;
}
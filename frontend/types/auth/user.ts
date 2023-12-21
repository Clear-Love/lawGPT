export interface UserResponse {
    id: number
    username: string
    nickname: string | null
    email: string
    avatar: string
    last_active_time: string
    create_time: string
    is_superuser: boolean
    is_verified: boolean
    is_active: boolean
}

export interface OAuth2PasswordRequestForm {
    grant_type: string | null
    username: string
    password: string
    scopes: string | null
    client_id: string | null
    client_secret: string | null
}

export interface AuthResponse {
    code: number
    message: string,
    result: any | null
}

export interface validEmailRequest {
    email: string
}

export interface registerRequest {
    email: string,
    password: string,
    username: string,
    code: string
}

export interface resetPasswordRequest {
    password: string,
    email: string,
    code: string
}
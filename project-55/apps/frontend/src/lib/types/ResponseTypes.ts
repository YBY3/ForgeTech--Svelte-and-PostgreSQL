export type ErrorResponseType = {
    success: boolean,
    response: {status: number, error: string, message: string | null};
}
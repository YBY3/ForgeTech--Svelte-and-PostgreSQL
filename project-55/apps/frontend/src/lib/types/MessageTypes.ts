export type MessageType = {
    id: number;
    thread_id: number;
    user_id: number;
    responding_to_id: number | null;
    message: string;
};
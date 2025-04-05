declare global {
    namespace App {
        interface Locals {
            user?: {
                id: number;
                username: string;
                email: string;
                name: string | null;
                profile_pic: string | null;
                user_type: string;
                registered_by: string;
                active_by: string;
            } | null;
        }
    }
}

export {};
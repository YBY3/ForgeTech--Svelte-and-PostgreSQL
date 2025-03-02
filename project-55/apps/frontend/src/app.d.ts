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
            } | null;
        }
    }
}

export {};
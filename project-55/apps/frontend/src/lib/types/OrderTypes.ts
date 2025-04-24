import type { ProductOrderPreviewType } from "./ProductTypes";

export type OrderType = {
    id: number;
    user_id: number;
    products: ProductOrderPreviewType[]
    status: string;
    total: number;
    created_at: string;
    claimed_by_employee_id?: number;
    arrive_by: number;
    hidden: boolean;
};


export type PastOrderType = { //what is this?
    id: number;
    user_id: number;
    products: ProductPreviewType[]
    status: string;
    total: number;
    created_at: string;
    claimed_by_employee_id?: number;
    arrive_by: number;
    hidden: boolean;
};
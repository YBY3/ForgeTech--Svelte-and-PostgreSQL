import type { ProductPreviewType } from "./ProductTypes";


export type PastOrderType = {
    id: number;
    user_id: number;
    products: ProductPreviewType[]
    // product_ids: number[]; // Updated property: now an array of numbers
    status: string;
    total: number;
    created_at: string;
    claimed_by_employee_id?: number;
};
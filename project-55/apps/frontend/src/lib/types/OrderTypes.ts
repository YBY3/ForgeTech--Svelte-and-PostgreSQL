import type { ProductPreviewType } from "./ProductTypes";


export type PastOrderType = {
    id: number;
    user_id: number;
    products: ProductPreviewType[]
    status: string;
    total: string;
};
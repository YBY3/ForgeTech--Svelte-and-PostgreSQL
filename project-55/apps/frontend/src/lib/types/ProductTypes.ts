export type RawProductType = {
    id: number;
    name: string;
    price: number;
    description: string;
    brand: string;
    options: string[];
    product_type: string;
    product_stock: number;
    image_ids: number[];
    quantity: number;
};


export type ProductType = {
    id: number;
    name: string;
    price: number;
    description: string;
    brand: string;
    options: string[];
    product_type: string;
    product_stock: number;
    image_ids: number[];
    image_urls: string[];
    quanity: number;
};


export type ProductPreviewType = {
    id: number;
    name: string;
    price: number;
    quantity: number;
}
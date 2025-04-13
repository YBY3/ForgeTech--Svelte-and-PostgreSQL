//This file will store types related to products

//Named it ProductType to Avoid Naming Conflicts
export type ProductType = {
    id: number;
    name: string;
    price: number;
    description: string;
    brand: string;
    options: string[];
    images: number[];
    product_type: string;
    product_stock: number;
};


export type ProductPreviewType = {
    id: number;
    name: string;
    price: number;
}
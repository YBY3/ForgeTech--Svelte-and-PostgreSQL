//This file will store types related to products

//Named it ProductType to Avoid Naming Conflicts
export type ProductType = {
    id: number;
    name: string;
    price: number;
    description: string;
    components: string[];
    image: string;
};
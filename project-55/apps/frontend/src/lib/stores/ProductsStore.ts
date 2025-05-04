import { writable } from "svelte/store";
import type { ProductType } from "$lib/types/ProductTypes"

export const productsStore = writable<ProductType[]>([]);


export function replaceProductInStore(updatedProduct: ProductType) {
    productsStore.update(products =>
        products.map(product => (product.id === updatedProduct.id ? updatedProduct : product))
    );
}

export function addProductToStore(product: ProductType) {
    productsStore.update(products => [...products, product]);
}

export function deleteProductFromStore(productId: string | number) {
    productsStore.update(products => products.filter(p => p.id !== productId));
}
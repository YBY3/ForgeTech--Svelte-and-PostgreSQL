import { writable } from "svelte/store";
import type { ProductType } from "$lib/types/ProductTypes"

export const ordersStore = writable<ProductType[]>([]);


export function addToOrder(product: ProductType) {
    ordersStore.update(currentOrder => {
    return [...currentOrder, product];
  });
}


export function removeFromOrder(productId: number) {
    ordersStore.update(currentOrder => {
    return currentOrder.filter(product => product.id !== productId);
  });
}
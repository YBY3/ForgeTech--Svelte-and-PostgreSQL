// src/lib/stores/OrdersStore.ts
import { writable } from "svelte/store";
import type { ProductType } from "$lib/types/ProductTypes";

/**  
 * Holds full ProductType entries—including their new
 * quantity & product_option fields—for your cart.
 */
export const ordersStore = writable<ProductType[]>([]);

/**  
 * Pushes one ProductType (with quantity + product_option)
 * into the cart array.
 */
export function addToOrder(product: ProductType) {
  ordersStore.update(current => [...current, product]);
}

/**  
 * Removes the first matching product.id from the cart.
 */
export function removeFromOrder(productId: number) {
  ordersStore.update(current => {
    const idx = current.findIndex(p => p.id === productId);
    if (idx !== -1) current.splice(idx, 1);
    return [...current];
  });
}

import { writable } from "svelte/store";
import type { ProductType } from "$lib/types/ProductTypes"

export const productsStore = writable<ProductType[]>([]);
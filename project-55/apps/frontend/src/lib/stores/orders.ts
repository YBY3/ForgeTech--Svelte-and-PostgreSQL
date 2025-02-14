import { writable } from "svelte/store";

export type Product = {
  id: number;
  name: string;
  price: number;
  description: string;
  components: string[];
  image: string;
};

// Store for all products
export const productStore = writable<Product[]>([
  { id: 1, name: "Sample GPU", price: 9.99, description: "Graphics Processing Unit", components: ["Color", "Make", "Year"], image: "/catalog-images/gpu.jpg" },
  { id: 2, name: "Sample CPU", price: 12.49, description: "Central Processing Unit", components: ["Color", "Make", "Year"], image: "/catalog-images/cpu.jpg" },
  { id: 3, name: "Sample Keyboard", price: 8.99, description: "Wireless Bluetooth Keyboard", components: ["Color", "Make", "Year"], image: "/catalog-images/keyboard.jpg" },
  // { id: 4, name: "Sample Monitor", price: 149.99, description: "27-inch LED Monitor", components: ["Resolution", "Size", "Refresh Rate"], image: "/catalog-images/monitor.jpg" }
  { id: 4, name: "Sample GPU", price: 9.99, description: "Graphics Processing Unit", components: ["Color", "Make", "Year"], image: "/catalog-images/gpu.jpg" },
  { id: 5, name: "Sample CPU", price: 12.49, description: "Central Processing Unit", components: ["Color", "Make", "Year"], image: "/catalog-images/cpu.jpg" },
  { id: 6, name: "Sample Keyboard", price: 8.99, description: "Wireless Bluetooth Keyboard", components: ["Color", "Make", "Year"], image: "/catalog-images/keyboard.jpg" },
]);

// Store for the selected product
export const selectedProduct = writable<Product | null>(null);

// ✅ Order Store
export const orderStore = writable<Product[]>([]);

// ✅ Function to add a product to the order
export function addToOrder(product: Product) {
  orderStore.update(currentOrder => {
    return [...currentOrder, product]; // Adds product while maintaining order
  });
}

// ✅ Function to remove a product from the order by ID
export function removeFromOrder(productId: number) {
  orderStore.update(currentOrder => {
    return currentOrder.filter(product => product.id !== productId);
  });
}
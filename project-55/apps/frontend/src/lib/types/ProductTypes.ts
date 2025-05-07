// src/lib/types/ProductTypes.ts

export type RawProductType = {
  id:             number;
  name:           string;
  price:          number;
  description:    string;
  brand:          string;
  options:        string[];
  product_type:   string;
  product_stock:  number;
  image_ids:      number[];
};

// YOUR main ProductType, now with optional quantity & option:
export type ProductType = {
  id:               number;
  product_id:       number;
  name:             string;
  price:            number;
  description:      string;
  brand:            string;
  options:          string[];
  product_type:     string;
  product_stock:    number;
  hidden:           boolean;
  image_ids:        number[];
  image_urls:       string[];
  // ← NEW fields for the cart
  quantity?:        number;
  product_option?:  string;
};

export type ProductPreviewType = {
  id:    number;
  name:  string;
  price: number;
  quantity: number;
};

export type ProductOrderPreviewType = {
  id:       number;
  name:     string;
  price:    number;
  quantity: number;
  // if you use this in your orders list:
  product_option?: string;
};

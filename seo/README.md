# SEO copy for fishscalegaffs.com

Source of truth for the product and collection copy pushed to Shopify on 2026-09-24.

- `products.json`: input list (product id, handle, title, starting price, hook finish per colorway).
- `generate_product_copy.py`: builds a description, SEO title and meta description for each product from its
  real options (lengths, actions, hook styles, spike sizes, sheath/butt-cap add-ons) and FAQ facts
  (5–7 / 8–12 business-day lead times). Run `python3 generate_product_copy.py` to regenerate `product_copy.json`.
- `product_copy.json`: generated copy for 54 products, as applied via `productUpdate`.
- `collection_copy.json`: copy for the 6 collections, as applied via `collectionUpdate`.

Related fix applied the same day: 11 Calcutta gaffs had the 4ft / Heavy / Mustad 3/0 variant priced at $17.99;
it was corrected to $174.99 to match the neighbouring variants.

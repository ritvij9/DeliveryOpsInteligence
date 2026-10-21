# DeliveryOps Intelligence — Data Reconnaissance

## 1. Objective

Inspect the Olist Brazilian E-Commerce Public Dataset before designing analytical transformations for delivery performance and customer satisfaction.

## 2. Source inventory

Nine CSV files were inspected.

| Source file | Rows | Columns |
|---|---:|---:|
| Customers | 99,441 | 5 |
| Geolocation | 1,000,163 | 5 |
| Order items | 112,650 | 7 |
| Payments | 103,886 | 5 |
| Reviews | 99,224 | 7 |
| Orders | 99,441 | 8 |
| Products | 32,951 | 9 |
| Sellers | 3,095 | 4 |
| Category translation | 71 | 2 |

## 3. Initial data quality findings

- The customers, order items, payments, orders, products, sellers, and category translation files have zero completely duplicated rows.
- The geolocation file has 261,831 completely duplicated rows out of 1,000,163.
- The review file has zero completely duplicated rows.
- The orders file contains 2,965 missing customer-delivery timestamps and 1,783 missing carrier-handover timestamps.
- Review titles are missing in 87,656 rows (88.34%); review messages are missing in 58,247 rows (58.70%).
- The products file has 610 missing category names and two rows with missing physical measurements.

## 4. Key and relationship checks

- `customer_id` is unique in the customers file and in the observed orders file.
- `order_id` is unique in the orders file.
- (`order_id`, `order_item_id`) is unique in order items.
- (`order_id`, `payment_sequential`) is unique in payments.
- `product_id` and `seller_id` are unique in their respective dimension files.
- All six tested foreign-key relationships had zero unmatched child rows.
- The reviews file has 814 duplicate-key rows when checked by `review_id` and 551 when checked by `order_id`.

## 5. Review investigation

- Total review rows: 99,224.
- Distinct review IDs: 98,410.
- Distinct order IDs: 98,673.
- Completely duplicated review rows: zero.
- Sampled records show review IDs reused across orders and orders with multiple review IDs.

Therefore, neither `review_id` nor `order_id` should be assumed to be a unique key in the raw review file. No review records have been removed.

## 6. Limitations and open questions

- Timestamp parsing, chronological validity, and delivery metric definitions have not yet been validated.
- Geolocation duplication needs grain-level investigation before any deduplication or geographic joins.
- The review table's appropriate analytical grain remains unresolved.
- Key uniqueness and foreign-key checks were performed using pandas scripts; automated tests and SQL transformations have not yet been implemented.
- These are historical observations from the supplied dataset, not current marketplace performance.

## 7. Reproducibility

Inspection scripts:

- `scripts/inspect_data.py`
- `scripts/check_relationships.py`
- `scripts/investigate_reviews.py`

Run them from the project root with the project's Python environment activated.

## 8. Geolocation grain investigation

The geolocation source contains 1,000,163 rows and 19,015 distinct postal-code prefixes.

| Check | Result |
|---|---:|
| Rows beyond the first occurrence of a postal prefix | 981,148 |
| Distinct prefix-coordinate combinations | 720,154 |
| Rows beyond the first occurrence of a prefix-coordinate combination | 280,009 |
| Prefixes with multiple city names | 8,556 |
| Prefixes with multiple states | 8 |
| Prefixes with multiple latitude values | 17,781 |
| Prefixes with multiple longitude values | 17,780 |

A sample of prefix `1037` contains multiple coordinates and repeated coordinate combinations. The sample also contains city-name variation, including `sao paulo` and `são paulo`.

**Decision:** Do not join the raw geolocation table directly to customer or seller records using only the postal prefix. Do not arbitrarily select one coordinate per prefix. Geographic enrichment is deferred until a defensible lookup or aggregation method is established.

The core delivery analysis can begin using the customer and seller location attributes supplied in their respective source tables.

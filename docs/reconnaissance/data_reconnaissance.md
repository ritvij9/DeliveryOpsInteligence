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

## 9. Delivery timestamp validation and baseline KPI

### Timestamp validation

The five order timestamps were parsed as datetimes and checked for missing values and chronological inconsistencies.

| Validation check | Result |
|---|---:|
| Carrier handoff before purchase | 166 orders |
| Customer delivery before carrier handoff | 23 orders |
| Orders with at least one chronology violation | 189 orders |
| Late orders that also have chronology violations | 3 orders |

The violations overlap: 189 is the distinct-order count with at least one of the two chronology issues, not the sum of both violation counts.

### Missing customer-delivery timestamps

A total of 2,965 orders lack a customer-delivery timestamp.

| Order status | Missing timestamps |
|---|---:|
| Shipped | 1,107 |
| Canceled | 619 |
| Unavailable | 609 |
| Invoiced | 314 |
| Processing | 301 |
| Delivered | 8 |
| Created | 5 |
| Approved | 2 |
| **Total** | **2,965** |

The eight orders marked `delivered` despite missing customer-delivery timestamps were inspected separately. Seven have a carrier-handoff timestamp; one has neither a carrier-handoff nor a customer-delivery timestamp. Their actual delivery timeliness cannot be established from the available timestamps.

### Baseline late-delivery KPI

**Definition:** The percentage of orders with both actual customer-delivery and estimated-delivery timestamps for which actual customer delivery occurred after the estimated delivery timestamp.

Formula:

Late delivery rate = (orders delivered after estimate / orders with both timestamps) × 100

| Metric | Result |
|---|---:|
| Total orders | 99,441 |
| Orders with actual customer-delivery timestamp | 96,476 |
| Orders with both actual and estimated delivery timestamps | 96,476 |
| Orders delivered after estimate | 7,827 |
| Baseline late-delivery rate | 8.11% |

Orders without an actual customer-delivery timestamp are excluded from this baseline calculation, not classified as on time or late. Missing timestamps and chronology violations should be reported as separate data-quality measures.

This is an initial descriptive baseline for the supplied historical dataset, not a validated current business-performance benchmark. Before finalizing the KPI, the analysis should explicitly define the eligible order population and treatment of order statuses.

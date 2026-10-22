# DeliveryOps Intelligence

**An end-to-end e-commerce delivery analytics project using Python, SQL, DuckDB, pandas, and Streamlit.**

DeliveryOps Intelligence analyzes historical e-commerce orders to identify delivery-performance patterns, investigate potential sources of delays, and translate findings into operational investigation priorities.

## 1. Business Problem

Late deliveries can affect customer experience and operational efficiency. However, an overall late-delivery rate does not explain where delays occur or which segments deserve further investigation.

This project addresses five business questions:

- How does late-delivery performance vary across customer states?
- How does delivery performance change over time?
- Which sellers have high late-delivery rates or contribute large volumes of late orders?
- At which delivery stage are the largest differences between late and on-time orders observed?
- Which seller–state combinations warrant deeper operational investigation?

## 2. Dataset

The project uses the public Olist Brazilian e-commerce dataset.

The data includes orders, customers, order items, payments, reviews, products, sellers, geolocation records, and product-category translations.

The analysis focuses on orders with both actual customer-delivery timestamps and estimated delivery timestamps.

**Baseline population:** 96,476 eligible orders from 99,441 orders in the dataset.

## 3. Technology Stack

- **Python** — analytical workflows and data processing
- **DuckDB** — SQL-based analysis and querying CSV and Parquet data
- **pandas** — data manipulation and aggregation
- **Streamlit** — interactive dashboard
- **pytest** — automated data-quality tests
- **Git** — version control

## 4. Analytical Methodology

### Data reconnaissance and validation

- Inspected dataset sizes, columns, missing values, and key uniqueness.
- Checked relationships between orders, customers, products, sellers, and payments.
- Investigated duplicate review keys and the grain of geolocation records.
- Validated timestamp availability and chronology.
- Created automated tests for important data-quality constraints.

### Analytical dataset construction

Created a reproducible order-level analytical dataset in Parquet format.

The dataset includes delivery timestamps, delivery-status indicators, delivery-stage durations, and indicators for late delivery and timestamp chronology issues.

### Exploratory and diagnostic analysis

The project investigates:

1. Late-delivery rates and order volumes by customer state.
2. Monthly delivery performance.
3. Seller-level late-delivery rates, volumes, and delay severity.
4. Approval-to-carrier and carrier-to-customer stage durations.
5. Seller–state performance relative to state-level baselines.

### Interactive dashboard

The Streamlit dashboard provides:

- Summary KPIs
- Monthly delivery-performance charts
- State-level comparisons
- Seller-performance analysis
- Filters for purchase month and customer state
- Adjustable minimum order thresholds
- CSV export of filtered eligible orders

## 5. Key Findings

### Overall delivery performance

| Metric | Result |
|---|---:|
| Total orders | 99,441 |
| Eligible orders | 96,476 |
| Late orders | 7,827 |
| Late-delivery rate | 8.11% |
| Average days late among late orders | 9.53 days |

An order is considered late when its actual customer-delivery timestamp is later than its estimated delivery timestamp.

### Geographic variation

- Maranhão (MA) recorded a late-delivery rate of **19.67%**, with 141 late orders among 717 eligible orders.
- Rio de Janeiro (RJ) recorded **1,664 late orders**, with a late-delivery rate of 13.47%.
- São Paulo (SP) recorded 2,387 late orders, despite a lower late-delivery rate of 5.89%.

These results illustrate why both late-delivery rates and late-order volumes are important for prioritization.

### Monthly variation

- March 2018 recorded a late-delivery rate of **21.36%** (1,496 of 7,003 eligible orders).
- June 2018 recorded **1.36%** (83 of 6,096 eligible orders).
- August 2018 recorded 10.39%.

These differences warrant further investigation into destination mix, seller mix, promised delivery windows, and data completeness.

### Delivery-stage analysis

| Average stage duration | Late orders | On-time orders |
|---|---:|---:|
| Approval to carrier handoff | 5.35 days | 2.63 days |
| Carrier handoff to customer delivery | 25.68 days | 7.89 days |
| Purchase to customer delivery | 31.52 days | 10.88 days |

The carrier-to-customer stage showed the largest average duration difference between late and on-time orders. This makes it a priority for further investigation, not proof that a particular carrier or other party caused the delays.

### Seller–state investigation

Four seller–state combinations were identified with late-delivery rates above their respective state baselines. Their observed rates ranged from 12.71% to 20.21%, compared with state baselines between 5.89% and 13.47%.

The stage-level comparisons showed different patterns: one flagged São Paulo combination had substantially longer average approval-to-handoff time, while flagged Rio de Janeiro and Rio Grande do Sul combinations showed particularly long post-handoff transit times among late orders.

These are exploratory findings based on relatively small segment samples and require validation.

## 6. Business Recommendations

1. Investigate geographic differences using late-delivery rates, order volumes, and transit-time distributions.
2. Examine approval-to-handoff processes for the flagged São Paulo seller–state combination.
3. Investigate tracking events, routes, and carrier service levels for the flagged Rio de Janeiro and Rio Grande do Sul combinations.
4. Compare sellers across similar destinations and order characteristics before recommending seller-specific interventions.
5. Monitor late-delivery rate, late-order volume, delay severity, stage durations, and missing timestamps together.

## 7. Project Structure

```text
DeliveryOps Intelligence/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── business_recommendations.md
│   └── reconnaissance/
├── scripts/
│   ├── inspect_data.py
│   ├── check_relationships.py
│   ├── investigate_reviews.py
│   ├── investigate_geolocation.py
│   ├── check_geolocation_grain.py
│   ├── run_order_delivery_base.py
│   ├── run_state_delivery_analysis.py
│   └── run_business_summary.py
├── sql/
│   ├── 01_order_delivery_base.sql
│   ├── 02_late_delivery_by_state.sql
│   ├── 03_late_delivery_by_month.sql
│   ├── 04_late_delivery_by_seller.sql
│   ├── 05_delivery_stage_analysis.sql
│   ├── 06_delivery_stage_by_state.sql
│   ├── 07_seller_state_delivery.sql
│   ├── 08_seller_vs_state_baseline.sql
│   ├── 09_flagged_seller_stage_analysis.sql
│   └── 10_flagged_handoff_analysis.sql
└── tests/
    └── test_data_quality.py
```

## 8. Run the Project Locally

### Prerequisites

- Python
- Git
- The Olist CSV files in `data/raw/`

### Install dependencies

Activate your virtual environment, then run:

```powershell
python -m pip install -r requirements.txt
```

### Generate the analytical dataset

```powershell
python scripts/run_order_delivery_base.py
```

This generates the processed order-delivery Parquet dataset used by the analysis and dashboard.

### Run automated tests

```powershell
python -m pytest tests -v
```

The current test suite contains six data-quality tests covering key uniqueness and order-item relationships.

### Launch the dashboard

```powershell
streamlit run app.py
```

Streamlit will provide a local URL for viewing the dashboard in your browser.

## 9. Limitations

- The analysis uses historical observational data and does not establish causality.
- Seller and state comparisons may be influenced by destination, route, product, and order characteristics.
- Some timestamps are missing or chronologically inconsistent.
- Seller–state samples are relatively small and should not be treated as definitive rankings.
- The current project does not quantify the financial impact of late deliveries or prove the effectiveness of proposed interventions.
- Results should be validated against additional operational information before implementation decisions are made.

## 10. Future Improvements

- Incorporate route-level and carrier-level information where available.
- Control for relevant order and destination characteristics in comparative analysis.
- Quantify the financial and customer impact of delays where suitable data is available.
- Add statistical uncertainty estimates to segment comparisons.
- Develop predictive models for late-delivery risk once an appropriate modeling objective and validation strategy are established.
- Deploy the dashboard for broader stakeholder access.

## 11. Project Status

The project includes a reproducible analytical dataset pipeline, SQL analyses, six passing automated data-quality tests, business recommendations, and an interactive Streamlit dashboard.

The findings are exploratory and intended to guide further investigation rather than establish operational causality.

**Author:** Add your name and portfolio links here.

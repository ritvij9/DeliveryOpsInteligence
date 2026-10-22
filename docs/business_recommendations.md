# DeliveryOps Intelligence — Business Recommendations

## 1. Executive summary

The initial analysis of the Olist historical e-commerce dataset shows substantial variation in late-delivery rates across purchase months, customer states, and sellers. These differences provide starting points for operational investigation, but they do not establish the causes of late delivery.

## 2. Key findings

### Geographic performance

- Maranhão (MA) recorded a late-delivery rate of 19.67%, with 141 late orders among 717 eligible orders.
- Rio de Janeiro (RJ) recorded 1,664 late orders, with a late-delivery rate of 13.47%.
- Rates and volumes provide different prioritization signals: a high rate indicates a greater proportion of late orders, while high volume indicates a larger number of affected orders.

### Monthly performance

- March 2018 recorded a late-delivery rate of 21.36% (1,496 of 7,003 eligible orders).
- June 2018 recorded 1.36% (83 of 6,096 eligible orders).
- August 2018 recorded 10.39%, despite having the shortest average actual transit time among the January–August months analyzed.

These results show that transit time and late-delivery rate are distinct metrics. The monthly differences require further investigation before operational causes can be assigned.

### Seller performance

- Seller `4a3ca9315b744ce9f8e9374361493884` recorded 195 late orders among 1,772 eligible orders, a rate of 11.00%.
- Seller `4869f7a5dfa277a7dca6462dcf3b52b2` recorded a rate of 11.57%, with 130 late orders among 1,124 eligible orders.

Seller results are descriptive and may be influenced by destination mix, product mix, order characteristics, and other factors.

## 3. Recommended actions

### Priority 1 — Investigate geographic delivery variation

Compare delivery performance across states and, where reliable data permits, more granular destinations.

- Examine late-delivery rate and late-order volume together.
- Compare actual transit times and estimated delivery windows.
- Investigate whether destination mix or other order characteristics explain observed differences.

### Priority 2 — Investigate high-volume sellers

Use seller-level results to identify candidates for further analysis rather than immediately penalizing sellers.

- Compare seller delivery performance across similar destinations and order types.
- Inspect order volumes, late-delivery rates, and delay severity.
- Validate results before recommending seller-specific interventions.

### Priority 3 — Monitor multiple delivery KPIs

Track the following measures together:

- Late-delivery rate
- Number of late orders
- Average actual transit time
- Average days late among late orders
- Eligible orders and missing delivery timestamps

This combination distinguishes frequency, volume, and severity of delivery delays.

### Priority 4 — Validate the monthly pattern

Investigate the substantial monthly differences before attributing them to operational changes.

- Compare destination and seller mix across months.
- Examine estimated delivery windows and actual transit-time distributions.
- Assess data completeness and chronology violations.
- Avoid interpreting incomplete recent purchase cohorts as comparable with mature cohorts.

## 4. Limitations

This analysis uses historical observational data. It does not establish causation, quantify the financial impact of delays, or demonstrate that any proposed intervention will improve performance.

The current analysis also does not control for all potential confounding factors. The recommendations are therefore investigation priorities, not proven operational solutions.

## 5. Next steps

1. Validate the monthly and seller-level findings.
2. Segment delivery performance by destination and seller.
3. Identify plausible operational drivers and quantify their business impact where the data permits.
4. Build a dashboard for monitoring delivery performance.
5. Present recommendations with explicit evidence, assumptions, and limitations.

# DeliveryOps Intelligence — Business Recommendations

## 1. Executive Summary

The initial analysis of the Olist historical e-commerce dataset shows substantial variation in late-delivery rates across purchase months, customer states, and sellers. Further investigation indicates that the time between carrier handoff and customer delivery is a major diagnostic lead, while some seller–state combinations also show unusually high late-delivery rates relative to their state baselines.

These findings identify priorities for operational investigation, but they do not establish the causes of late delivery. The recommendations below distinguish observed evidence from hypotheses requiring validation.

## 2. Key Findings

### 2.1 Geographic Performance

- Maranhão (MA) recorded a late-delivery rate of 19.67%, with 141 late orders among 717 eligible orders.
- Rio de Janeiro (RJ) recorded 1,664 late orders, with a late-delivery rate of 13.47%.
- São Paulo (SP) recorded 2,387 late orders, with a late-delivery rate of 5.89%.

Rates and volumes provide different prioritization signals: a high rate indicates a greater proportion of late orders, while high volume indicates a larger number of affected orders.

### 2.2 Monthly Performance

- March 2018 recorded a late-delivery rate of 21.36% (1,496 of 7,003 eligible orders).
- June 2018 recorded 1.36% (83 of 6,096 eligible orders).
- August 2018 recorded 10.39%, despite having the shortest average actual transit time among the January–August months analyzed.

These results show that transit time and late-delivery rate are distinct metrics. Monthly differences require further investigation before operational causes can be assigned. September and October contain too few orders with completed delivery timestamps to support comparable monthly late-rate conclusions.

### 2.3 Seller Performance

- Seller `4a3ca9315b744ce9f8e9374361493884` recorded 195 late orders among 1,772 eligible orders, a rate of 11.00%.
- Seller `4869f7a5dfa277a7dca6462dcf3b52b2` recorded a rate of 11.57%, with 130 late orders among 1,124 eligible orders.

Seller results are descriptive and may be influenced by destination mix, product mix, order characteristics, and other factors.

## 3. Delivery-Stage Investigation

### 3.1 Overall Stage Comparison

The initial stage-level analysis found substantial differences between late and on-time orders.

| Metric | Late orders | On-time orders |
|---|---:|---:|
| Orders included in the group | 7,827 | 88,649 |
| Average approval-to-carrier time | 5.35 days | 2.63 days |
| Average carrier-to-customer time | 25.68 days | 7.89 days |
| Average total purchase-to-delivery time | 31.52 days | 10.88 days |

The average carrier-to-customer stage was approximately 17.79 days longer for late orders. The approval-to-carrier stage was approximately 2.72 days longer.

**Interpretation:** The carrier-to-customer stage is the strongest initial diagnostic lead in the overall dataset. The approval-to-carrier stage may also contribute to observed differences.

These comparisons are observational. The stage metrics have different numbers of valid timestamps, and the analysis does not establish that a specific seller or carrier caused the delays.

## 4. Seller–State Investigation

### 4.1 Seller–State Combinations Above Their State Baselines

Four seller–state combinations were selected for investigation because their late-delivery rates were above the corresponding state baselines.

| Seller ID (short) | State | Eligible orders | Late orders | Late rate | State baseline | Difference |
|---|---|---:|---:|---:|---:|---:|
| `88460e8e` | SP | 118 | 15 | 12.71% | 5.89% | +6.82 percentage points |
| `7d13fca1` | RJ | 94 | 19 | 20.21% | 13.47% | +6.74 percentage points |
| `4869f7a5` | RJ | 201 | 40 | 19.90% | 13.47% | +6.43 percentage points |
| `4a3ca931` | RS | 91 | 12 | 13.19% | 7.15% | +6.04 percentage points |

These differences make the four combinations reasonable candidates for further investigation. Their sample sizes range from 91 to 201 orders, so the estimates should not be treated as definitive seller performance rankings.

### 4.2 Stage-Level Comparison Within Flagged Groups

| Seller ID (short) | State | Late-order average carrier-to-customer time | On-time average carrier-to-customer time | Seller–state average approval-to-carrier time | State approval-to-carrier baseline |
|---|---|---:|---:|---:|---:|
| `4869f7a5` | RJ | 32.73 days | 11.50 days | 2.47 days | 2.92 days |
| `7d13fca1` | RJ | 37.56 days | 9.49 days | 3.58 days | 2.92 days |
| `4a3ca931` | RS | 33.26 days | 14.21 days | 2.63 days | 2.73 days |
| `88460e8e` | SP | 13.05 days | 7.02 days | 7.64 days | 2.76 days |

**Interpretation:**

- **SP — seller `88460e8e`:** The average approval-to-carrier time was 7.64 days, compared with 2.76 days for the state baseline. This is a strong signal to investigate the pre-handoff process, alongside the post-handoff stage.
- **RJ — seller `7d13fca1`:** Approval-to-carrier time was moderately above the state baseline, while late orders averaged 37.56 days after carrier handoff. The post-handoff stage warrants particular attention.
- **RS — seller `4a3ca931`:** Approval-to-carrier time was close to the state baseline, while late orders averaged 33.26 days after handoff. The post-handoff stage is the stronger diagnostic lead.
- **RJ — seller `4869f7a5`:** Approval-to-carrier time was below the state baseline, while late orders averaged 32.73 days after handoff. This also makes post-handoff transit a priority for investigation.

These findings describe differences in observed stage durations. They do not establish whether the seller, carrier, route, destination, or another factor was responsible.

## 5. Recommended Operational Actions

### Priority 1 — Investigate Geographic Delivery Variation

Compare delivery performance across states and, where reliable data permits, more granular destinations.

- Examine late-delivery rate and late-order volume together.
- Compare actual transit times with estimated delivery windows.
- Investigate whether destination mix, route characteristics, or other order characteristics explain observed differences.
- Avoid assuming that a state's late-delivery rate reflects a single operational cause.

### Priority 2 — Investigate Delivery Stages

Use the stage-level findings to guide targeted investigation.

- Review approval-to-carrier processes for the flagged SP seller–state combination.
- Examine tracking events, routes, and carrier service levels for the flagged RJ and RS combinations.
- Compare promised delivery windows with actual transit times.
- Inspect missing timestamps and chronology violations before using stage metrics for operational accountability.

### Priority 3 — Investigate High-Volume Sellers

Use seller-level results to identify candidates for further analysis rather than immediately penalizing sellers.

- Compare seller performance across similar destinations and order types.
- Inspect eligible order volumes, late-delivery rates, and delay severity.
- Evaluate seller–state combinations alongside overall seller performance.
- Validate findings on larger samples before recommending seller-specific interventions.

### Priority 4 — Monitor Multiple Delivery KPIs

Track the following measures together:

- Late-delivery rate
- Number of late orders
- Average actual transit time
- Average days late among late orders
- Approval-to-carrier time
- Carrier-to-customer time
- Eligible order count
- Missing delivery timestamps

This combination distinguishes delay frequency, volume, severity, and stage-level duration.

### Priority 5 — Validate the Monthly Pattern

Investigate the substantial monthly differences before attributing them to operational changes.

- Compare destination and seller mix across months.
- Examine estimated delivery windows and actual transit-time distributions.
- Assess data completeness and chronology violations.
- Avoid interpreting incomplete recent purchase cohorts as comparable with mature cohorts.

## 6. Limitations

This analysis uses historical observational data. It does not establish causation, quantify the financial impact of delays, or demonstrate that any proposed intervention will improve performance.

The current analysis does not control for all potential confounding factors, including destination mix, route distance, product category, order characteristics, and promised delivery windows.

Stage-level averages may be affected by missing timestamps and are calculated from different numbers of eligible orders. Seller–state results are based on relatively small samples and should be treated as investigation signals rather than definitive rankings.

The recommendations are therefore investigation priorities, not proven operational solutions.

## 7. Next Steps

1. Validate the monthly, state, seller, and seller–state findings.
2. Investigate stage-level delays using tracking and route information where available.
3. Compare seller performance across similar destinations and order characteristics.
4. Quantify the business impact of delays where financial or customer-outcome data permits.
5. Build and maintain a dashboard for monitoring delivery performance.
6. Present recommendations with explicit evidence, assumptions, limitations, and validation criteria.

## 8. Overall Conclusion

The analysis identifies meaningful variation in delivery performance across states, months, and sellers. The strongest initial diagnostic lead is the carrier-to-customer stage, which has substantially longer average durations among late orders. The seller–state investigation further identifies four combinations whose late-delivery rates exceed their state baselines, with different stage-duration patterns.

The practical next step is targeted validation: investigate where delays occur, compare similar orders and routes, and establish whether the observed differences persist after accounting for relevant factors. Operational interventions should follow that validation rather than be based on descriptive rates alone.
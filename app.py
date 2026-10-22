
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="DeliveryOps Intelligence",
    page_icon="📦",
    layout="wide",
)

ROOT = Path(__file__).resolve().parent
PARQUET = ROOT / "data" / "processed" / "order_delivery_base.parquet"
RAW = ROOT / "data" / "raw"

st.title("DeliveryOps Intelligence")
st.caption("E-commerce delivery performance | Olist historical dataset")

if not PARQUET.exists():
    st.error("Processed dataset not found. Run the data pipeline first.")
    st.code("python scripts/run_order_delivery_base.py")
    st.stop()


@st.cache_data
def load_data():
    con = duckdb.connect()

    def safe_path(path):
        return str(path).replace("\\", "/").replace("'", "''")

    base = con.execute(
        f"SELECT * FROM read_parquet('{safe_path(PARQUET)}')"
    ).fetchdf()

    customers = con.execute(
        f"""
        SELECT customer_id, customer_state
        FROM read_csv_auto('{safe_path(RAW / "olist_customers_dataset.csv")}')
        """
    ).fetchdf()

    items = con.execute(
        f"""
        SELECT order_id, seller_id
        FROM read_csv_auto('{safe_path(RAW / "olist_order_items_dataset.csv")}')
        """
    ).fetchdf()

    con.close()
    return base, customers, items


base, customers, items = load_data()

base["purchase_ts"] = pd.to_datetime(base["purchase_ts"])
base["purchase_month"] = base["purchase_ts"].dt.to_period("M").astype(str)

eligible = base[base["has_complete_delivery_dates"]].copy()
eligible["is_late_delivery"] = (
    eligible["is_late_delivery"].fillna(False).astype(bool)
)
eligible["days_late_vs_estimate"] = pd.to_numeric(
    eligible["days_late_vs_estimate"], errors="coerce"
)

# Sidebar filters
st.sidebar.header("Filters")

months = sorted(eligible["purchase_month"].dropna().unique())
selected_months = st.sidebar.multiselect(
    "Purchase month",
    months,
    default=months,
)

states = sorted(customers["customer_state"].dropna().unique())
selected_states = st.sidebar.multiselect(
    "Customer state",
    states,
    default=states,
)

filtered = eligible[
    eligible["purchase_month"].isin(selected_months)
].copy()

filtered = filtered.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
)

filtered = filtered[
    filtered["customer_state"].isin(selected_states)
].copy()

if filtered.empty:
    st.warning("No eligible orders match these filters.")
    st.stop()

late = filtered[filtered["is_late_delivery"]]
late_rate = 100 * filtered["is_late_delivery"].mean()
avg_delay = late["days_late_vs_estimate"].mean()

# KPI cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Eligible orders", f"{len(filtered):,}")
c2.metric("Late orders", f"{int(filtered['is_late_delivery'].sum()):,}")
c3.metric("Late-delivery rate", f"{late_rate:.2f}%")
c4.metric(
    "Avg. days late",
    f"{avg_delay:.2f}" if pd.notna(avg_delay) else "N/A",
)

st.caption(
    "Eligible orders have both actual and estimated delivery timestamps. "
    "Results are descriptive and do not establish causation."
)

# Monthly analysis
st.subheader("Monthly delivery performance")

monthly = (
    filtered.groupby("purchase_month")
    .agg(
        eligible_orders=("order_id", "nunique"),
        late_orders=("is_late_delivery", "sum"),
        avg_transit_days=("purchase_to_delivery_days", "mean"),
    )
    .reset_index()
)

monthly["late_rate_pct"] = (
    100 * monthly["late_orders"] / monthly["eligible_orders"]
)

# Exclude tiny monthly cohorts from charts to prevent misleading spikes.
monthly_chart = monthly[monthly["eligible_orders"] >= 100].copy()

left, right = st.columns(2)

with left:
    st.markdown("**Late-delivery rate by month (100+ eligible orders)**")
    st.line_chart(
        monthly_chart.set_index("purchase_month")[["late_rate_pct"]]
    )

with right:
    st.markdown("**Average transit time by month (100+ eligible orders)**")
    st.bar_chart(
        monthly_chart.set_index("purchase_month")[["avg_transit_days"]]
    )

st.dataframe(
    monthly.round(2),
    use_container_width=True,
    hide_index=True,
)

# State analysis
st.subheader("Delivery performance by customer state")

state_summary = (
    filtered.groupby("customer_state")
    .agg(
        eligible_orders=("order_id", "nunique"),
        late_orders=("is_late_delivery", "sum"),
        avg_transit_days=("purchase_to_delivery_days", "mean"),
    )
    .reset_index()
)

state_summary["late_rate_pct"] = (
    100 * state_summary["late_orders"] / state_summary["eligible_orders"]
)

min_state_orders = st.slider(
    "Minimum eligible orders per state",
    min_value=1,
    max_value=1000,
    value=100,
    step=25,
)

state_view = state_summary[
    state_summary["eligible_orders"] >= min_state_orders
].sort_values("late_rate_pct", ascending=False)

st.bar_chart(
    state_view.set_index("customer_state")[["late_rate_pct"]]
)

st.dataframe(
    state_view.round(2),
    use_container_width=True,
    hide_index=True,
)

# Seller analysis
st.subheader("Seller delivery performance")

# Count each seller-order combination once.
seller_orders = items.merge(
    filtered[
        [
            "order_id",
            "has_complete_delivery_dates",
            "is_late_delivery",
            "purchase_to_delivery_days",
            "days_late_vs_estimate",
        ]
    ],
    on="order_id",
    how="inner",
)

seller_orders = seller_orders.drop_duplicates(["seller_id", "order_id"])

# The filtered base already contains eligible orders only.
seller_summary = (
    seller_orders.groupby("seller_id")
    .agg(
        eligible_orders=("order_id", "nunique"),
        late_orders=("is_late_delivery", "sum"),
        avg_transit_days=("purchase_to_delivery_days", "mean"),
        avg_days_late=(
            "days_late_vs_estimate",
            lambda values: values[values > 0].mean(),
        ),
    )
    .reset_index()
)

seller_summary["late_rate_pct"] = (
    100 * seller_summary["late_orders"] / seller_summary["eligible_orders"]
)

min_seller_orders = st.slider(
    "Minimum eligible orders per seller",
    min_value=10,
    max_value=500,
    value=100,
    step=10,
)

seller_view = seller_summary[
    seller_summary["eligible_orders"] >= min_seller_orders
].copy()

if seller_view.empty:
    st.info("No sellers meet the selected minimum order threshold.")
else:
    rate_tab, volume_tab = st.tabs(
        ["Highest late-delivery rate", "Most late orders"]
    )

    with rate_tab:
        rate_view = seller_view.sort_values(
            "late_rate_pct", ascending=False
        ).head(15).copy()

        rate_view["seller_label"] = rate_view["seller_id"].str.slice(0, 8)

        st.bar_chart(
            rate_view.set_index("seller_label")[["late_rate_pct"]]
        )
        st.dataframe(
            rate_view.drop(columns=["seller_label"]).round(2),
            use_container_width=True,
            hide_index=True,
        )

    with volume_tab:
        volume_view = seller_view.sort_values(
            "late_orders", ascending=False
        ).head(15).copy()

        volume_view["seller_label"] = volume_view["seller_id"].str.slice(0, 8)

        st.bar_chart(
            volume_view.set_index("seller_label")[["late_orders"]]
        )
        st.dataframe(
            volume_view.drop(columns=["seller_label"]).round(2),
            use_container_width=True,
            hide_index=True,
        )

# Export
st.subheader("Export")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download filtered eligible orders (CSV)",
    data=csv,
    file_name="deliveryops_filtered_orders.csv",
    mime="text/csv",
)

st.caption(
    "DeliveryOps Intelligence | Exploratory analysis | Olist public dataset"
)

import duckdb

con = duckdb.connect()

state_query = open(
    "sql/02_late_delivery_by_state.sql", encoding="utf-8"
).read()

seller_query = open(
    "sql/04_late_delivery_by_seller.sql", encoding="utf-8"
).read()

monthly_query = open(
    "sql/03_late_delivery_by_month.sql", encoding="utf-8"
).read()

state_df = con.execute(state_query).fetchdf()
seller_df = con.execute(seller_query).fetchdf()
monthly_df = con.execute(monthly_query).fetchdf()

print("\n=== MONTHLY DELIVERY PERFORMANCE ===")
print(monthly_df.to_string(index=False))

print("\n=== TOP 10 STATES BY LATE-DELIVERY RATE ===")
print(
    state_df.sort_values(
        "late_delivery_rate_pct", ascending=False
    ).head(10).to_string(index=False)
)

print("\n=== TOP 10 SELLERS BY LATE-DELIVERY RATE ===")
print(
    seller_df.sort_values(
        "late_delivery_rate_pct", ascending=False
    ).head(10).to_string(index=False)
)

print("\n=== TOP 10 SELLERS BY LATE-ORDER VOLUME ===")
print(
    seller_df.sort_values(
        "late_orders", ascending=False
    ).head(10).to_string(index=False)
)

con.close()
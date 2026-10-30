import streamlit as st
from seed import generate_orders
from analysis import database,kpis,breakdown,monthly,audit
st.set_page_config(page_title="Customer Operations Insights",layout="wide")
st.title("Customer Operations Insights")
st.caption("SQL-backed ecommerce dashboard — entirely fictional data generated for this demo")
raw=generate_orders()
with st.sidebar:
    region=st.multiselect("Regions",sorted(raw.region.unique()),default=sorted(raw.region.unique()))
    channels=st.multiselect("Channels",sorted(raw.channel.unique()),default=sorted(raw.channel.unique()))
    categories=st.multiselect("Categories",sorted(raw.category.unique()),default=sorted(raw.category.unique()))
filtered=raw[raw.region.isin(region)&raw.channel.isin(channels)&raw.category.isin(categories)]
if filtered.empty: st.warning("No orders match the filters");st.stop()
con=database(filtered)
m=kpis(con)
a,b,c,d=st.columns(4)
a.metric("Orders",f"{int(m['orders']):,}")
b.metric("Net revenue (CAD)",f"${m['net_revenue_cad']:,.0f}")
c.metric("Late deliveries",f"{m['late_pct']:.1f}%")
d.metric("Refunded orders",f"{m['refund_pct']:.1f}%")
st.subheader("Monthly performance")
st.line_chart(monthly(con).set_index("month"))
field=st.selectbox("Compare by",["channel","region","category"])
segments=breakdown(con,field)
st.subheader("Segment comparison")
st.dataframe(segments,hide_index=True,use_container_width=True)
st.bar_chart(segments.set_index("segment")["late_pct"])
st.subheader("Exploratory operational insights")
worst=segments.sort_values("late_pct",ascending=False).iloc[0]
st.write(f"Investigate delivery performance for {worst['segment']} (simulated late delivery rate: {worst['late_pct']}%). Validate with genuine operational data before changing policy.")
st.subheader("Data quality")
st.json(audit(filtered))
st.download_button("Export filtered data",filtered.to_csv(index=False),"orders.csv","text/csv")
con.close()

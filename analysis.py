import sqlite3
import pandas as pd
ALLOWED={"channel","region","category"}
def database(df):
    con=sqlite3.connect(":memory:")
    df.to_sql("orders",con,index=False)
    return con
def kpis(con):
    return pd.read_sql_query("""SELECT COUNT(*) orders,
    ROUND(SUM(subtotal_cad+shipping_cad-discount_cad-refund_cad),2) net_revenue_cad,
    ROUND(100.0*AVG(CASE WHEN actual_days>promised_days THEN 1.0 ELSE 0 END),1) late_pct,
    ROUND(100.0*AVG(CASE WHEN refund_cad>0 THEN 1.0 ELSE 0 END),1) refund_pct,
    ROUND(100.0*AVG(support_case),1) support_pct FROM orders""",con).iloc[0]
def breakdown(con,field):
    if field not in ALLOWED: raise ValueError("Invalid group-by field")
    return pd.read_sql_query(f"""SELECT {field} segment,COUNT(*) orders,
    ROUND(SUM(subtotal_cad+shipping_cad-discount_cad-refund_cad),2) net_revenue_cad,
    ROUND(100.0*AVG(CASE WHEN actual_days>promised_days THEN 1.0 ELSE 0 END),1) late_pct,
    ROUND(100.0*AVG(CASE WHEN refund_cad>0 THEN 1.0 ELSE 0 END),1) refund_pct
    FROM orders GROUP BY {field} ORDER BY net_revenue_cad DESC""",con)
def monthly(con):
    return pd.read_sql_query("""SELECT substr(order_date,1,7) month,
    ROUND(SUM(subtotal_cad+shipping_cad-discount_cad-refund_cad),2) net_revenue_cad
    FROM orders GROUP BY substr(order_date,1,7) ORDER BY month""",con)
def audit(df):
    return dict(rows=len(df),duplicate_order_ids=int(df.order_id.duplicated().sum()),missing_values=int(df.isna().sum().sum()),negative_amounts=int((df[["subtotal_cad","shipping_cad","discount_cad","refund_cad"]]<0).sum().sum()))

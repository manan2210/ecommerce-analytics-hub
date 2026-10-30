from seed import generate_orders
from analysis import database,kpis,breakdown,audit
def test_reproducible(): assert generate_orders(10).equals(generate_orders(10))
def test_metrics():
    df=generate_orders(100)
    con=database(df)
    assert kpis(con)["orders"]==100
    assert len(breakdown(con,"channel"))>0
    assert audit(df)["duplicate_order_ids"]==0

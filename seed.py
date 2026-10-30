import random
from datetime import date,timedelta
import pandas as pd
def generate_orders(n=1800,seed=42):
    rng=random.Random(seed)
    rows=[]
    for i in range(n):
        channel=rng.choices(["Website","Mobile","Marketplace"],[50,35,15])[0]
        region=rng.choice(["Ontario","Quebec","Alberta","British Columbia","Atlantic Canada"])
        promised=4 if region=="Atlantic Canada" else 3
        late=rng.random()<(.32 if channel=="Marketplace" else .15)
        subtotal=round(rng.uniform(25,300),2)
        refund=round(subtotal*rng.choice([.25,.5,1]),2) if rng.random()<(.11 if late else .055) else 0.0
        rows.append(dict(order_id=f"ORD-{i+1:05d}",order_date=str(date(2026,1,1)+timedelta(days=rng.randrange(181))),channel=channel,region=region,category=rng.choice(["Home","Clothing","Electronics","Beauty"]),subtotal_cad=subtotal,shipping_cad=rng.choice([0,5.99,9.99]),discount_cad=round(subtotal*rng.choice([0,0,.1]),2),refund_cad=refund,promised_days=promised,actual_days=promised+rng.choice([1,2,3]) if late else rng.choice([1,2,promised]),support_case=int(rng.random()<(.27 if late else .08))))
    return pd.DataFrame(rows)
if __name__=="__main__":
    generate_orders().to_csv("synthetic_orders.csv",index=False)

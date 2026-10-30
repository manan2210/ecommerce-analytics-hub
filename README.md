# Customer Operations Insights

A **synthetic-data** SQL and Python ecommerce operations dashboard demonstrating KPIs, segmentation, refunds, shipping delays, and operational recommendations. This is a portfolio prototype, **not actual company data or real business results**.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard generates a reproducible fictional dataset (seed 42). It builds a temporary SQLite database and calculates metrics with SQL. No real customer or employer records are used.

## Metrics

- **Net revenue:** subtotal + shipping - discount - refund, not profit
- **Late delivery rate:** share of orders arriving after the promised date
- **Refunded orders:** share of orders with a positive refund
- **Support cases:** share of orders flagged for support

Channel patterns are descriptive and deliberately simulated, not causal conclusions. Future improvements could add source-quality checks, forecasting, and validated real-data integrations.

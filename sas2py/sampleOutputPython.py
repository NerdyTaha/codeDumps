import pandas as pd

# DATA step
customer_summary = pd.read_csv('raw/customers.csv')  # or from DB
customer_summary = customer_summary[customer_summary['balance'] > 1000]
customer_summary['risk_score'] = customer_summary['balance'] / 1000
customer_summary['risk_level'] = customer_summary['risk_score'].apply(
    lambda x: 'HIGH' if x > 5 else 'LOW'
)

# PROC MEANS
summary_stats = customer_summary.groupby('risk_level')['risk_score'].agg(['mean', 'std'])
print(summary_stats)

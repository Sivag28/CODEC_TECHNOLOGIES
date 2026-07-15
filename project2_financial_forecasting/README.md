# Financial Forecasting

Time-series forecasting of future monthly revenue using 4 years of historical order data from the "Sample Superstore" retail dataset, built with Holt-Winters Exponential Smoothing.

## Project Structure
```
project2_financial_forecasting/
├── data/
│   └── superstore_cleaned.csv        # Cleaned dataset (9,994 rows)
├── scripts/
│   └── financial_forecasting.py      # Decomposition, validation, forecasting
├── charts/                           # Generated PNG charts + summary.json
└── reports/
    └── Financial_Forecasting_Report.docx
```

## Method
- **Model:** Holt-Winters Triple Exponential Smoothing (additive trend + additive seasonality, 12-month cycle)
- **Validation:** trained on the first 42 months, tested against the final 6 held-out actual months
- **Result:** 15.6% Mean Absolute Percentage Error (MAPE) on validation

## Key Findings
- Historical average monthly revenue: **$47.9K**
- 2018 closed with **+20.4% YoY growth**
- Forecast for Jan–Jun 2019: **$354.4K total**, with an expected seasonal dip in Jan–Feb followed by a March rebound
- Seasonal decomposition confirms a consistent Q4 peak / Q1 trough pattern with a steady underlying upward trend

## How to Reproduce
```bash
pip install pandas numpy matplotlib statsmodels scikit-learn
python scripts/financial_forecasting.py
```

## Tools Used
Python (Statsmodels, Scikit-learn, Pandas, Matplotlib), Microsoft Word (report)

## Data Source
[Sample Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) (Kaggle)

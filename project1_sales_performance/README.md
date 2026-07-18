# Sales Performance Analysis

Analysis of 4 years (2015–2018) of historical order-level data from the classic "Sample Superstore" retail dataset, identifying sales trends, seasonal patterns, and top-performing products, categories, and regions.

## Project Structure
```
project1_sales_performance/
├── data/
│   └── superstore_cleaned.csv        # Cleaned dataset (9,994 rows)
├── scripts/
│   ├── sales_performance_analysis.py # EDA + static chart generation
│   └── build_dashboard.py            # Interactive Plotly dashboard builder
├── charts/                           # Generated PNG charts + summary.json
├── dashboard/
│   └── sales_dashboard.pbix          # Open in PowerBI — fully interactive
└── reports/
    └── Sales_Performance_Analysis_Report.docx
```

## Key Findings
- **Total Sales:** $2.30M | **Total Profit:** $286.4K | **Margin:** 12.5% | **Orders:** 5,009
- Revenue grew **29.5%** in 2017 and **20.4%** in 2018 after a slight dip in 2016.
- **November** is the strongest sales month every year; **February** is the weakest — a clear seasonal pattern for inventory/staffing planning.
- **Technology** is the top-selling category; **Furniture** has the weakest profit margin due to heavy discounting.
- The **West** region leads in both sales and profit.
- Orders discounted **30%+** are unprofitable **96.8%** of the time.

## How to Reproduce
```bash
pip install pandas matplotlib plotly
python scripts/sales_performance_analysis.py   # generates charts + summary.json
python scripts/build_dashboard.py              # generates dashboard/sales_dashboard.html
```

## Tools Used
Python (Pandas, Matplotlib, Plotly), Microsoft Word (report)

## Data Source
[Sample Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) (Kaggle)

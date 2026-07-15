# CODEC_TECHNOLOGIES

This repository contains two end-to-end data analytics and business intelligence projects developed using the **Sample Superstore** retail dataset. The projects demonstrate data analysis, visualization, dashboard development, and time-series forecasting using Python and Power BI.

---

## Repository Structure

```
CODEC_TECHNOLOGIES/
│
├── project1_sales_performance/
│   ├── data/
│   ├── scripts/
│   ├── charts/
│   ├── dashboard/
│   ├── reports/
│   └── README.md
│
├── project2_financial_forecasting/
│   ├── data/
│   ├── scripts/
│   ├── charts/
│   ├── dashboard/
│   ├── reports/
│   └── README.md
│
└── README.md
```

---

# Project 1 – Sales Performance Analysis

### Overview

Analyzed four years (2015–2018) of historical order-level data from the Sample Superstore retail dataset to identify sales trends, seasonal patterns, customer purchasing behavior, and business performance across products, categories, and regions.

### Objectives

- Analyze historical sales performance
- Identify top-performing products and categories
- Compare regional sales and profit
- Detect seasonal sales trends
- Evaluate the impact of discounts on profitability
- Build an interactive Power BI dashboard

### Key Findings

- **Total Sales:** $2.30M
- **Total Profit:** $286.4K
- **Profit Margin:** 12.5%
- **Orders:** 5,009
- Revenue increased by **29.5%** in 2017 and **20.4%** in 2018.
- November consistently recorded the highest sales, while February showed the lowest.
- Technology generated the highest sales.
- The West region achieved the highest sales and profit.
- Orders with discounts above 30% were unprofitable approximately **96.8%** of the time.

### Technologies Used

- Python
- Pandas
- Matplotlib
- Plotly
- Power BI
- Microsoft Word

---

# Project 2 – Financial Forecasting

### Overview

Developed a time-series forecasting model to predict future monthly revenue using four years of historical retail sales data. Forecasting was performed using the Holt-Winters Triple Exponential Smoothing algorithm.

### Objectives

- Analyze historical monthly revenue
- Perform seasonal decomposition
- Build and validate a forecasting model
- Predict future monthly sales
- Visualize forecast trends using Power BI

### Forecasting Method

- Holt-Winters Triple Exponential Smoothing
- Additive Trend
- Additive Seasonality
- 12-Month Seasonal Cycle

### Model Validation

- Training Data: First 42 months
- Testing Data: Last 6 months
- Validation Metric: Mean Absolute Percentage Error (MAPE)
- **Validation Accuracy:** 15.6% MAPE

### Key Findings

- Average Monthly Revenue: **$47.9K**
- 2018 recorded **20.4%** year-over-year growth.
- Forecasted revenue for **January–June 2019:** **$354.4K**
- Seasonal analysis confirmed strong Q4 sales and weaker Q1 performance.
- Long-term revenue trend remained consistently upward.

### Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Statsmodels
- Scikit-learn
- Power BI
- Microsoft Word

---

# Dataset

Both projects use the **Sample Superstore** retail dataset containing approximately **9,994 cleaned order records** spanning **2015–2018**.

---

# Skills Demonstrated

- Data Cleaning
- Exploratory Data Analysis (EDA)
- Data Visualization
- Business Intelligence
- Dashboard Development
- Time-Series Forecasting
- Model Validation
- Business Insights
- Python Programming
- Power BI

---

# Author

**SIVASANKARI G**

B.Tech Information Technology  
National Engineering College

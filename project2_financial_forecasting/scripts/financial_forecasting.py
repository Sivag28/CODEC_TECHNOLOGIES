"""
Financial Forecasting — Sample Superstore Dataset
Uses Holt-Winters Exponential Smoothing (trend + seasonality) to forecast
future monthly revenue, validated against a held-out test period.
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import json

CHART_DIR = '/home/claude/project2_financial_forecasting/charts'

df = pd.read_csv('/home/claude/project2_financial_forecasting/data/superstore_cleaned.csv', parse_dates=['Order Date'])

monthly = df.set_index('Order Date').resample('MS').agg(Sales=('Sales','sum'), Profit=('Profit','sum'))
sales_series = monthly['Sales']

def fmt_k(x, pos):
    return f'${x/1000:,.0f}K'

# ---------- 1. Seasonal decomposition ----------
decomp = seasonal_decompose(sales_series, model='additive', period=12)
fig, axes = plt.subplots(4, 1, figsize=(11, 9), sharex=True)
axes[0].plot(decomp.observed, color='#2563eb'); axes[0].set_ylabel('Observed')
axes[1].plot(decomp.trend, color='#16a34a'); axes[1].set_ylabel('Trend')
axes[2].plot(decomp.seasonal, color='#f59e0b'); axes[2].set_ylabel('Seasonal')
axes[3].plot(decomp.resid, color='#dc2626', marker='o', linestyle='None', markersize=3); axes[3].set_ylabel('Residual')
for ax in axes:
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
fig.suptitle('Monthly Revenue — Seasonal Decomposition', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/01_decomposition.png', dpi=150)
plt.close()

# ---------- 2. Train/test split & model validation ----------
train = sales_series.iloc[:-6]
test = sales_series.iloc[-6:]

model_val = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=12).fit()
val_forecast = model_val.forecast(6)

mae = mean_absolute_error(test, val_forecast)
mape = mean_absolute_percentage_error(test, val_forecast)

plt.figure(figsize=(11,5))
plt.plot(train.index, train.values, label='Training Data', color='#2563eb')
plt.plot(test.index, test.values, label='Actual (Held-out)', color='#16a34a', marker='o')
plt.plot(test.index, val_forecast.values, label='Forecast (Validation)', color='#dc2626', linestyle='--', marker='x')
plt.title(f'Model Validation — MAPE: {mape:.1%}', fontsize=13, fontweight='bold')
plt.ylabel('Sales ($)')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
plt.legend()
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/02_model_validation.png', dpi=150)
plt.close()

# ---------- 3. Final forecast (next 6 months), trained on full history ----------
final_model = ExponentialSmoothing(sales_series, trend='add', seasonal='add', seasonal_periods=12).fit()
future_forecast = final_model.forecast(6)
conf_range = 1.96 * np.std(final_model.resid)

plt.figure(figsize=(11,5))
plt.plot(sales_series.index, sales_series.values, label='Historical Revenue', color='#2563eb')
plt.plot(future_forecast.index, future_forecast.values, label='Forecast (Next 6 Months)', color='#dc2626', linestyle='--', marker='o')
plt.fill_between(future_forecast.index, future_forecast.values - conf_range, future_forecast.values + conf_range, color='#dc2626', alpha=0.15, label='Approx. 95% Interval')
plt.title('Revenue Forecast — Next 6 Months', fontsize=13, fontweight='bold')
plt.ylabel('Sales ($)')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
plt.legend()
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/03_future_forecast.png', dpi=150)
plt.close()

# ---------- Summary ----------
summary = {
    'validation_mae': float(mae),
    'validation_mape': float(mape),
    'historical_avg_monthly_sales': float(sales_series.mean()),
    'last_actual_month': str(sales_series.index[-1].date()),
    'last_actual_value': float(sales_series.iloc[-1]),
    'forecast_months': [str(d.date()) for d in future_forecast.index],
    'forecast_values': [round(float(v),2) for v in future_forecast.values],
    'forecast_total_6mo': float(future_forecast.sum()),
    'yoy_2018_growth': float(monthly['Sales'].resample('YE').sum().pct_change().iloc[-1]),
}
with open(f'{CHART_DIR}/summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))

# ---------- 4. Power BI export tables ----------
POWERBI_DIR = '/home/claude/project2_financial_forecasting/powerbi'
import os
os.makedirs(POWERBI_DIR, exist_ok=True)

# 4a. Actual + Forecast + confidence band (for the trend chart)
rows = []
for d, v in sales_series.items():
    rows.append({'Date': d.date(), 'Type': 'Actual', 'Sales': round(v, 2),
                 'ForecastSales': '', 'LowerCI': '', 'UpperCI': ''})
for d, v in future_forecast.items():
    rows.append({'Date': d.date(), 'Type': 'Forecast', 'Sales': '',
                 'ForecastSales': round(v, 2),
                 'LowerCI': round(v - conf_range, 2), 'UpperCI': round(v + conf_range, 2)})
pd.DataFrame(rows).to_csv(f'{POWERBI_DIR}/forecast_table_full.csv', index=False)

# 4b. Validation comparison (actual vs held-out validation forecast, for the accuracy chart)
val_rows = []
for d, a, f_ in zip(test.index, test.values, val_forecast.values):
    val_rows.append({'Date': d.date(), 'ActualSales': round(a, 2), 'ValidationForecast': round(f_, 2),
                      'AbsError': round(abs(a - f_), 2), 'PctError': round(abs(a - f_) / a, 4)})
pd.DataFrame(val_rows).to_csv(f'{POWERBI_DIR}/validation_table.csv', index=False)

print(f"\nPower BI CSVs written to {POWERBI_DIR}/")

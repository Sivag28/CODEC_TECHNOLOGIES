"""
Sales Performance Analysis — Sample Superstore Dataset
Generates key charts: monthly trend, seasonality, top products/categories,
regional performance, discount-vs-profit relationship.
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.rcParams['font.family'] = 'DejaVu Sans'
CHART_DIR = '/home/claude/project1_sales_performance/charts'

df = pd.read_csv('/home/claude/project1_sales_performance/data/superstore_cleaned.csv', parse_dates=['Order Date'])

def fmt_k(x, pos):
    return f'${x/1000:,.0f}K'

# ---------- 1. Monthly Sales & Profit Trend ----------
monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
monthly['Order Date'] = monthly['Order Date'].dt.to_timestamp()

fig, ax1 = plt.subplots(figsize=(11,5))
ax1.plot(monthly['Order Date'], monthly['Sales'], color='#2563eb', linewidth=2, label='Sales')
ax1.set_ylabel('Sales ($)', color='#2563eb')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
ax2 = ax1.twinx()
ax2.plot(monthly['Order Date'], monthly['Profit'], color='#16a34a', linewidth=2, linestyle='--', label='Profit')
ax2.set_ylabel('Profit ($)', color='#16a34a')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
plt.title('Monthly Sales & Profit Trend (2015–2018)', fontsize=13, fontweight='bold')
fig.tight_layout()
plt.savefig(f'{CHART_DIR}/01_monthly_trend.png', dpi=150)
plt.close()

# ---------- 2. Seasonality: Avg sales by calendar month ----------
df['Month Name'] = df['Order Date'].dt.strftime('%b')
month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
seasonal = df.groupby('Month Name')['Sales'].sum().reindex(month_order)

plt.figure(figsize=(10,5))
bars = plt.bar(seasonal.index, seasonal.values, color='#f59e0b')
plt.title('Total Sales by Calendar Month (Seasonality, 2015–2018 combined)', fontsize=13, fontweight='bold')
plt.ylabel('Total Sales ($)')
plt.gca().yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
peak_idx = seasonal.values.argmax()
bars[peak_idx].set_color('#dc2626')
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/02_seasonality.png', dpi=150)
plt.close()

# ---------- 3. Top 10 Products by Sales ----------
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.barh(top_products.index[::-1], top_products.values[::-1], color='#7c3aed')
plt.title('Top 10 Products by Total Sales', fontsize=13, fontweight='bold')
plt.xlabel('Total Sales ($)')
plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/03_top_products.png', dpi=150)
plt.close()

# ---------- 4. Sales & Profit by Category / Sub-Category ----------
cat = df.groupby('Category').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).sort_values('Sales', ascending=False)
fig, ax = plt.subplots(figsize=(9,5))
x = range(len(cat))
w = 0.35
ax.bar([i - w/2 for i in x], cat['Sales'], width=w, label='Sales', color='#2563eb')
ax.bar([i + w/2 for i in x], cat['Profit'], width=w, label='Profit', color='#16a34a')
ax.set_xticks(list(x))
ax.set_xticklabels(cat.index)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
ax.set_title('Sales & Profit by Category', fontsize=13, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/04_category_performance.png', dpi=150)
plt.close()

# ---------- 5. Regional performance ----------
region = df.groupby('Region').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).sort_values('Sales', ascending=False)
fig, ax = plt.subplots(figsize=(9,5))
x = range(len(region))
ax.bar([i - w/2 for i in x], region['Sales'], width=w, label='Sales', color='#2563eb')
ax.bar([i + w/2 for i in x], region['Profit'], width=w, label='Profit', color='#16a34a')
ax.set_xticks(list(x))
ax.set_xticklabels(region.index)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
ax.set_title('Sales & Profit by Region', fontsize=13, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/05_region_performance.png', dpi=150)
plt.close()

# ---------- 6. Discount vs Profit Margin ----------
plt.figure(figsize=(9,5.5))
plt.scatter(df['Discount'], df['Profit Margin'], alpha=0.25, s=15, color='#dc2626')
plt.axhline(0, color='black', linewidth=0.8)
plt.title('Discount vs Profit Margin per Order', fontsize=13, fontweight='bold')
plt.xlabel('Discount Rate')
plt.ylabel('Profit Margin')
plt.tight_layout()
plt.savefig(f'{CHART_DIR}/06_discount_vs_margin.png', dpi=150)
plt.close()

# ---------- Text summary for the report ----------
summary = {
    'total_sales': df['Sales'].sum(),
    'total_profit': df['Profit'].sum(),
    'overall_margin': df['Profit'].sum() / df['Sales'].sum(),
    'total_orders': df['Order ID'].nunique(),
    'best_month': seasonal.idxmax(),
    'best_month_sales': seasonal.max(),
    'worst_month': seasonal.idxmin(),
    'top_product': top_products.index[0],
    'top_product_sales': top_products.iloc[0],
    'best_category': cat['Sales'].idxmax(),
    'best_region': region['Sales'].idxmax(),
    'worst_profit_category': cat['Profit'].idxmin(),
    'high_discount_loss_share': (df[df['Discount'] >= 0.3]['Profit'] < 0).mean(),
    'yoy_growth': {str(k.year): v for k, v in monthly.set_index('Order Date')['Sales'].resample('YE').sum().pct_change().dropna().to_dict().items()},
}
import json
with open('/home/claude/project1_sales_performance/charts/summary.json', 'w') as f:
    json.dump(summary, f, indent=2, default=str)

print(json.dumps(summary, indent=2, default=str))

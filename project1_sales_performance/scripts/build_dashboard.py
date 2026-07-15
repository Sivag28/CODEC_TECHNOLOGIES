"""
Builds a single self-contained interactive HTML dashboard for the
Sales Performance Analysis project using Plotly.
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

df = pd.read_csv('/home/claude/project1_sales_performance/data/superstore_cleaned.csv', parse_dates=['Order Date'])

month_order = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
df['Month Name'] = df['Order Date'].dt.strftime('%b')

monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
monthly['Order Date'] = monthly['Order Date'].dt.to_timestamp()

seasonal = df.groupby('Month Name')['Sales'].sum().reindex(month_order)
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
cat = df.groupby('Category').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).sort_values('Sales', ascending=False)
region = df.groupby('Region').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).sort_values('Sales', ascending=False)
subcat = df.groupby(['Category','Sub-Category'])['Sales'].sum().reset_index().sort_values('Sales', ascending=False)

COLORS = dict(sales='#2563eb', profit='#16a34a', accent='#f59e0b', purple='#7c3aed', red='#dc2626')

fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        "Monthly Sales & Profit Trend", "Sales by Calendar Month (Seasonality)",
        "Top 10 Products by Sales", "Sales & Profit by Category",
        "Sales & Profit by Region", "Sub-Category Sales Breakdown"
    ),
    specs=[[{"secondary_y": True}, {}], [{}, {}], [{}, {}]],
    vertical_spacing=0.10, horizontal_spacing=0.09
)

# 1. Monthly trend (dual axis)
fig.add_trace(go.Scatter(x=monthly['Order Date'], y=monthly['Sales'], name='Sales', line=dict(color=COLORS['sales'], width=3)), row=1, col=1, secondary_y=False)
fig.add_trace(go.Scatter(x=monthly['Order Date'], y=monthly['Profit'], name='Profit', line=dict(color=COLORS['profit'], width=2, dash='dash')), row=1, col=1, secondary_y=True)

# 2. Seasonality
colors_season = [COLORS['red'] if v == seasonal.max() else COLORS['accent'] for v in seasonal.values]
fig.add_trace(go.Bar(x=seasonal.index, y=seasonal.values, name='Monthly Sales', marker_color=colors_season, showlegend=False), row=1, col=2)

# 3. Top products
fig.add_trace(go.Bar(x=top_products.values[::-1], y=top_products.index[::-1], orientation='h', name='Top Products', marker_color=COLORS['purple'], showlegend=False), row=2, col=1)

# 4. Category
fig.add_trace(go.Bar(x=cat.index, y=cat['Sales'], name='Sales', marker_color=COLORS['sales'], showlegend=False), row=2, col=2)
fig.add_trace(go.Bar(x=cat.index, y=cat['Profit'], name='Profit', marker_color=COLORS['profit'], showlegend=False), row=2, col=2)

# 5. Region
fig.add_trace(go.Bar(x=region.index, y=region['Sales'], name='Sales', marker_color=COLORS['sales'], showlegend=False), row=3, col=1)
fig.add_trace(go.Bar(x=region.index, y=region['Profit'], name='Profit', marker_color=COLORS['profit'], showlegend=False), row=3, col=1)

# 6. Sub-category treemap-ish (bar, top 10)
top_sub = subcat.head(10)
fig.add_trace(go.Bar(x=top_sub['Sub-Category'], y=top_sub['Sales'], name='Sub-Category Sales', marker_color=COLORS['accent'], showlegend=False), row=3, col=2)

fig.update_layout(
    title=dict(text="Sales Performance Dashboard — Sample Superstore (2015–2018)", font=dict(size=22)),
    height=1250, width=1300,
    barmode='group',
    template='plotly_white',
    legend=dict(orientation='h', yanchor='bottom', y=1.06, xanchor='center', x=0.5),
    margin=dict(t=110)
)
fig.update_yaxes(title_text="Sales ($)", row=1, col=1, secondary_y=False)
fig.update_yaxes(title_text="Profit ($)", row=1, col=1, secondary_y=True)

# KPI header numbers
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
margin = total_profit/total_sales
orders = df['Order ID'].nunique()

kpi_html = f"""
<div style="display:flex; gap:20px; justify-content:center; font-family: 'Segoe UI', Arial, sans-serif; margin: 20px 0 0 0;">
  <div style="background:#eff6ff; border-radius:12px; padding:18px 28px; text-align:center; min-width:180px;">
    <div style="color:#2563eb; font-size:26px; font-weight:700;">${total_sales:,.0f}</div>
    <div style="color:#475569; font-size:13px;">Total Sales</div>
  </div>
  <div style="background:#f0fdf4; border-radius:12px; padding:18px 28px; text-align:center; min-width:180px;">
    <div style="color:#16a34a; font-size:26px; font-weight:700;">${total_profit:,.0f}</div>
    <div style="color:#475569; font-size:13px;">Total Profit</div>
  </div>
  <div style="background:#fffbeb; border-radius:12px; padding:18px 28px; text-align:center; min-width:180px;">
    <div style="color:#d97706; font-size:26px; font-weight:700;">{margin:.1%}</div>
    <div style="color:#475569; font-size:13px;">Profit Margin</div>
  </div>
  <div style="background:#faf5ff; border-radius:12px; padding:18px 28px; text-align:center; min-width:180px;">
    <div style="color:#7c3aed; font-size:26px; font-weight:700;">{orders:,}</div>
    <div style="color:#475569; font-size:13px;">Total Orders</div>
  </div>
</div>
"""

html_body = pio.to_html(fig, full_html=False, include_plotlyjs='cdn')

full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Sales Performance Dashboard</title></head>
<body style="margin:0; background:#f8fafc; font-family:'Segoe UI', Arial, sans-serif;">
<h1 style="text-align:center; color:#1e293b; padding-top:24px;">Sales Performance Dashboard</h1>
<p style="text-align:center; color:#64748b;">Sample Superstore Dataset · Jan 2015 – Dec 2018</p>
{kpi_html}
<div style="display:flex; justify-content:center;">
{html_body}
</div>
</body></html>
"""

with open('/home/claude/project1_sales_performance/dashboard/sales_dashboard.html', 'w') as f:
    f.write(full_html)

print("Dashboard written.")

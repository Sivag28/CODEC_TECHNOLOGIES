const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, PageOrientation
} = require('docx');
const fs = require('fs');

const C = '/home/claude/project1_sales_performance/charts';

function h1(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 } }); }
function h2(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 240, after: 120 } }); }
function body(text) { return new Paragraph({ children: [new TextRun({ text, size: 22 })], spacing: { after: 160 } }); }
function bullet(text) { return new Paragraph({ children: [new TextRun({ text, size: 22 })], bullet: { level: 0 }, spacing: { after: 80 } }); }
function img(path, width, height) {
  return new Paragraph({
    children: [new ImageRun({ type: 'png', data: fs.readFileSync(path), transformation: { width, height } })],
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 }
  });
}
function caption(text) {
  return new Paragraph({ children: [new TextRun({ text, italics: true, size: 18, color: '64748B' })], alignment: AlignmentType.CENTER, spacing: { after: 260 } });
}

function kpiCell(label, value, color) {
  return new TableCell({
    width: { size: 25, type: WidthType.PERCENTAGE },
    shading: { type: ShadingType.CLEAR, fill: 'F1F5F9' },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: 'CBD5E1' },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: 'CBD5E1' },
      left: { style: BorderStyle.SINGLE, size: 2, color: 'CBD5E1' },
      right: { style: BorderStyle.SINGLE, size: 2, color: 'CBD5E1' },
    },
    children: [
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100 }, children: [new TextRun({ text: value, bold: true, size: 30, color })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: label, size: 18, color: '475569' })] }),
    ]
  });
}

const kpiTable = new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  columnWidths: [2340, 2340, 2340, 2340],
  rows: [
    new TableRow({ children: [
      kpiCell('Total Sales', '$2.30M', '2563EB'),
      kpiCell('Total Profit', '$286.4K', '16A34A'),
      kpiCell('Profit Margin', '12.5%', 'D97706'),
      kpiCell('Total Orders', '5,009', '7C3AED'),
    ]})
  ]
});

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 } } },
    children: [
      new Paragraph({ children: [new TextRun({ text: 'Sales Performance Analysis', bold: true, size: 44, color: '1E293B' })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: 'Sample Superstore Dataset · January 2015 – December 2018', size: 22, color: '64748B' })], spacing: { after: 300 } }),

      kpiTable,

      h1('1. Project Overview'),
      body('This analysis examines four years of historical order-level data from a nationwide retail superstore to uncover sales trends, seasonal demand patterns, and top-performing products, categories, and regions. The goal is to surface actionable insights that support inventory planning, marketing timing, and profitability improvement.'),
      bullet('Dataset: 9,994 cleaned order line items, Jan 2015 – Dec 2018'),
      bullet('Fields: Order date, customer segment, region, category/sub-category, product, sales, quantity, discount, profit'),
      bullet('Tools used: Python (Pandas, Matplotlib, Plotly) for cleaning, analysis, and the interactive dashboard'),

      h1('2. Overall Trend'),
      body('Monthly sales show a clear long-term upward trend across the four-year period, punctuated by strong seasonal spikes. After a slight dip in 2016 (-2.8% YoY), revenue grew 29.5% in 2017 and a further 20.4% in 2018, indicating accelerating business momentum going into 2019.'),
      img(`${C}/01_monthly_trend.png`, 620, 282),
      caption('Figure 1: Monthly sales (solid) and profit (dashed) trend, 2015–2018.'),

      h1('3. Seasonal Patterns'),
      body('Aggregating sales by calendar month across all four years reveals a strong end-of-year buying pattern. November is consistently the strongest month, while February is consistently the weakest — a pattern retailers can use to plan inventory build-up and staffing ahead of Q4.'),
      img(`${C}/02_seasonality.png`, 580, 290),
      caption('Figure 2: Total sales by calendar month, all years combined. November (highlighted) is the peak month.'),

      h1('4. Top-Performing Products'),
      body(`The Canon imageCLASS 2200 Advanced Copier is the single highest-revenue product at roughly $61.6K in cumulative sales, with high-value office technology (copiers, phones) dominating the top-10 list. This suggests technology products carry disproportionate revenue weight despite lower unit volumes than office supplies.`),
      img(`${C}/03_top_products.png`, 580, 348),
      caption('Figure 3: Top 10 products ranked by total sales.'),

      h1('5. Category & Regional Performance'),
      body('Technology is the top-selling category overall, while Furniture — despite solid sales — delivers the weakest profit contribution of the three categories, largely due to heavy discounting on tables and bookcases. Regionally, the West leads in both sales and profit, while other regions show comparatively thinner margins.'),
      img(`${C}/04_category_performance.png`, 480, 267),
      caption('Figure 4: Sales and profit by product category.'),
      img(`${C}/05_region_performance.png`, 480, 267),
      caption('Figure 5: Sales and profit by region.'),

      h1('6. Discount Impact on Profitability'),
      body('Discounting shows a strong negative relationship with profit margin. Orders discounted at 30% or more are unprofitable in 96.8% of cases, indicating that current discount thresholds well beyond ~20% are eroding margin faster than they are driving incremental volume.'),
      img(`${C}/06_discount_vs_margin.png`, 520, 318),
      caption('Figure 6: Discount rate vs. profit margin per order — high discounts cluster in negative-margin territory.'),

      h1('7. Key Recommendations'),
      bullet('Build inventory and staffing plans around the Sep–Nov demand ramp; treat February as a natural low-season window for maintenance, training, or promotions to smooth revenue.'),
      bullet('Cap standard discounting at ~20% for Furniture sub-categories (Tables, Bookcases) where margin erosion is most severe, and reserve deeper discounts for clearance-only SKUs.'),
      bullet('Double down on Technology merchandising (copiers, accessories) in the West region, which combines the highest sales with the highest profit — a template to replicate in weaker regions.'),
      bullet('Introduce bundling for Furniture items with complementary Office Supplies to lift average order value without relying on blanket discounts.'),

      h1('8. Interactive Dashboard'),
      body('An accompanying interactive HTML dashboard (dashboard/sales_dashboard.html) lets stakeholders filter and explore monthly trends, seasonality, top products, and category/region performance directly in a browser — no software installation required.'),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('/home/claude/project1_sales_performance/reports/Sales_Performance_Analysis_Report.docx', buf);
  console.log('Report written.');
});

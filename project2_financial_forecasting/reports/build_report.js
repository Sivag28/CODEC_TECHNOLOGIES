const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, ImageRun, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType
} = require('docx');
const fs = require('fs');

const C = '/home/claude/project2_financial_forecasting/charts';

function h1(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 } }); }
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
      kpiCell('Validation MAPE', '15.6%', '2563EB'),
      kpiCell('Avg Monthly Sales', '$47.9K', '16A34A'),
      kpiCell('2018 YoY Growth', '+20.4%', 'D97706'),
      kpiCell('Next 6-Mo Forecast', '$354.4K', '7C3AED'),
    ]})
  ]
});

// Forecast table
const forecastRows = [
  ['Jan 2019', '$47,337'], ['Feb 2019', '$39,353'], ['Mar 2019', '$76,412'],
  ['Apr 2019', '$60,367'], ['May 2019', '$65,417'], ['Jun 2019', '$65,518'],
];
function fCell(text, header=false) {
  return new TableCell({
    width: { size: 50, type: WidthType.PERCENTAGE },
    shading: header ? { type: ShadingType.CLEAR, fill: '1E293B' } : undefined,
    children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text, bold: header, color: header ? 'FFFFFF' : '000000', size: 20 })] })]
  });
}
const forecastTable = new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  rows: [
    new TableRow({ children: [fCell('Month', true), fCell('Forecasted Revenue', true)] }),
    ...forecastRows.map(([m, v]) => new TableRow({ children: [fCell(m), fCell(v)] }))
  ]
});

const doc = new Document({
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 } } },
    children: [
      new Paragraph({ children: [new TextRun({ text: 'Financial Forecasting Report', bold: true, size: 44, color: '1E293B' })], spacing: { after: 60 } }),
      new Paragraph({ children: [new TextRun({ text: 'Sample Superstore Dataset · Revenue Forecast for Jan–Jun 2019', size: 22, color: '64748B' })], spacing: { after: 300 } }),

      kpiTable,

      h1('1. Objective'),
      body('This report uses four years of historical monthly revenue (Jan 2015 – Dec 2018) to forecast expected revenue for the next six months. The goal is to give finance and operations teams a data-driven baseline for budgeting, cash-flow planning, and target-setting.'),
      bullet('Method: Holt-Winters Triple Exponential Smoothing (additive trend + additive seasonality, 12-month period)'),
      bullet('Validation: model trained on the first 42 months, tested against the final 6 actual months'),
      bullet('Tools used: Python (Statsmodels, Scikit-learn, Matplotlib)'),

      h1('2. Seasonal Decomposition'),
      body('Breaking the monthly revenue series into trend, seasonal, and residual components confirms a steady upward trend across the four years, with a repeating annual seasonal pattern (a strong Q4 peak, a Q1 trough) and no major structural anomalies in the residuals.'),
      img(`${C}/01_decomposition.png`, 560, 458),
      caption('Figure 1: Additive decomposition of monthly revenue into trend, seasonal, and residual components.'),

      h1('3. Model Validation'),
      body('Before forecasting the future, the model was tested on data it had not seen: trained on the first 3.5 years and evaluated against the actual final 6 months. The model achieved a Mean Absolute Percentage Error (MAPE) of 15.6%, correctly capturing the direction and rough magnitude of the year-end seasonal swing, which gives reasonable confidence in the forward-looking forecast.'),
      img(`${C}/02_model_validation.png`, 580, 264),
      caption('Figure 2: Validation forecast (red) vs. actual held-out revenue (green) for the last 6 known months.'),

      h1('4. Six-Month Revenue Forecast'),
      body('Using the full four-year history, the model projects the following monthly revenue for the first half of 2019. Total projected revenue for the period is approximately $354,400, consistent with the seasonal low typically seen in Q1 followed by a build into spring.'),
      img(`${C}/03_future_forecast.png`, 580, 264),
      caption('Figure 3: Historical revenue with 6-month forward forecast and an approximate 95% confidence band.'),
      forecastTable,

      h1('5. Key Insights & Recommendations'),
      bullet('Expect a seasonal dip in January–February 2019, consistent with every prior year — plan cash reserves and discretionary spend accordingly rather than treating it as underperformance.'),
      bullet('March 2019 is forecast to rebound sharply (~$76K), so inventory and staffing should ramp ahead of quarter-end rather than reactively.'),
      bullet('2018 closed with 20.4% YoY growth; if that momentum continues beyond this conservative baseline forecast, actual 2019 H1 revenue could outperform the model — treat these figures as a floor, not a ceiling, for target-setting.'),
      bullet('Re-run this model quarterly as new actuals arrive to narrow the confidence interval and catch any deviation from trend early.'),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('/home/claude/project2_financial_forecasting/reports/Financial_Forecasting_Report.docx', buf);
  console.log('Report written.');
});

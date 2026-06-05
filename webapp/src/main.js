/* ============================================
   CUSTOMER SEGMENTATION DASHBOARD - MAIN JS
   ============================================ */

import Chart from 'chart.js/auto';

// ============================================
// CHART.JS GLOBAL DEFAULTS
// ============================================
Chart.defaults.color = '#8888a0';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.plugins.legend.labels.padding = 16;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.legend.labels.pointStyle = 'circle';
// Chart defaults removed temporarily for debugging

// Color palette
const COLORS = {
  purple: '#6c5ce7',
  lavender: '#a29bfe',
  blue: '#74b9ff',
  cyan: '#00cec9',
  green: '#55efc4',
  yellow: '#fdcb6e',
  orange: '#e17055',
  red: '#ff7675',
  pink: '#fd79a8',
  teal: '#81ecec',
};

const CHART_COLORS = [
  COLORS.purple, COLORS.blue, COLORS.cyan, COLORS.green,
  COLORS.yellow, COLORS.orange, COLORS.red, COLORS.pink,
  COLORS.lavender, COLORS.teal,
];


// ============================================
// DATA LOADING
// ============================================
async function loadJSON(path) {
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`Failed to load ${path}`);
    return await response.json();
  } catch (error) {
    console.error(`Error loading ${path}:`, error);
    return null;
  }
}

// Helper: make semi-transparent version of a hex color
function alpha(hex, a) {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r}, ${g}, ${b}, ${a})`;
}


// ============================================
// HERO SECTION
// ============================================
function renderHeroStats(overview) {
  const container = document.getElementById('hero-stats');
  if (!container || !overview) return;

  const stats = [
    { value: overview.total_customers?.toLocaleString() || '—', label: 'Customers' },
    { value: overview.total_features || '—', label: 'Features' },
    { value: '2', label: 'Datasets' },
  ];

  container.innerHTML = stats.map(s => `
    <div class="hero-stat">
      <div class="hero-stat-value">${s.value}</div>
      <div class="hero-stat-label">${s.label}</div>
    </div>
  `).join('');
}


// ============================================
// EDA CHARTS
// ============================================
function renderGenderChart(demographics) {
  const ctx = document.getElementById('chart-gender');
  if (!ctx || !demographics?.gender) return;

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(demographics.gender),
      datasets: [{
        data: Object.values(demographics.gender),
        backgroundColor: [COLORS.purple, COLORS.pink],
        hoverBackgroundColor: [COLORS.lavender, COLORS.red],
        borderWidth: 0,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      cutout: '65%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { padding: 20, font: { size: 11 } }
        },
      },
    }
  });
}


function renderAgeChart(demographics) {
  const ctx = document.getElementById('chart-age');
  if (!ctx || !demographics?.age_distribution) return;

  const keys = Object.keys(demographics.age_distribution);
  const values = Object.values(demographics.age_distribution);

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: keys,
      datasets: [{
        data: values,
        backgroundColor: keys.map((_, i) => alpha(CHART_COLORS[i % CHART_COLORS.length], 0.8)),
        borderWidth: 0,
      }]
    },
    options: {
      responsive: true,
      cutout: '50%',
      plugins: {
        legend: {
          position: 'right',
          labels: { padding: 12, font: { size: 10 } }
        }
      }
    }
  });
}


function renderEducationChart(demographics) {
  const ctx = document.getElementById('chart-education');
  if (!ctx || !demographics?.education) return;

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: Object.keys(demographics.education),
      datasets: [{
        data: Object.values(demographics.education),
        backgroundColor: [COLORS.blue, COLORS.purple, COLORS.cyan, COLORS.yellow],
        borderWidth: 0,
        hoverOffset: 8,
      }]
    },
    options: {
      responsive: true,
      cutout: '60%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: { padding: 16, font: { size: 11 } }
        },
      },
    }
  });
}


function renderSpendingChart(spending) {
  const ctx = document.getElementById('chart-spending');
  if (!ctx || !spending?.average_per_category) return;

  const labels = Object.keys(spending.average_per_category);
  const values = Object.values(spending.average_per_category);

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: labels.map((_, i) => alpha(CHART_COLORS[i % CHART_COLORS.length], 0.8)),
        borderWidth: 0,
      }]
    },
    options: {
      responsive: true,
      cutout: '40%',
      plugins: {
        legend: { position: 'right', labels: { font: { size: 10 } } },
        tooltip: {
          callbacks: {
            label: (item) => ` €${item.raw.toLocaleString()}`
          }
        }
      }
    }
  });
}

function renderTotalSpendChart(spending) {
  const ctx = document.getElementById('chart-total-spend');
  if (!ctx || !spending?.total_spend_histogram) return;

  const edges = spending.total_spend_histogram.bin_edges;
  const labels = edges.slice(0, -1).map((e, i) =>
    `€${Math.round(e)}-€${Math.round(edges[i + 1])}`
  );

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Customers',
        data: spending.total_spend_histogram.counts,
        backgroundColor: alpha(COLORS.blue, 0.4),
        borderColor: COLORS.blue,
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { font: { size: 10 } } },
        x: { ticks: { font: { size: 9 }, maxRotation: 45 } }
      }
    }
  });
}

function renderChildrenChart(demographics) {
  const ctx = document.getElementById('chart-children');
  
  if (!ctx) return;
  
  let dataKeys, dataValues, chartType;

  if (demographics?.total_children) {
    dataKeys = Object.keys(demographics.total_children);
    dataValues = Object.values(demographics.total_children);
    
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: dataKeys.map(k => `${k} Children`),
        datasets: [{
          data: dataValues,
          backgroundColor: dataKeys.map((_, i) => alpha(CHART_COLORS[i % CHART_COLORS.length], 0.8)),
          borderWidth: 0,
        }]
      },
      options: {
        responsive: true,
        plugins: { 
          legend: { position: 'right', labels: { padding: 12, font: { size: 10 } } }
        }
      }
    });
  } else if (demographics?.has_children) {
    dataKeys = Object.keys(demographics.has_children);
    dataValues = Object.values(demographics.has_children);
    
    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: dataKeys,
        datasets: [{
          data: dataValues,
          backgroundColor: [COLORS.green, COLORS.orange],
          borderWidth: 0,
          hoverOffset: 8,
        }]
      },
      options: {
        responsive: true,
        cutout: '65%',
        plugins: {
          legend: { position: 'bottom', labels: { padding: 16, font: { size: 11 } } },
        },
      }
    });
  }
}

function renderBasketChart(basket) {
  const ctx = document.getElementById('chart-basket');
  if (!ctx || !basket?.trips_histogram) return;

  const edges = basket.trips_histogram.bin_edges;
  const labels = edges.slice(0, -1).map((e, i) =>
    `${Math.round(e)}-${Math.round(edges[i + 1])}`
  );

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Customers',
        data: basket.trips_histogram.counts,
        backgroundColor: alpha(COLORS.purple, 0.4),
        borderColor: COLORS.purple,
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { font: { size: 10 } } },
        x: { ticks: { font: { size: 9 }, maxRotation: 45 } }
      }
    }
  });
}


function renderTimeChart(demographics) {
  const ctx = document.getElementById('chart-time');
  if (!ctx || !demographics?.time_of_day) return;

  const order = ['Morning', 'Afternoon', 'Evening', 'Night'];
  const labels = order.filter(k => k in demographics.time_of_day);
  const values = labels.map(k => demographics.time_of_day[k]);
  const colors = [COLORS.yellow, COLORS.orange, COLORS.purple, COLORS.blue];

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: labels.map((_, i) => alpha(colors[i], 0.8)),
        borderWidth: 0,
      }]
    },
    options: {
      responsive: true,
      cutout: '50%',
      plugins: { 
        legend: { position: 'right', labels: { padding: 12, font: { size: 10 } } }
      }
    }
  });
}


function renderCorrelationChart(correlation) {
  const ctx = document.getElementById('chart-correlation');
  if (!ctx || !correlation) return;

  const { labels, matrix } = correlation;
  const n = labels.length;

  // Build data points
  const data = [];
  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      data.push({ x: j, y: i, v: matrix[i][j] });
    }
  }

  // Custom canvas heatmap
  const canvas = ctx;
  const context = canvas.getContext('2d');

  const parent = canvas.parentElement;
  const width = parent.clientWidth;
  const height = Math.min(width * 0.85, 380);
  canvas.width = width * 2;
  canvas.height = height * 2;
  canvas.style.width = width + 'px';
  canvas.style.height = height + 'px';
  context.scale(2, 2);

  const marginLeft = 100;
  const marginBottom = 80;
  const marginTop = 10;
  const marginRight = 20;
  const plotW = width - marginLeft - marginRight;
  const plotH = height - marginBottom - marginTop;
  const cellW = plotW / n;
  const cellH = plotH / n;

  // Draw cells
  for (const { x, y, v } of data) {
    if (x > y) continue; // Cut the upper triangle
    
    const val = v;
    let r, g, b;
    if (val > 0) {
      r = Math.round(108 + val * 147);
      g = Math.round(92 + val * 100);
      b = 231;
    } else {
      r = Math.round(108 - val * 147);
      g = 92;
      b = Math.round(231 + val * 80);
    }
    const a = Math.abs(val) * 0.8 + 0.1;

    context.fillStyle = `rgba(${r}, ${g}, ${b}, ${a})`;
    context.fillRect(marginLeft + x * cellW, marginTop + y * cellH, cellW - 1, cellH - 1);

    if (cellW > 30) {
      context.fillStyle = Math.abs(val) > 0.5 ? '#fff' : '#8888a0';
      context.font = '9px Inter';
      context.textAlign = 'center';
      context.textBaseline = 'middle';
      context.fillText(
        val.toFixed(1),
        marginLeft + x * cellW + cellW / 2,
        marginTop + y * cellH + cellH / 2
      );
    }
  }

  // Y-axis labels
  context.fillStyle = '#8888a0';
  context.font = '9px Inter';
  context.textAlign = 'right';
  context.textBaseline = 'middle';
  labels.forEach((label, i) => {
    const short = label.length > 14 ? label.slice(0, 12) + '..' : label;
    context.fillText(short, marginLeft - 6, marginTop + i * cellH + cellH / 2);
  });

  // X-axis labels (rotated)
  labels.forEach((label, i) => {
    const short = label.length > 14 ? label.slice(0, 12) + '..' : label;
    context.save();
    context.translate(marginLeft + i * cellW + cellW / 2, marginTop + plotH + 8);
    context.rotate(-Math.PI / 3);
    context.textAlign = 'right';
    context.textBaseline = 'middle';
    context.fillText(short, 0, 0);
    context.restore();
  });
}

function renderGeography(geography) {
  const mapContainer = document.getElementById('customer-map');
  if (!mapContainer || !geography || !geography.points) return;

  const map = L.map('customer-map').setView([38.74, -9.15], 11);

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map);

  geography.points.forEach(point => {
    L.circleMarker([point.lat, point.lng], {
      radius: 4,
      fillColor: COLORS.purple,
      color: COLORS.purple,
      weight: 1,
      opacity: 0.6,
      fillOpacity: 0.4
    }).addTo(map);
  });
}

// ============================================
// PREPROCESSING SECTION
// ============================================
function renderPreprocessing(preprocessing) {
  if (!preprocessing) return;

  // Before/After comparison
  const compContainer = document.getElementById('comparison-stats');
  if (compContainer) {
    const { raw, clean } = preprocessing;
    compContainer.innerHTML = `
      <div class="comparison-card before">
        <div class="comparison-label">Raw Data</div>
        <div class="comparison-stats">
          <div class="comparison-stat">
            <span class="comparison-stat-label">Rows</span>
            <span class="comparison-stat-value">${raw.rows?.toLocaleString()}</span>
          </div>
          <div class="comparison-stat">
            <span class="comparison-stat-label">Columns</span>
            <span class="comparison-stat-value">${raw.columns}</span>
          </div>
          <div class="comparison-stat">
            <span class="comparison-stat-label">Missing Values</span>
            <span class="comparison-stat-value" style="color: var(--danger)">${raw.missing_values?.toLocaleString()}</span>
          </div>
          <div class="comparison-stat">
            <span class="comparison-stat-label">Duplicates</span>
            <span class="comparison-stat-value" style="color: var(--danger)">${raw.duplicates?.toLocaleString()}</span>
          </div>
        </div>
      </div>
      <div class="comparison-arrow">→</div>
      <div class="comparison-card after">
        <div class="comparison-label">Clean Data</div>
        <div class="comparison-stats">
          <div class="comparison-stat">
            <span class="comparison-stat-label">Rows</span>
            <span class="comparison-stat-value">${clean.rows?.toLocaleString()}</span>
          </div>
          <div class="comparison-stat">
            <span class="comparison-stat-label">Columns</span>
            <span class="comparison-stat-value">${clean.columns}</span>
          </div>
          <div class="comparison-stat">
            <span class="comparison-stat-label">Missing Values</span>
            <span class="comparison-stat-value" style="color: var(--success)">${clean.missing_values}</span>
          </div>
          <div class="comparison-stat">
            <span class="comparison-stat-label">Duplicates</span>
            <span class="comparison-stat-value" style="color: var(--success)">${clean.duplicates}</span>
          </div>
        </div>
      </div>
    `;
  }

  // Pipeline steps
  const pipelineContainer = document.getElementById('pipeline-steps');
  if (pipelineContainer && preprocessing.pipeline_steps) {
    pipelineContainer.innerHTML = preprocessing.pipeline_steps.map((step, i) => `
      <div class="pipeline-step">
        <div class="pipeline-marker">${String(i + 1).padStart(2, '0')}</div>
        <div class="pipeline-info">
          <h4>${step.name}</h4>
          <p>${step.description}</p>
        </div>
      </div>
    `).join('');
  }
}


// ============================================
// NAVIGATION
// ============================================
function initNavigation() {
  const nav = document.getElementById('main-nav');
  const links = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('.section');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }

    let current = '';
    sections.forEach(section => {
      const rect = section.getBoundingClientRect();
      if (rect.top <= 200) {
        current = section.getAttribute('id');
      }
    });

    links.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('data-section') === current) {
        link.classList.add('active');
      }
    });
  });
}


// ============================================
// FADE-IN ON SCROLL (non-chart elements only)
// ============================================
function initScrollAnimations() {
  const animatableElements = document.querySelectorAll('.comparison-card, .coming-soon-container, .report-block, .fade-in');
  animatableElements.forEach(el => el.classList.add('fade-in'));

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  animatableElements.forEach(el => observer.observe(el));
}


// ============================================
// INTERACTIVE TABS
// ============================================
function initTabs() {
  const tabs = document.querySelectorAll('.insight-tab');
  const contents = document.querySelectorAll('.insight-content');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Remove active from all tabs and contents
      tabs.forEach(t => t.classList.remove('active'));
      contents.forEach(c => c.classList.remove('active'));

      // Add active to clicked tab
      tab.classList.add('active');

      // Find and show corresponding content
      const tabId = tab.getAttribute('data-tab');
      const content = document.getElementById(`content-${tabId}`);
      if (content) {
        content.classList.add('active');
        
        // Trigger resize on charts and map to ensure they render correctly
        setTimeout(() => {
          window.dispatchEvent(new Event('resize'));
        }, 50);
      }
    });
  });
}

// ============================================
// NEW CHART RENDERING FUNCTIONS
// ============================================

function renderAgeBarChart(demographics) {
  const ctx = document.getElementById('chart-age-bar');
  if (!ctx || !demographics?.age_distribution) return;

  const keys = Object.keys(demographics.age_distribution);
  const values = Object.values(demographics.age_distribution);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: keys,
      datasets: [{
        label: 'Customers',
        data: values,
        backgroundColor: keys.map((_, i) => alpha(CHART_COLORS[i % CHART_COLORS.length], 0.8)),
        borderWidth: 0,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { font: { size: 10 } } },
        x: { ticks: { font: { size: 10 } } }
      }
    }
  });
}

function renderEducationBarChart(demographics) {
  const ctx = document.getElementById('chart-education-bar');
  if (!ctx || !demographics?.education) return;

  const keys = Object.keys(demographics.education);
  const values = Object.values(demographics.education);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: keys,
      datasets: [{
        label: 'Count',
        data: values,
        backgroundColor: [COLORS.blue, COLORS.purple, COLORS.cyan, COLORS.yellow].map(c => alpha(c, 0.8)),
        borderWidth: 0,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { beginAtZero: true, ticks: { font: { size: 10 } } },
        y: { ticks: { font: { size: 10 } } }
      }
    }
  });
}

function renderSpendingBarChart(spending) {
  const ctx = document.getElementById('chart-spending-bar');
  if (!ctx || !spending?.average_per_category) return;

  const entries = Object.entries(spending.average_per_category).sort((a, b) => b[1] - a[1]);
  const labels = entries.map(e => e[0]);
  const values = entries.map(e => e[1]);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Avg Spend (€)',
        data: values,
        backgroundColor: alpha(COLORS.blue, 0.8),
        borderWidth: 0,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { font: { size: 10 } } },
        x: { ticks: { font: { size: 9 }, maxRotation: 45, minRotation: 45 } }
      }
    }
  });
}

function renderSpendStatsChart(spending) {
  const ctx = document.getElementById('chart-spend-stats');
  if (!ctx || !spending?.total_spend_stats) return;

  const stats = spending.total_spend_stats;
  const labels = ['Mean', 'Median'];
  const values = [stats.mean, stats.median];

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Total Spend (€)',
        data: values,
        backgroundColor: [alpha(COLORS.purple, 0.8), alpha(COLORS.pink, 0.8)],
        borderWidth: 0,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: { beginAtZero: true, ticks: { font: { size: 10 } } },
        y: { ticks: { font: { size: 11 } } }
      }
    }
  });
}

function renderTripStatsChart(basket) {
  const ctx = document.getElementById('chart-trip-stats');
  if (!ctx || !basket['Total Trips'] || !basket['Total Items Bought']) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Mean', 'Median'],
      datasets: [
        {
          label: 'Total Trips',
          data: [basket['Total Trips'].mean, basket['Total Trips'].median],
          backgroundColor: alpha(COLORS.green, 0.8),
          borderRadius: 4
        },
        {
          label: 'Total Items',
          data: [basket['Total Items Bought'].mean, basket['Total Items Bought'].median],
          backgroundColor: alpha(COLORS.teal, 0.8),
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } },
      scales: {
        y: { beginAtZero: true, ticks: { font: { size: 10 } } },
        x: { ticks: { font: { size: 11 } } }
      }
    }
  });
}

function renderBasketSizesChart(basket) {
  const ctx = document.getElementById('chart-basket-sizes');
  if (!ctx || !basket['Average Basket Size']) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Min Basket', 'Avg Basket', 'Max Basket'],
      datasets: [{
        label: 'Mean Size',
        data: [
          basket['Min Basket Size'].mean,
          basket['Average Basket Size'].mean,
          basket['Max Basket Size'].mean
        ],
        backgroundColor: [alpha(COLORS.orange, 0.8), alpha(COLORS.yellow, 0.8), alpha(COLORS.red, 0.8)],
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { font: { size: 10 } } },
        x: { ticks: { font: { size: 10 } } }
      }
    }
  });
}

function renderUniqueProductsChart(basket) {
  const ctx = document.getElementById('chart-unique-products');
  if (!ctx || !basket['Unique Products Bought']) return;

  const stats = basket['Unique Products Bought'];
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Mean', 'Median', 'Min', 'Max'],
      datasets: [{
        label: 'Unique Products',
        data: [stats.mean, stats.median, stats.min, stats.max],
        backgroundColor: alpha(COLORS.cyan, 0.8),
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { font: { size: 10 } } },
        x: { ticks: { font: { size: 10 } } }
      }
    }
  });
}


// ============================================
// MAIN INITIALIZATION
// ============================================
async function init() {
  console.log('Customer Segmentation Dashboard loading...');

  // Load all data in parallel
  const [overview, demographics, spending, basket, preprocessing, correlation, geography] = await Promise.all([
    loadJSON('/data/dataset_overview.json'),
    loadJSON('/data/demographics.json'),
    loadJSON('/data/spending.json'),
    loadJSON('/data/basket_stats.json'),
    loadJSON('/data/preprocessing.json'),
    loadJSON('/data/correlation.json'),
    loadJSON('/data/geography.json'),
  ]);

  // Debug: log the data to console
  console.log('Demographics:', demographics);
  console.log('Spending:', spending);
  console.log('Basket:', basket);

  // Render sections
  renderHeroStats(overview);
  renderGenderChart(demographics);
  renderAgeBarChart(demographics);
  renderEducationBarChart(demographics);
  renderSpendingChart(spending);
  renderSpendingBarChart(spending);
  renderTotalSpendChart(spending);
  renderSpendStatsChart(spending);
  renderChildrenChart(demographics);
  renderBasketChart(basket);
  renderTimeChart(demographics);
  renderTripStatsChart(basket);
  renderBasketSizesChart(basket);
  renderUniqueProductsChart(basket);
  renderCorrelationChart(correlation);
  renderGeography(geography);
  renderPreprocessing(preprocessing);

  // Init UI
  initNavigation();
  initTabs();

  // Delay scroll animations to not interfere with chart rendering
  setTimeout(() => {
    initScrollAnimations();
  }, 500);

  console.log('Dashboard loaded successfully');
}

// Start the app
document.addEventListener('DOMContentLoaded', init);

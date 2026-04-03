const API_BASE = 'http://localhost:8080/api/v1';

const params = new URLSearchParams(window.location.search);
const symbol = params.get('symbol');

const loading = document.getElementById('loading');
const content = document.getElementById('content');
const error = document.getElementById('error');

function goBack() {
  window.history.back();
}

async function loadCompany() {
  try {

    const res = await fetch(`${API_BASE}/screener/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_query: 'price > 0' })
    });

    const data = await res.json();
    const stock = data.stocks.find(s => s.symbol === symbol);

    if (!stock) throw new Error('No data');

    document.getElementById('companyTitle').innerText = stock.name;
    document.getElementById('symbol').innerText = stock.symbol;
    document.getElementById('price').innerText = stock.price;
    document.getElementById('marketCap').innerText = stock.market_cap;
    document.getElementById('sector').innerText = stock.sector || 'N/A';
    document.getElementById('pe').innerText = stock.pe_ratio;
    document.getElementById('volume').innerText = stock.volume;

    document.getElementById('watchlistBtn').onclick = async () => {
      await fetch(`${API_BASE}/watchlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol })
      });
      alert(`${symbol} added to watchlist`);
    };

    loading.style.display = 'none';
    content.style.display = 'block';

  } catch (e) {
    loading.style.display = 'none';
    error.style.display = 'block';
  }
}

function renderPriceChart() {
  const ctx = document.getElementById('priceChart').getContext('2d');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Price ($)',
        data: [150, 155, 148, 160, 170, 175],
        borderColor: '#00e5ff',
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function renderRevenueChart() {
  const ctx = document.getElementById('revenueChart').getContext('2d');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['2019', '2020', '2021', '2022', '2023'],
      datasets: [{
        label: 'Revenue ($B)',
        data: [200, 220, 240, 260, 280],
        backgroundColor: '#4caf50'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      }
    }
  });

  document.getElementById('addPortfolioBtn').onclick = async () => {
  await fetch('http://localhost:8080/api/v1/portfolio', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      symbol,
      quantity: 10,
      buyPrice: document.getElementById('price').innerText
    })
  });

  alert('Added to portfolio');
};

}
loadCompany();
renderPriceChart();
renderRevenueChart();
content.style.display = 'block';


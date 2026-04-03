const API_BASE = '/api/v1';

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
      body: JSON.stringify({ raw_query: `symbol = '${symbol}'` })
    });

    const data = await res.json();
    const stock = data.stocks[0];

    if (!stock) throw new Error('No data found for ' + symbol);

    document.getElementById('companyTitle').innerText = stock.company_name;
    document.getElementById('symbol').innerText = stock.symbol;
    document.getElementById('price').innerText = parseFloat(stock.price).toFixed(2);
    
    let mktCap = parseFloat(stock.market_cap);
    if (mktCap > 1e12) {
        document.getElementById('marketCap').innerText = `$${(mktCap / 1e12).toFixed(2)}T`;
    } else {
        document.getElementById('marketCap').innerText = `$${(mktCap / 1e9).toFixed(2)}B`;
    }
    
    document.getElementById('sector').innerText = stock.sector || 'N/A';
    document.getElementById('pe').innerText = parseFloat(stock.pe_ratio).toFixed(2);
    document.getElementById('volume').innerText = stock.volume.toLocaleString();

    document.getElementById('watchlistBtn').onclick = async () => {
      await fetch(`${API_BASE}/watchlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol })
      });
      alert(`${symbol} added to watchlist!`);
    };

    document.getElementById('addPortfolioBtn').onclick = async () => {
      const qty = prompt("How many shares did you buy?", "10");
      if (!qty) return;

      const resPort = await fetch(`${API_BASE}/portfolio`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbol,
          quantity: parseFloat(qty),
          average_price: parseFloat(stock.price)
        })
      });

      if (resPort.ok) {
        alert(`${qty} shares of ${symbol} added to portfolio!`);
      } else {
        alert("Failed to add to portfolio.");
      }
    };

    loading.style.display = 'none';
    content.style.display = 'block';

  } catch (e) {
    console.error(e);
    loading.style.display = 'none';
    error.style.display = 'block';
  }
}

loadCompany();

console.log('✅ script.js loaded');

const API_BASE = 'http://localhost:8080/api/v1';

const runBtn = document.getElementById('runBtn');
const queryInput = document.getElementById('queryInput');
const resultsList = document.getElementById('resultsList');
const stockCount = document.getElementById('stockCount');

async function handleScan() {
  const query = queryInput.value.trim();
  console.log('🚀 Scan clicked with query:', query);

  if (!query) {
    alert('Enter a query');
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/screener/execute`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ raw_query: query })
    });

    const data = await res.json();
    console.log('📦 API RESPONSE:', data);

    renderResults(data.stocks || []);
    stockCount.innerText = `${data.total_matches} Matches`;

  } catch (err) {
    console.error('❌ Error:', err);
  }
}

function renderResults(stocks) {
  resultsList.innerHTML = '';

  if (!stocks.length) {
    resultsList.innerHTML = '<p>No results</p>';
    return;
  }

  stocks.forEach(stock => {
    const card = document.createElement('div');
    card.className = 'stock-card';

    card.innerHTML = `
      <b>${stock.symbol}</b> – ${stock.name}<br/>
      Price: $${stock.price} | PE: ${stock.pe_ratio}
      <button class="star">⭐</button>
    `;

    const starBtn = card.querySelector('.star');
    starBtn.addEventListener('click', async (e) => {
      e.stopPropagation(); 
      await fetch(`${API_BASE}/watchlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: stock.symbol })
      });
      alert(`${stock.symbol} added to watchlist`);
    });

    card.addEventListener('click', () => {
      console.log('➡ Opening company:', stock.symbol);
      window.location.href = `./company.html?symbol=${stock.symbol}`;
    });

    resultsList.appendChild(card);
  });
}

runBtn.addEventListener('click', handleScan);

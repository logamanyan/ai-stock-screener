const API_BASE = '/api/v1';

async function loadWatchlist() {
    try {
        const res = await fetch(`${API_BASE}/watchlist`);
        const data = await res.json();
        
        const list = document.getElementById('watchlistList');
        const summary = document.getElementById('watchlistSummary');

        if (data.status === 'success') {
            summary.innerHTML = `${data.data.length} symbol(s) pinned`;

            if (data.data.length === 0) {
                list.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">⭐</div>
                        <p class="empty-text">Your watchlist is empty. Pin stocks from the company details page.</p>
                        <button class="nav-btn" onclick="window.location.href='index.html'">Explore Stocks</button>
                    </div>`;
                return;
            }

            // Fetch live data for these symbols efficiently
            const resStocks = await fetch(`${API_BASE}/screener/execute`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ raw_query: 'symbol IN (' + data.data.map(s => `'${s}'`).join(',') + ')' })
            });

            const stockData = await resStocks.json();

            list.innerHTML = stockData.stocks.map(s => {
                const s_metrics = s;
                return `
                <div class="stock-card" onclick="window.location.href='company.html?symbol=${s_metrics.symbol}'">
                    <div class="card-top">
                        <div class="stock-info">
                            <span class="symbol">${s_metrics.symbol}</span>
                            <span class="sector">${s_metrics.sector || 'Various'}</span>
                        </div>
                        <span class="price">$${parseFloat(s_metrics.price).toFixed(2)}</span>
                    </div>

                    <div class="card-metrics">
                        <div class="metric">
                            <span class="label">P/E Ratio</span>
                            <span class="value">${s_metrics.pe_ratio || 'N/A'}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Market Cap</span>
                            <span class="value">$${(s_metrics.market_cap / 1e9).toFixed(1)}B</span>
                        </div>
                    </div>
                    <button class="nav-btn" style="margin-top: 10px; width:100%;" onclick="event.stopPropagation(); removeWatchlist('${s_metrics.symbol}')">🗑 Remove</button>
                </div>`;
            }).join('');
        }
    } catch (e) {
        console.error("Failed to load watchlist:", e);
        document.getElementById('watchlistList').innerHTML = '<p class="error-text">Failed to load watchlist data.</p>';
    }
}

async function removeWatchlist(symbol) {
    if (!confirm(`Remove ${symbol} from watchlist?`)) return;
    
    try {
        await fetch(`${API_BASE}/watchlist/${symbol}`, {
            method: 'DELETE'
        });
        loadWatchlist();
    } catch (e) {
        alert("Failed to remove item.");
    }
}

document.addEventListener('DOMContentLoaded', loadWatchlist);

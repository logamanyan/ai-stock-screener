const API_BASE = '/api/v1'; // Uses relative path, works for both local and Docker

async function loadPortfolio() {
    try {
        const res = await fetch(`${API_BASE}/portfolio`);
        const data = await res.json();
        
        const list = document.getElementById('portfolioList');
        const summary = document.getElementById('portfolioSummary');

        if (data.status === 'success') {
            // Update summary
            const s = data.summary;
            summary.innerHTML = `
                <span class="status-indicator" style="background: ${s.total_pl >= 0 ? 'var(--success)' : 'var(--error)'};"></span>
                <span class="status-text" style="color: ${s.total_pl >= 0 ? 'var(--success)' : 'var(--error)'};">
                    $${s.current_value.toFixed(2)} (${s.total_pl_percent.toFixed(2)}%)
                </span>
            `;

            if (data.data.length === 0) {
                list.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-icon">💼</div>
                        <p class="empty-text">Your portfolio is empty. Add stocks from the company details page.</p>
                        <button class="nav-btn" onclick="window.location.href='index.html'">Explore Stocks</button>
                    </div>`;
                return;
            }

            list.innerHTML = data.data.map(p => {
                const isProfit = p.profit_loss >= 0;
                return `
                <div class="stock-card" onclick="window.location.href='company.html?symbol=${p.symbol}'">
                    <div class="card-top">
                        <div class="stock-info">
                            <span class="symbol">${p.symbol}</span>
                            <span class="sector">Holding: ${p.quantity} shares</span>
                        </div>
                        <span class="price">$${p.live_price.toFixed(2)}</span>
                    </div>

                    <div class="card-metrics">
                        <div class="metric">
                            <span class="label">Investment</span>
                            <span class="value">$${p.investment.toFixed(2)}</span>
                        </div>
                        <div class="metric">
                            <span class="label">P&L</span>
                            <span class="value" style="color: ${isProfit ? 'var(--success)' : 'var(--error)'};">
                                ${isProfit ? '+' : ''}${p.profit_loss.toFixed(2)} (${p.pl_percent.toFixed(2)}%)
                            </span>
                        </div>
                    </div>
                </div>`;
            }).join('');
        }
    } catch (e) {
        console.error("Failed to load portfolio:", e);
        document.getElementById('portfolioList').innerHTML = '<p class="error-text">Failed to load portfolio data. Make sure the server is running.</p>';
    }
}

document.addEventListener('DOMContentLoaded', loadPortfolio);

fetch('http://localhost:8080/api/v1/portfolio')
  .then(res => res.json())
  .then(data => {
    const list = document.getElementById('portfolioList');

    if (!data.data.length) {
      list.innerHTML = '<p>No holdings yet</p>';
      return;
    }

    list.innerHTML = data.data.map(p => `
      <div class="stock-card">
        <b>${p.symbol}</b><br/>
        Qty: ${p.quantity}<br/>
        Buy Price: $${p.buyPrice}
      </div>
    `).join('');
  });

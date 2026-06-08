document.getElementById('footprint-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('calculate-btn');
    const resultsContainer = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const resultsContent = document.getElementById('results-content');
    
    // Disable button and show loader
    submitBtn.disabled = true;
    submitBtn.textContent = 'Calculating & Fetching Insights...';
    resultsContainer.classList.remove('hidden');
    loader.classList.remove('hidden');
    resultsContent.classList.add('hidden');
    
    // Gather data
    const payload = {
        transport_miles_per_week: parseFloat(document.getElementById('transport_miles_per_week').value),
        mpg: parseFloat(document.getElementById('mpg').value),
        electricity_kwh_per_month: parseFloat(document.getElementById('electricity_kwh_per_month').value),
        diet_type: document.getElementById('diet_type').value
    };
    
    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Populate metrics
            document.getElementById('res-transport').textContent = `${data.footprint.transport_co2_lbs} lbs CO₂`;
            document.getElementById('res-energy').textContent = `${data.footprint.energy_co2_lbs} lbs CO₂`;
            document.getElementById('res-diet').textContent = `${data.footprint.diet_co2_lbs} lbs CO₂`;
            document.getElementById('res-total').textContent = `${data.footprint.total_co2_lbs} lbs CO₂`;
            
            // Render markdown insights
            document.getElementById('ai-insights').innerHTML = marked.parse(data.insights);
            
            // Show content
            loader.classList.add('hidden');
            resultsContent.classList.remove('hidden');
        } else {
            alert('Error calculating footprint. Please try again.');
            resultsContainer.classList.add('hidden');
        }
    } catch (err) {
        console.error(err);
        alert('Failed to connect to the server.');
        resultsContainer.classList.add('hidden');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Calculate Footprint & Get Insights';
    }
});

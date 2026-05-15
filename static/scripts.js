async function loadLogs() {
    const res = await fetch("/api/logs");
    const data = await res.json();

    let html = "";

    data.forEach(log => {
        html += `
        <tr>
            <td data-label="IP">${log.ip}</td>
            <td data-label="Username">${log.username}</td>
            <td data-label="Password">${log.password}</td>
            <td data-label="Time">${log.timestamp}</td>
            <td data-label="Country">${log.country || "N/A"}</td>
            <td data-label="City">${log.city || "N/A"}</td>
        </tr>
        `;
    });

    document.getElementById("logs").innerHTML = html;
}

// refresh toutes les 2 secondes
setInterval(loadLogs, 2000);
loadLogs();

async function loadBruteforce() {
    const res = await fetch("/api/bruteforce");
    const data = await res.json();

    let html = "";

    data.forEach(log => {
        html += `
        <tr>
            <td data-label="IP">${log.ip}</td>
            <td data-label="Attempts">${log.attempts}</td>
        </tr>
        `;
    });

    document.getElementById("bruteforce").innerHTML = html;
}

// refresh toutes les 2 secondes
setInterval(loadBruteforce, 2000);
loadBruteforce();

async function loadMap() {
    const res = await fetch("/api/location");
    const data = await res.json();

    const map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    data.forEach(log => {
        if (log.lat && log.lon) {
            L.marker([log.lat, log.lon]).addTo(map)
                .bindPopup(`<b>${log.ip}</b><br>${log.country}, ${log.city}`);
        }
    });
}

loadMap();
let topPasswordsChart = null;

async function loadTopPasswords() {
    const res = await fetch("/api/top_passwords");
    const data = await res.json();

    const labels = data.map(d => d.password);
    const values = data.map(d => d.attempts);
    if (topPasswordsChart) topPasswordsChart.destroy();

    topPasswordsChart = new Chart(document.getElementById("topPasswords"), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Attempts',
                data: values,
            }]
        }
    });
}
loadTopPasswords();
setInterval(loadTopPasswords, 10000);

let topCountriesChart = null;

async function loadTopCountries() {
    const res = await fetch("/api/top_countries");
    const data = await res.json();

    const labels = data.map(d => d.country);
    const values = data.map(d => d.attempts);
    if (topCountriesChart) topCountriesChart.destroy();

    topCountriesChart = new Chart(document.getElementById("topCountries"), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Attempts',
                data: values,
            }]
        }
    });
}
loadTopCountries();
setInterval(loadTopCountries, 10000);

async function loadStats() {
    const res = await fetch("/api/stats");
    const data = await res.json();

    document.getElementById("totalAttempts").innerText = data.total_attempts;
    document.getElementById("uniqueIPs").innerText = data.unique_ips;
    document.getElementById("topCountry").innerText = data.unique_countries;
    const last = new Date(data.latest_timestamp + "Z");
    const diffMs = Date.now() - last.getTime();
    const diffMin = Math.floor(diffMs / 60000);
    const diffHr = Math.floor(diffMin / 60);
    document.getElementById("latestTimestamp").innerText = diffMin < 1 ? "Just now" : diffHr < 1 ? `${diffMin} min ago` : `${diffHr} hr ago`;
}

loadStats();
setInterval(loadStats, 2000);

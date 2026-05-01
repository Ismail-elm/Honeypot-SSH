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

async function loadTopPasswords() {
    const res = await fetch("/api/top_passwords");
    const data = await res.json();

    const labels = data.map(d => d.password);
    const values = data.map(d => d.attempts);

    new Chart(document.getElementById("topPasswords"), {
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
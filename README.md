# 🛡️ SSH Honeypot
 
A Python-based SSH honeypot that captures brute-force attempts and displays them in a real-time SOC dashboard.
 
## Features
 
- **SSH Honeypot** — Fake SSH server built with `paramiko` that captures IP, username, and password from every login attempt
- **IP Geolocation** — Automatically geolocates attacker IPs via `ip-api.com` with in-memory caching to avoid API rate limits
- **SQLite Storage** — Persists all attempts with IP, credentials, country, city, coordinates, and timestamp
- **Live SOC Dashboard** — Flask web interface with real-time updates every 2 seconds
- **Attack Heatmap** — World map (Leaflet.js) showing attack origins
- **Top Passwords Chart** — Bar chart (Chart.js) of the most commonly attempted passwords
- **Brute-force Detection** — Flags IPs with more than 10 attempts in the last hour
## Project Structure
 
```
honeypot-ssh/
├── honeypot_ssh.py    # SSH server (paramiko)
├── database.py        # SQLite logic + geolocation
├── app.py             # Flask dashboard
├── templates/
│   └── index.html     # Dashboard UI
├── static/
│   ├── styles.css
│   └── scripts.js
├── requirements.txt
└── .gitignore
```
 
## Installation
 
```bash
git clone https://github.com/Ismail-elm/Honeypot-SSH
cd honeypot-ssh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
 
## Usage
 
Start the honeypot (terminal 1) :
 
```bash
python honeypot_ssh.py
```
 
Start the dashboard (terminal 2) :
 
```bash
python app.py
```
 
Open your browser at `http://localhost:5000`
 
## How it works
 
1. The honeypot listens on port `2222` and accepts any SSH connection
2. Every login attempt is intercepted — credentials never grant access
3. The attacker IP is geolocated and stored in SQLite
4. The Flask dashboard reads the database and displays live stats
## Tech Stack
 
- **Python** — `paramiko`, `socket`, `threading`, `sqlite3`, `requests`
- **Flask** — REST API + web dashboard
- **Leaflet.js** — Interactive attack map
- **Chart.js** — Password frequency chart
- **SQLite** — Local database
## ⚠️ Legal Notice
 
This tool is intended for educational and research purposes only. Deploy only on infrastructure you own or have explicit permission to monitor.
import sqlite3
import requests
import threading
db_lock = threading.Lock()

def init_db():
    conn = sqlite3.connect('honeypot_ssh.db')
    c = conn.cursor()
    c.execute('''
            CREATE TABLE IF NOT EXISTS auth_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT,
                username TEXT,
                password TEXT,
                country TEXT,
                city TEXT,
                lat TEXT,
                lon TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            ''')
    conn.commit()
    conn.close()

def log_auth_attempt(ip, username, password, country, city, lat=None, lon=None):
    with db_lock:
        conn =sqlite3.connect('honeypot_ssh.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO auth_attempts (ip, username, password, country, city, lat, lon)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (ip, username, password, country, city, lat, lon))
        conn.commit()
        conn.close()    


cache = {}
def get_ip_location(ip):
    if ip in cache:
        return cache[ip]
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        if r.status_code == 200:
            data = r.json()
            
            if data['status'] == 'success':
                location = {
                    "country": data.get('country'),
                    "city": data.get('city'),
                    "lat": data.get('lat'),
                    "lon": data.get('lon')
                }
                cache[ip] = location
                return location
    except Exception as e:
        print(f"Error fetching IP location: {e}")
    return {
        "country": "Unknown",
        "city": "Unknown",
        "lat": "Unknown",
        "lon": "Unknown"
    }   

            
from flask import Flask, render_template, jsonify

app = Flask(__name__)
DB = 'honeypot_ssh.db'

def get_logs():
    import sqlite3
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT ip, username, password, timestamp, country, city FROM auth_attempts ORDER BY timestamp DESC LIMIT 50")
    logs = cursor.fetchall()
    conn.close()
    return logs

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/logs")
def api_logs():
    logs = get_logs()
    data = []
    for log in logs:
        data.append({
            "ip": log[0],
            "username": log[1],
            "password": log[2],
            "timestamp": log[3],
            "country": log[4],
            "city": log[5]
        })
    return jsonify(data)

@app.route("/api/bruteforce")
def api_bruteforce():
    import sqlite3
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ip, COUNT(*) as attempts
        FROM auth_attempts
        WHERE timestamp >= datetime('now', '-1 hour')
        GROUP BY ip HAVING attempts > 10
    ''')
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({
            "ip": row[0],
            "attempts": row[1]
        })
    return jsonify(data)

@app.route("/api/location")
def api_location():
    import sqlite3
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT lat, lon, COUNT(*) as attempts
        FROM auth_attempts
        GROUP BY lat, lon
        ORDER BY attempts DESC
        LIMIT 10
    ''')
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({
            "lat": row[0],
            "lon": row[1],
            "attempts": row[2]
        })
    return jsonify(data)

@app.route("/api/top_passwords")
def api_top_passwords():
    import sqlite3
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT password, COUNT(*) as attempts
        FROM auth_attempts
        GROUP BY password
        ORDER BY attempts DESC
        LIMIT 10
    ''')
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({
            "password": row[0],
            "attempts": row[1]
        })
    return jsonify(data)

@app.route("/api/top_countries")
def api_top_countries():
    import sqlite3
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT country, COUNT(*) as attempts
        FROM auth_attempts
        GROUP BY country
        ORDER BY attempts DESC
        LIMIT 10
    ''')
    results = cursor.fetchall()
    conn.close()
    data = []
    for row in results:
        data.append({
            "country": row[0],
            "attempts": row[1]
        })
    return jsonify(data)

@app.route("/api/stats")
def api_stats():
    import sqlite3
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM auth_attempts")
    total_attempts = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT ip) FROM auth_attempts")
    unique_ips = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(DISTINCT country) FROM auth_attempts")
    unique_countries = cursor.fetchone()[0]
    cursor.execute("SELECT timestamp FROM auth_attempts ORDER BY timestamp DESC LIMIT 1")
    latest_timestamp = cursor.fetchone()[0] 
    conn.close()
    return jsonify({
        "total_attempts": total_attempts,
        "unique_ips": unique_ips,
        "unique_countries": unique_countries,
        "latest_timestamp": latest_timestamp
    })


if __name__ == "__main__":
    app.run(debug=True)

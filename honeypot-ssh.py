import paramiko
import socket
import threading
import logging
import time
from database import init_db, log_auth_attempt, get_ip_location


init_db()
logging.basicConfig(level=logging.INFO)
host_key = paramiko.RSAKey.generate(2048)


class HoneypotSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
    def check_auth_password(self, username, password):
        logging.info(f"Authentication attempt with username: {username} and password: {password}")
        location = get_ip_location(self.client_ip)
        log_auth_attempt(self.client_ip, username, password, location['country'], location['city'], location['lat'], location['lon'])
        return paramiko.AUTH_FAILED
    def get_allowed_auths(self, username):
        return 'password'
    
def start_honeypot_ssh(host='0.0.0.0', port=2222):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    logging.info(f"Honeypot SSH listening on {host}:{port}")

    while True:
        client, addr = server.accept()
        logging.info(f"Connection from {addr}")
        threading.Thread(target=handle_client, args=(client, addr[0])).start()

def handle_client(client, client_ip):
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(host_key)
        transport.start_server(server=HoneypotSSHServer(client_ip))
        while transport.is_active():
            time.sleep(0.1)
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        transport.close()
        client.close()

if __name__ == "__main__":
    start_honeypot_ssh()
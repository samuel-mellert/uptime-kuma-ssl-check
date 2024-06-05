import ssl
import socket
import datetime
import requests
from dotenv import load_dotenv
import smtplib
import os
import time

load_dotenv()

def get_certificate_expiry(host, port, use_starttls=False):
    context = ssl.create_default_context()
    if use_starttls:
        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            cert = server.sock.getpeercert()
    else:
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
    
    expiry = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
    expiry = expiry.replace(tzinfo=datetime.timezone.utc)
    return expiry

def send_to_uptime_kuma(url, status, msg):
    params = {
        "status": status,
        "msg": msg
    }
    requests.get(url, params=params)

host = os.getenv("HOST")
port = int(os.getenv("PORT"))
minimum_validity_days = int(os.getenv("MINIMUM_VALIDITY_DAYS", 30))
uptime_kuma_push_url = os.getenv("UPTIME_KUMA_PUSH_URL")
heartbeat_interval = int(os.getenv("HEARTBEAT_INTERVAL", 0))

# Determine if STARTTLS is needed based on the port number
use_starttls = port in {25, 110, 143, 587}

while True:    
    try:
        expiry = get_certificate_expiry(host, port, use_starttls=use_starttls)
        now = datetime.datetime.now(datetime.timezone.utc)
        days_left = (expiry - now).days
        msg = f"SSL Expiry for {host}:{port} is in {days_left} days"
        if days_left < minimum_validity_days:
            status = "down"        
        else:
            status = "up"
        send_to_uptime_kuma(uptime_kuma_push_url, status, msg)
    except Exception as e:
        send_to_uptime_kuma(uptime_kuma_push_url, "down", str(e))

    if (heartbeat_interval > 0):
        time.sleep(heartbeat_interval)
    else:
        break

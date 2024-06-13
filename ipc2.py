from flask import Flask, request, render_template, redirect, url_for
import requests

app = Flask(__name__)

# File to store IP addresses
ip_file = "ip_addresses.txt"

# Function to get IP address and country
def get_ip_info():
    # Check if the X-Forwarded-For header is present
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    country = data.get("country", "Unknown")
    return ip, country

# Function to check if IP address is already saved
def is_ip_saved(ip):
    with open(ip_file, "r") as file:
        saved_ips = file.read().splitlines()
    return ip in saved_ips

# Route for homepage
@app.route("/")
def index():
    ip, country = get_ip_info()
    is_saved = is_ip_saved(ip)
    return render_template("index.html", ip=ip, country=country, is_saved=is_saved)

# Route for saving IP address
@app.route("/save")
def save_ip():
    ip, _ = get_ip_info()
    if not is_ip_saved(ip):
        with open(ip_file, "a") as file:
            file.write(ip + "\n")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session, url_for
import datetime
import json
import os

app = Flask(__name__)
app.secret_key = "secret_key"

SCADA_FILE = "scada_data.json"
users = {
    "mnovak": "203.0.113.50",
    "admin": "192.168.1.100"
}

def load_scada_data():
    if os.path.exists(SCADA_FILE):
        try:
            with open(SCADA_FILE, "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    print("SCADA DATA LOADED:", data)
                    return data
                else:
                    print("CHYBA: SCADA subor nie je v spravnom formate!")
        except (json.JSONDecodeError, ValueError):
            print("CHYBA: scada_data.json je poskodeny! Obnovujem pociatocne hodnoty.")

    default_data = {"water_level": 50, "pressure": 10, "temperature": 25}
    save_scada_data(default_data)
    return default_data

scada_data = load_scada_data()

def save_scada_data(data):
    try:
        with open(SCADA_FILE, "w") as file:
            json.dump(data, file, indent=4)
            print("SCADA DATA SAVED:", data)
    except IOError:
        print("CHYBA: Data sa neulozili!")

def log_event(user, event):
    if not user:
        user = "UNKNOWN_USER"
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    ip = users.get(user, request.remote_addr)
    log_entry = f"{timestamp} USER: {user} | SCADA SYSTEM | {event} | IP: {ip}\n"
    with open("scada.log", "a") as log_file:
        log_file.write(log_entry)
    print(log_entry.strip())

@app.route("/", methods=["GET", "POST"])
def index():
    global scada_data
    if "user" not in session:
        return redirect(url_for("login_page"))
    user = session["user"]
    scada_data = load_scada_data()
    if request.method == "POST":
        param = request.form.get("parameter")
        new_value = request.form.get("value")
        if param in scada_data and new_value.replace(".", "").isdigit():
            old_value = scada_data[param]
            scada_data[param] = float(new_value)
            save_scada_data(scada_data)
            log_event(user, f"CHANGED PARAMETER: {param.upper()} | OLD VALUE: {old_value} | NEW VALUE: {scada_data[param]}")
            print(f"SCADA DATA UPDATED: {param} = {scada_data[param]}")
        else:
            return "Invalid input", 400
    scada_data = load_scada_data()
    flag_message = ""
    if (
        scada_data.get("water_level") == 15
        and scada_data.get("pressure") == 5
        and scada_data.get("temperature") == 25
    ):
        flag_message = "FLAG{scadasupport}"
    try:
        with open("scada.log", "r") as log_file:
            logs = log_file.readlines()
    except FileNotFoundError:
        logs = ['No logs found.']
    return render_template("index.html", scada_data=scada_data, logs=logs, user=user, flag_message=flag_message)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        user = request.form.get("user")
        if user in users:
            session["user"] = user
            log_event(user, "LOGIN SUCCESS")
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Neplatne uzivatelske meno!")
    return render_template("login.html")

@app.route("/logout")
def logout():
    user = session.get("user", "UNKNOWN_USER")
    log_event(user, "LOGOUT")
    session.pop("user", None)
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

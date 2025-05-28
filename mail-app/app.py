from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Používateľská databáza s novými e-mailmi pre Boba
users = {
    "alice": {"password": "alicepass", "emails": [
        {"id": 1, "odosielatel": "friend@example.com", "predmet": "Hi Alice!", "obsah": "Hello Alice, how are you?"}
    ]},
    "bob": {"password": "bobpass", "emails": [
        {"id": 2, "odosielatel": "microsoft@account.com", "predmet": "Security Alert", "template": "email_microsoft.html", 
         "data": {"FirstName": "Bob", "URL": "https://security.microsoft.com"}},
        {"id": 3, "odosielatel": "dropbox@notifications.com", "predmet": "New Dropbox Document", "template": "email_dropbox.html", 
         "data": {"FirstName": "Bob", "URL": "https://dropbox.com/shared-docs", "Tracker": "Tracking ID: 123456"}}
    ]},
    "john": {"password": "johnpass", "emails": [
        {"id": 4, "odosielatel": "support@service.com", "predmet": "Account Update", "obsah": "Your account was updated successfully."}
    ]}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for("inbox"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def inbox():
    return render_template("inbox.html", maily=users[current_user.id]["emails"])

@app.route("/mail/<int:mail_id>")
@login_required
def mail_detail(mail_id):
    mail = next((m for m in users[current_user.id]["emails"] if m["id"] == mail_id), None)
    if mail:
        if "template" in mail:
            return render_template(mail["template"], **mail["data"])
        return render_template("mail_detail.html", mail=mail)
    return redirect(url_for("inbox"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

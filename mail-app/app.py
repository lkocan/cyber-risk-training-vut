from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

users = {
  "alice": {
    "password": "alicepass",
    "emails": [
      {
        "id": 1,
        "odosielatel": "ava@uward.com",
        "predmet": "Ahoj Alice!",
        "obsah": "Co nove v praci?"
      },
      {
        "id": 2,
        "odosielatel": "kalendar@terravolt.cz",
        "predmet": "Pripomenutie: Stretnutie timu",
        "obsah": """
<p>Nezabudnite na dnesne timove stretnutie v <strong>zasedacke B2</strong> o 14:00.</p>
<p>Tema: Rozdelenie uloh na buduci mesiac.</p>
"""
      },
      {
        "id": 3,
        "odosielatel": "newsletter@slevomat.cz",
        "predmet": "Zlava 60 % na wellness vikend v Tatrach",
        "obsah": """
<p>Uzite si oddych vo Vysokych Tatrach s 60 % zlavou len do nedele!</p>
<p><a href="https://slevomat.cz" onclick="return false;">Zobrazit ponuku</a></p>
<br>
<p>Vas Slevomat.</p>
"""
      },
      {
        "id": 4,
        "odosielatel": "info@ryanair-letenky.cz",
        "predmet": "Jediny sposob cestovania",
        "obsah": """
<h2 style="color:#2980b9;">RYANAIR</h2>
<p>Dobry den Alice,</p>
<p>Uz je to nejaky cas, co ste s nami naposledy leteli. Chybate nam!</p>
<p>Aby sme Vas privitali spat na palube, pripravili sme pre Vas specialne ponuky:</p>
<ul>
  <li>Brno -> Barcelona uz od <strong>59 €</strong></li>
  <li>Vieden -> Pariz uz od <strong>79 €</strong></li>
  <li>Praha -> Londyn uz od <strong>69 €</strong></li>
</ul>
<p><a href="https://ryanair.cz" onclick="return false;" style="color: #2980b9; text-decoration: underline;">Zobrazit vsetky ponuky</a></p>
<p>Tesime sa na vasu dalsiu cestu,<br>Vas tim Ryanair</p>
"""
      },
      {
        "id": 5,
        "odosielatel": "vedenie@terravolt.cz",
        "predmet": "Podakovanie za vasu pracu v 1. kvartali",
        "obsah": """
<p>Vazeni kolegovia,</p>
<p>Chcem vam osobne podakovat za vasu usilovnost a pracu pocas prveho kvartalu tohto roka.</p>
<p>Spolocne sme dosiahli rast o <strong>7 %</strong>, otvorili nove trhy a prekonali vyzvy, ktore pred nami stali.</p>
<p>Verim, ze druhy kvartal bude este uspesnejsi. Dakujem, ze ste sucastou nasho timu.</p>
<p>S podakovanim,<br>Ing. Tomas Malik<br>CEO</p>
"""
      },
      {
        "id": 6,
        "odosielatel": "account@microsoft.com",
        "predmet": "Pripomenutie: Overenie vasej e-mailovej adresy",
        "obsah": """
<p>Dobry den,</p>
<p>Vas ucet Microsoft je pripraveny, no este nebol overeny.</p>
<p>Pre plnohodnotne vyuzitie sluzieb (OneDrive, Office, Teams) potvrdte svoj e-mail kliknutim nizsie:</p>
<p><a href="https://microsoft.com/overenie" onclick="return false;">Overit e-mailovu adresu</a></p>
<p>Tato vyzva vyprsi o 3 dni.</p>
<p>Dakujeme,<br>Tim Microsoft</p>
"""
      },
      {
        "id": 7,
        "odosielatel": "newsletter@alza.cz",
        "predmet": "Zlavy az do 70 % len do nedele!",
        "obsah": """
<h2 style="color:#0392b2;">Mega vypredaj je tu!</h2>
<p>Len do nedele nakupite s mimoriadnymi zlavami az do <strong>70 %</strong>.</p>
<ul>
  <li>Notebooky od 349 $</li>
  <li>Kamerove sety so zlavou 40 %</li>
  <li>Sluchadla s cashbackom</li>
</ul>
<p><a href="https://alza.cz" onclick="return false;">Nakupit teraz</a></p>
"""
      },
      {
        "id": 8,
        "odosielatel": "newsletter@zdravievzivote.sk",
        "predmet": "Tipy na jarny restart tela aj mysle",
        "obsah": """
<h2>Jar v plnom prude - budete fit a v pohode</h2>
<p>V dnesnom vydani:</p>
<ul>
  <li>5 jednoduchych receptov na zdrave obedy</li>
  <li>Ako lepsie spat bez liekov</li>
  <li>Domace cvicenie pre zaciatocnikov</li>
</ul>
<p><a href="https://zdravievzivote.sk" onclick="return false;">Zobrazit clanok</a></p>
<p>Tím Zdravie v zivote</p>
"""
      },
      {
        "id": 9,
        "odosielatel": "vedenie@terravolt.cz",
        "predmet": "Uprava pracovnej doby pocas velkonocnych sviatkov",
        "obsah": """
<p>Mili kolegovia,</p>
<p>Upozornujeme na zmenu otvaracich hodin a dostupnosti kancelarii pocas Velkej noci:</p>
<ul>
  <li><strong>18. 4.</strong> - praca z domu odporucana</li>
</ul>
<p>Dakujeme za pochopenie,<br>HR oddelenie</p>
"""
      },
      {
        "id": 10,
        "odosielatel": "mnovak@terravolt.cz",
        "predmet": "Prezentacia na zajtrajsi meeting",
        "obsah": """
<p>Ahoj Alice,</p>
<p>Posielam ti finalnu verziu prezentacie na zajtrajsi meeting s klientom.</p>
<p>Najdes ju tu: <a href="https://dropbox.com/shared-docs" onclick="return false;">Prezentacia - Finalna verzia</a></p>
<p>Skontroluj si, prosim, este cast s grafom - nie som si isty, ci su tam spravne cisla.</p>
<p>Vdaka,<br>Milan</p>
"""
      },
      {
        "id": 11,
        "odosielatel": "account@microsoft.com",
        "predmet": "Pripomenutie: Overenie vasej e-mailovej adresy",
        "obsah": """
<p>Dobry den,</p>
<p>Vas ucet Microsoft je pripraveny, no este nebol overeny.</p>
<p>Pre plnohodnotne vyuzitie sluzieb (OneDrive, Office, Teams) potvrdte svoj e-mail kliknutim nizsie:</p>
<p><a href="https://microsoft.com/overenie" onclick="return false;">Overit e-mailovu adresu</a></p>
<p>Tato vyzva vyprsi o 1 den.</p>
<p>Dakujeme,<br>Tim Microsoft</p>
"""
      },
      {
        "id": 12,
        "odosielatel": "ava@uward.com",
        "predmet": "Mam plan",
        "obsah": "Mali by sme ist dnes nakupovat."
      },
      {
        "id": 13,
        "odosielatel": "microsoft@support.com",
        "predmet": "Security Alert",
        "obsah": """
<h1 style="color:#4472c4">Microsoft Account</h1>
<p>Dear Bob,</p>
<p>Someone in Bogota, Colombia attempted to log into your account several times.</p>
<p>If you believe this was fraudulent activity, please report it!<br>
<a href="https://microsoft.com" onclick="return false;">here</a>.</p>
<p>If you do not believe this to be fraudulent activity, you may ignore this message.</p>
<br>
<p>Sincerely,</p>
<p>office365@microsoft.com</p>
"""
      },
      {
        "id": 14,
        "odosielatel": "newsletter@slevomat.cz",
        "predmet": "Zlava 60 % na wellness vikend v Tatrach",
        "obsah": """
<p>Uzite si oddych pre dvoch v Nizkych Tatrach s 40 % zlavou len do konca tohto tyzdna!</p>
<p><a href="https://slevomat.cz" onclick="return false;">Zobrazit ponuku</a></p>
<br>
<p>Vas Slevomat.</p>
"""
      },
      {
        "id": 15,
        "odosielatel": "newsletter@datart.cz",
        "predmet": "Zlavy az do 70 % len do nedele!",
        "obsah": """
<h2 style="color:#c0392b;">Super zlavi su tu!</h2>
<p>Len do konca mesiaca nakupite s mimoriadnymi zlavami az do <strong>65 %</strong>.</p>
<ul>
  <li>Notebooky od 319 $</li>
  <li>Domace spotrebice so zlavou 40 %</li>
  <li>Mobilne telefony s cashbackom</li>
</ul>
<p><a href="https://datart.cz" onclick="return false;">Nakupit teraz</a></p>
"""
      }
    ]
  },
  "milan": {
    "password": "novakpass",
    "emails": [
      {
        "id": 16,
        "odosielatel": "microsoft@support.com",
        "predmet": "Security Alert",
        "obsah": """
<h1 style="color:#4472c4">Microsoft Account</h1>
<p>Dear Bob,</p>
<p>Someone in Bogota, Colombia attempted to log into your account several times.</p>
<p>If you believe this was fraudulent activity, please report it!<br>
<a href="https://microsoft.com" onclick="return false;">here</a>.</p>
<p>If you do not believe this to be fraudulent activity, you may ignore this message.</p>
<br>
<p>Sincerely,</p>
<p>office365@microsoft.com</p>
"""
      },
      {
        "id": 17,
        "odosielatel": "dropbox@notifications.com",
        "predmet": "Novy Dropbox dokument",
        "obsah": """
<p><img src="https://brandnew.archives/dropbox_2017_logo.png" style="width: 120px; height: 27px;" alt="Dropbox logo" /></p>
<p>Hi Bob,</p>
<p>You have a new document(s) shared with you via Dropbox.</p>
<p><a href="https://dropbox.com/shared-docs" onclick="return false;">VIEW HERE</a></p>
<br>
<p>Tracking ID: 14623</p>
"""
      },
      {
        "id": 18,
        "odosielatel": "vedenie@terravolt.cz",
        "predmet": "Podakovanie za vasu pracu v 1. kvartali",
        "obsah": """
<p>Vazeni kolegovia,</p>
<p>Chcem vam osobne podakovat za vasu usilovnost a pracu pocas prveho kvartalu tohto roka.</p>
<p>Spolocne sme dosiahli rast o <strong>7 %</strong>, otvorili nove trhy a prekonali vyzvy, ktore pred nami stali.</p>
<p>Verim, ze druhy kvartal bude este uspesnejsi. Dakujem, ze ste sucastou nasho timu.</p>
<p>S podakovanim,<br>Ing. Tomas Malik<br>CEO</p>
"""
      },
      {
        "id": 19,
        "odosielatel": "newsletter@alza.cz",
        "predmet": "Zlavy az do 70 % len do nedele!",
        "obsah": """
<h2 style="color:#0392b2;">Mega vypredaj je tu!</h2>
<p>Len do nedele nakupite s mimoriadnymi zlavami az do <strong>70 %</strong>.</p>
<ul>
  <li>Notebooky od 349 $</li>
  <li>Kamerove sety so zlavou 40 %</li>
  <li>Sluchadla s cashbackom</li>
</ul>
<p><a href="https://alza.cz" onclick="return false;">Nakupit teraz</a></p>
"""
      },
      {
        "id": 20,
        "odosielatel": "jcollins@terravolt.cz",
        "predmet": "Ahoj Milan!",
        "obsah": "Budem trocha meskat do prace."
      },
      {
        "id": 21,
        "odosielatel": "kalendar@terravolt.cz",
        "predmet": "Pripomenutie: Stretnutie timu",
        "obsah": """
<p>Nezabudnite na dnesne timove stretnutie v <strong>zasedacke B2</strong> o 14:00.</p>
<p>Tema: Rozdelenie uloh na buduci mesiac.</p>
          """
      },
      {
        "id": 22,
        "odosielatel": "vedenie@terravolt.cz",
        "predmet": "Uprava pracovnej doby pocas velkonocnych sviatkov",
        "obsah": """
<p>Mili kolegovia,</p>
<p>Upozornujeme na zmenu otvaracich hodin a dostupnosti kancelarii pocas Velkej noci:</p>
<ul>
  <li><strong>18. 4.</strong> - praca z domu odporucana</li>
</ul>
<p>Dakujeme za pochopenie,<br>HR oddelenie</p>
"""
      },
      {
        "id": 23,
        "odosielatel": "info@ryanair-letenky.cz",
        "predmet": "Jediny sposob cestovania",
        "obsah": """
<h2 style="color:#2980b9;">RYANAIR</h2>
<p>Dobry den Milan,</p>
<p>Uz je to nejaky cas, co ste s nami naposledy leteli. Chybate nam!</p>
<p>Aby sme Vas privitali spat na palube, pripravili sme pre Vas specialne ponuky:</p>
<ul>
  <li>Brno -> Barcelona uz od <strong>59 €</strong></li>
  <li>Vieden -> Pariz uz od <strong>79 €</strong></li>
  <li>Praha -> Londyn uz od <strong>69 €</strong></li>
</ul>
<p><a href="https://ryanair.cz" onclick="return false;" style="color: #2980b9; text-decoration: underline;">Zobrazit vsetky ponuky</a></p>
<p>Tesime sa na vasu dalsiu cestu,<br>Vas tim Ryanair</p>
"""
      },
      {
      "id": 24,
      "odosielatel": "dropbox@notifications.com",
      "predmet": "Novy Dropbox dokument",
      "obsah": """
<p><img src="https://www.underconsideration.com/brandnew/archives/dropbox_2017_logo.png" style="width: 120px; height: 27px;" alt="Dropbox logo" /></p>
<p>Hi Bob,</p>
<p>You have a new document(s) shared with you via Dropbox.</p>
<p><a href="https://dropbox.com/shared-docs" onclick="return false;">VIEW HERE</a></p>
<br>
<p>Tracking ID: 17853</p>
"""
    }
    ]},
    "john": {
    "password": "johnpass",
    "emails": [
      {
        "id": 31,
        "odosielatel": "support@service.com",
        "predmet": "Account Update",
        "obsah": "Your account was updated successfully."
      },
      {
        "id": 32,
        "odosielatel": "kalendar@terravolt.cz",
        "predmet": "Pripomenutie: Stretnutie timu",
        "obsah": """
<p>Nezabudnite na dnesne timove stretnutie v <strong>zasedacke B2</strong> o 14:00.</p>
<p>Tema: Rozdelenie uloh na buduci mesiac.</p>
"""
      },
      {
        "id": 33,
        "odosielatel": "vedenie@terravolt.cz",
        "predmet": "Podakovanie za vasu pracu v 1. kvartali",
        "obsah": """
<p>Vazeni kolegovia,</p>
<p>Chcem vam osobne podakovat za vasu usilovnost a pracu pocas prveho kvartalu tohto roka.</p>
<p>Spolocne sme dosiahli rast o <strong>7 %</strong>, otvorili nove trhy a prekonali vyzvy, ktore pred nami stali.</p>
<p>Verim, ze druhy kvartal bude este uspesnejsi. Dakujem, ze ste sucastou nasho timu.</p>
<p>S podakovanim,<br>Ing. Tomas Malik<br>CEO</p>
"""
      },
      {
        "id": 34,
        "odosielatel": "newsletter@alza.cz",
        "predmet": "Zlavy az do 70 % len do nedele!",
        "obsah": """
<h2 style="color:#0392b2;">Mega vypredaj je tu!</h2>
<p>Len do nedele nakupite s mimoriadnymi zlavami az do <strong>70 %</strong>.</p>
<ul>
  <li>Notebooky od 349 $</li>
  <li>Kamerove sety so zlavou 40 %</li>
  <li>Sluchadla s cashbackom</li>
</ul>
<p><a href="https://alza.cz" onclick="return false;">Nakupit teraz</a></p>
"""
      },
      {
        "id": 35,
        "odosielatel": "mnovak@terravolt.cz",
        "predmet": "Dlzis mi pivo",
        "obsah": "Pipol som ti dochadzku."
      },
      {
        "id": 36,
        "odosielatel": "account@microsoft.com",
        "predmet": "Pripomenutie: Overenie vasej e-mailovej adresy",
        "obsah": """
<p>Dobry den,</p>
<p>Vas ucet Microsoft je pripraveny, no este nebol overeny.</p>
<p>Pre plnohodnotne vyuzitie sluzieb (OneDrive, Office, Teams) potvrdte svoj e-mail kliknutim nizsie:</p>
<p><a href="https://microsoft.com/overenie" onclick="return false;">Overit e-mailovu adresu</a></p>
<p>Tato vyzva vyprsi o 3 dni.</p>
<p>Dakujeme,<br>Tim Microsoft</p>
"""
      },
      {
        "id": 37,
        "odosielatel": "info@ryanair-letenky.cz",
        "predmet": "Jediny sposob cestovania",
        "obsah": """
<h2 style="color:#2980b9;">RYANAIR</h2>
<p>Dobry den John,</p>
<p>Uz je to nejaky cas, co ste s nami naposledy leteli. Chybate nam!</p>
<p>Aby sme Vas privitali spat na palube, pripravili sme pre Vas specialne ponuky:</p>
<ul>
  <li>Bratislava -> Barcelona uz od <strong>59 $</strong></li>
  <li>Vieden -> Londyn uz od <strong>79 $</strong></li>
  <li>Brno -> Amsterdam, uz od <strong>69 $</strong></li>
</ul>
<p><a href="https://ryanair.cz" onclick="return false;" style="color: #2980b9; text-decoration: underline;">Zobrazit vsetky ponuky</a></p>
<p>Tesime sa na vasu dalsiu cestu,<br>Vas tim Ryanair</p>
"""
      },
      {
        "id": 38,
        "odosielatel": "dropbox@notifications.com",
        "predmet": "Novy Dropbox dokument",
        "obsah": """
<p><img src="https://www.underconsideration.com/brandnew/archives/dropbox_2017_logo.png" style="width: 120px; height: 27px;" alt="Dropbox logo" /></p>
<p>Hi Bob,</p>
<p>You have a new document(s) shared with you via Dropbox.</p>
<p><a href="https://dropbox.com/shared-docs" onclick="return false;">VIEW HERE</a></p>
<br>
<p>Tracking ID: 15523</p>
"""
      },
      {
        "id": 39,
        "odosielatel": "newsletter@datart.cz",
        "predmet": "Zlavy az do 70 % len do nedele!",
        "obsah": """
<h2 style="color:#0392b2;">Super zlavi su tu!</h2>
<p>Len do konca mesiaca nakupite s mimoriadnymi zlavami az do <strong>65 %</strong>.</p>
<ul>
  <li>Notebooky od 319 $</li>
  <li>Domace spotrebice so zlavou 40 %</li>
  <li>Mobilne telefony s cashbackom</li>
</ul>
<p><a href="https://datart.cz" onclick="return false;">Nakupit teraz</a></p>
"""
      },
      {
        "id": 40,
        "odosielatel": "aktualizacia@scadasupport.cs",
        "predmet": "Nova aktualizacia!",
        "obsah": """
<p>Dobry den,</p>
<p>Mame pre vas novu aktualizaciu systemu.</p>
<p><a href="https://scadasystem.cs/aktualizacia/ransomware.py" onclick="return false;">STIAHNUT</a></p>
<br>
<p>Dakujeme ze vyuzivate nase sluzby,<br>Vas SCADA support tim.</p>
"""
      },
      {
        "id": 41,
        "odosielatel": "newsletter@slevomat.cz",
        "predmet": "Zlava 60 % na wellness vikend v Tatrach",
        "obsah": """
<p>Uzite si oddych pre dvoch v Nizkych Tatrach s 40 % zlavou len do konca tohto tyzdna!</p>
<p><a href="https://slevomat.cz" onclick="return false;">Zobrazit ponuku</a></p>
<br>
<p>Vas Slevomat.</p>
"""
      }
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
    if current_user.id not in users:
        return redirect(url_for("login"))
    return render_template("inbox.html", maily=users[current_user.id].get("emails", []))

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

from flask import Flask, render_template, request, redirect, url_for, session, json
import psycopg2 as dbapi2
from configurations import db_url
from passlib.hash import pbkdf2_sha256 as hasher

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def queryToString(s):
    str1 = ""
    for e in s:
        str1 += e[0]
        str1 += ','
    return str1[:-1]

def queryIntToString(s):
    str1 = ""
    for e in s:
        str1 += str(e[0])
        str1 += ','
    return str1[:-1]

@app.route("/")
def home_page():
    state = "SELECT ALL SONG FROM MUSICS"
    with dbapi2.connect(db_url) as connection:
        cursor = connection.cursor()
        cursor.execute(state)
        songs = cursor.fetchall()
        cursor.close()
    state = "SELECT ALL GENRE FROM MUSICS"
    with dbapi2.connect(db_url) as connection:
        cursor = connection.cursor()
        cursor.execute(state)
        genres = cursor.fetchall()
        cursor.close()

    state = "SELECT ALL SCORE FROM MUSICS"
    with dbapi2.connect(db_url) as connection:
        cursor = connection.cursor()
        cursor.execute(state)
        scores = cursor.fetchall()
        cursor.close()
    return render_template('home.html', songs=queryToString(songs), genres=queryToString(genres), scores=queryIntToString(scores))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        if uname == "":
            return render_template("login.html", alert=0)
        passw = request.form["passw"]
        tup = (uname,)
        state = "SELECT ID, ISADMIN, PASSWORD FROM USERS WHERE USERNAME=%s"
        with dbapi2.connect(db_url) as connection:
            cursor = connection.cursor()
            cursor.execute(state, tup)
            record = cursor.fetchone()
            if record != None:
                if record[1]: # admin
                    if hasher.verify(passw, record[2]):
                        session["is_admin"] = "yes"
                        return redirect(url_for("admin_page"))
                    else: ###################################### hatalı şifre
                        return render_template("login.html", alert = 1)
                else: # user
                    if hasher.verify(passw, record[2]):########## doğru şifre
                        return redirect(url_for("home_page"))
                    else:  ###################################### hatalı şifre
                        return render_template("login.html", alert = 1)
            else: ############################################# wrong username
                return render_template("login.html", alert=1)
    else:
        return render_template("login.html", alert = 0)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        state = "SELECT ID FROM USERS WHERE USERNAME=%s"
        tup = (uname,)
        with dbapi2.connect(db_url) as connection:
            cursor = connection.cursor()
            cursor.execute(state, tup)
            record = cursor.fetchone()
            cursor.close()
        if record == None:
            mail = request.form['mail']
            passw = request.form['passw']
            hashed = hasher.hash(passw)
            state = "INSERT INTO USERS(USERNAME, PASSWORD, MAIL) VALUES(%s, %s, %s) "
            with dbapi2.connect(db_url) as connection:
                cursor = connection.cursor()
                cursor.execute(state, (uname, hashed, mail))
                cursor.close()
        else:
            return render_template("register.html", alert = 1)
        return redirect(url_for("login"))
    return render_template("register.html", alert = 0)

@app.route("/save_leads", methods=["GET", "POST"])
def save_leads():
    result = request.json('x')
    result = json.loads(result)
    print(result)

if __name__ == "__main__":
    app.run()

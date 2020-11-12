from . import app
from flask import render_template, request, redirect, url_for, abort
from flask import session, flash
import functools

"""
>>> import os
>>> os.urandom(24)
"""
app.secret_key = (
    b"\xd0\xf9\xads\x9e\xb2=\xec\xb3\xe7\x06\x84\xbf\xf2\x03s\n\xa0\xba\x8dy\xe0f="
)


def prihlasit(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login", nextpage=request.full_path))

    return wrapper


@app.route("/")
def index():
    pi = 3.141519
    e = 2.7
    title = "Index"
    text = "<h1>Nadpis</h1>"
    return render_template("base.html.j2", pi=pi, title=title, text=text)


@app.route("/info/", methods=["GET"])
def info():
    title = "Info"
    x = request.args.get("x")
    y = request.args.get("y")
    try:
        z = int(x) + int(y)
    except (TypeError, ValueError):
        z = ""
    return render_template("info.html.j2", title=title, z=z)


@app.route("/info/", methods=["POST"])
def info_post():
    jmeno = request.form.get("jmeno")
    heslo = request.form.get("heslo")
    if heslo == "heslo":
        session["user"] = jmeno
    print(jmeno, heslo)
    return redirect(url_for("info"))


@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html.j2")

    elif request.method == "POST":
        jmeno = request.form.get("jmeno")
        heslo = request.form.get("heslo")
        if jmeno and heslo == "heslo":
            session["user"] = jmeno
            flash("Právě jsi se úspěšně přihlásil!", "info")
            nextpage = request.args.get("nextpage")
            if nextpage:
                return redirect(nextpage)
            return redirect(url_for("index"))
        else:
            flash("Nespráné přihlašovací údaje", "error")
            return redirect(url_for("login"))


@app.route("/logout/")
def logout():
    flash("Byl jsi odhlášen!", "info")
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/tajne/")
def tajne():
    if "user" in session:
        return render_template("info.html.j2")
    else:
        flash("Na tuto stránku je třeba se přihlásit!", "error")
        return redirect(url_for("login", nextpage=request.full_path))


@app.route("/kvetak/")
@prihlasit
def kvetak():
    return render_template("kvetak.html.j2")

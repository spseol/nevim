from . import app
from flask import render_template, request, redirect, url_for


@app.route('/')
def index():
    pi=3.141519
    e=2.7
    title = 'Index'
    text = '<h1>Nadpis</h1>'
    return render_template('base.html.j2', pi=pi, title=title, text=text)


@app.route('/info/', methods=['GET'])
def info():
    title = 'Info'
    x = request.args.get('x')
    y = request.args.get('y')
    try:
        z = int(x) + int(y)
    except (TypeError, ValueError) :
        z = ''
    return render_template('info.html.j2', title=title, z=z)
    

@app.route('/info/', methods=['POST'])
def info_post():
    jmeno = request.form.get('jmeno')
    heslo = request.form.get('heslo')
    print(jmeno, heslo)
    return redirect(url_for('info'))

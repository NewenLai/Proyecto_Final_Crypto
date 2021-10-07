from programa import app
from flask import render_template

@app.route("/")
def inicio():
    return "Pagina de inicio"#render_template("inicio.html")
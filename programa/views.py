from programa import app
from flask import render_template
from programa.models import DBManager, Consulta


@app.route("/")
def inicio():
    return "Pagina de inicio"#render_template("inicio.html")

@app.route("/purchase")
def compra():

    actualizar = Consulta.Conversion()
    DBManager.Manager(actualizar[0], actualizar[1][0:10], actualizar[1][11:19],  actualizar[2], actualizar[3], actualizar[4])
    return "Pagina de compra"
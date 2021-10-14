import sqlite3
import requests
from requests.sessions import merge_setting
from programa import app
from flask import render_template, request, redirect, url_for
from programa.models import DBManager, Consulta


@app.route("/")
def inicio():

    Tabla = DBManager.CrearTabla()
    return render_template("inicio.html", obj = Tabla[0], items = Tabla[1])



@app.route("/purchase", methods=["GET", "POST"])
def compra():
    if request.method =="GET":
        return render_template("purchase.html")
    else:
        datos = request.form
        Consultaprecio = Consulta.Conversion(datos)
        DBManager.Manager(Consultaprecio[0], Consultaprecio[1][0:10], Consultaprecio[1][11:19],  Consultaprecio[2], Consultaprecio[3], Consultaprecio[4])
        
        return redirect(url_for("inicio"))


@app.route("/status")
def estado():
    
    return render_template("status.html")
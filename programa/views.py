import requests
from requests.sessions import merge_setting
from programa import app
from flask import render_template, request
from programa.models import DBManager, Consulta


@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/purchase", methods=["GET", "POST"])
def compra():
    if request.method =="GET":
        #FROM = input("Moneda from: ")
        #TO = input("Moneda To: ")
        #Amount = input("Cantidad de {} a invertir: ".format(FROM))

        #Consultaprecio = Consulta.Conversion(TO, Amount, FROM)
        #DBManager.Manager(Consultaprecio[0], Consultaprecio[1][0:10], Consultaprecio[1][11:19],  Consultaprecio[2], Consultaprecio[3], Consultaprecio[4])
        
        return render_template("purchase.html")
    else:
        return ("HOLA QUE ASE")


@app.route("/status")
def estado():
    
    return render_template("status.html")
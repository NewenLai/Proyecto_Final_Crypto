from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sqlite3

from werkzeug.utils import validate_arguments

class ValidationError(Exception):
  pass

class Comprobacion(): #Comprobacion basica de los inputs en el formulario y mensajes de error en caso de no rellenar correctamente los campos
  def __init__(self, datos, ruta_DB):
    self.ruta_DB = ruta_DB

    if datos["From"] == datos["To"]:
      raise ValidationError("No puede usarse la misma moneda en ambos campos")

    try:
      self.cantidad = float(datos["cantidad"])
    except ValueError:
      raise ValidationError("Por favor, introduzca una cantidad valida")
    
    if self.cantidad <=0:
       raise ValidationError("La cantidad debe ser positiva")

    if datos["From"] != "EUR":
      con = sqlite3.connect(self.ruta_DB)
      cur = con.cursor()
      sqlconsulta = "SELECT Cantidad from Portfolio where (Moneda) = ?"
      From = datos["From"]
      cur.execute(sqlconsulta, [From])
      previoFrom = cur.fetchall()
      if float(datos["cantidad"]) > float(previoFrom[0][0]):
        raise ValidationError("No puede vender una cantidad mayor que la que se posee")

class Consulta(): #Funcion de consulta del valor actual de una moneda en COINMARKETCAP
  def Conversion(valor): 
    datos = []
    datos.append(valor["cantidad"])
    datos.append(valor["From"])
    datos.append(valor["To"])
 
    url = " https://pro-api.coinmarketcap.com/v1/tools/price-conversion"

    parameters = {
      'amount':valor["cantidad"],
      'symbol':valor["From"],
      'convert':valor["To"]
      }

    headers =  {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '08fe5141-25d4-42b0-b631-cc484579e920',
    }

    session = Session()
    session.headers.update(headers)

    try:
      response = session.get(url, params=parameters)
      data = json.loads(response.text)
      DiaHora = data["data"]["last_updated"]
      recibido = data["data"]["quote"]["{}".format(datos[2])]["price"]
      unit = float(datos[0])/recibido
      return recibido, DiaHora, datos[0], datos[1], datos[2], unit
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

class DBManager(): #Funcion encargada de llamar y actualizar las bases de datos que usaremos en el programa
  def __init__(self, ruta_DB):
    self.ruta_DB = ruta_DB

  def Manager(self, recibido, Fecha, Hora,invertido, From, To):
    con = sqlite3.connect(self.ruta_DB)
    cur = con.cursor()
    #Establecemos condiciones para distinguir Compra, venta o cambio de divisas
    if From == "EUR" and To != "EUR":
        Concepto = "Compra"
    elif From != "EUR" and To != "EUR":
        Concepto = "Cambio"
    else:
        Concepto = "Venta"

    #Sacamos el precio unitario de la divisa que vamos a comprar
    unit = float(invertido)/recibido

    if Concepto != "Venta":
      recibido = float("{:0.8f}".format(recibido))
    else:
      recibido = float("{:0.2f}".format(recibido))

    #Insertamos en la base de datos el movimiento tras haber aprobado que todo esta correcto previamente
    sql = "INSERT INTO movs VALUES (?,?,?,?,?,?,?,?)"
    cur.execute(sql, (Fecha, Hora, From, To, Concepto, invertido, recibido, unit))

    self.sqlconsulta = "SELECT Cantidad from Portfolio where (Moneda) = ?"
    cur.execute(self.sqlconsulta, [To])
    self.previoTo = cur.fetchall()
    cur.execute(self.sqlconsulta, [From])
    self.previoFrom = cur.fetchall()
    update = "UPDATE Portfolio set Cantidad = ?,Valor = ? where Moneda = ?"

    #Se actualiza el Portfolio del usuario con la cantidad de monedas y su valor tras la transaccion
    if Concepto == "Compra":
      cantidadtotal = self.previoTo[0][0] + recibido
      valor = unit*cantidadtotal
      valor = float("{:0.2f}".format(valor))
      cur.execute(update, (cantidadtotal, valor, To))

      #Aprovechando la operacion actualizamos la cantidad invertida en Euros en la base de datos
      nuevaconsulta = "SELECT EURInvertidos from Inversion"
      cur.execute(nuevaconsulta)
      EURInvested= cur.fetchall()
      EUROSInv = float(invertido) + EURInvested[0][0]
      update = "UPDATE Inversion set EURinvertidos = ? where id = ?"
      cur.execute(update, (EUROSInv, 1))

    elif Concepto =="Venta":
      cantidadtotal = self.previoFrom[0][0] - float(invertido)
      unit = recibido/float(invertido)
      valor = unit*cantidadtotal
      valor = float("{:0.2f}".format(valor))
      cur.execute(update, (cantidadtotal, valor, From))

      #Aprovechando la operacion actualizamos la cantidad recuperada en Euros en la base de datos
      nuevaconsulta = "SELECT EURGanados from Inversion"
      cur.execute(nuevaconsulta)
      EURRetrieved= cur.fetchall()
      EUROSret = float(recibido) + EURRetrieved[0][0]
      update = "UPDATE Inversion set EURGanados = ? where id = ?"
      cur.execute(update, (EUROSret, 1))

    else:
      cantidadtotal = self.previoFrom[0][0] - float(invertido) 
      lista = {"From":"EUR","To": From,"cantidad": 1} #precio de una sola moneda elegida en Euros
      calculaeuros = Consulta.Conversion(lista)
      valor = calculaeuros[5]*cantidadtotal
      valor = float("{:0.2f}".format(valor))
      cur.execute(update, (cantidadtotal, valor, From))

      cantidadtotal = self.previoTo[0][0] + recibido
      lista = {"From":"EUR","To": To,"cantidad": 1} 
      calculaeuros = Consulta.Conversion(lista)
      valor = calculaeuros[5]*cantidadtotal
      valor = float("{:0.8f}".format(valor))
      cur.execute(update, (cantidadtotal, valor, To))
      
    con.commit()
    con.close()

  def CrearTabla(self, holder): #Creamos la tabla de movimientos que se mostrara en la pagina inicial
    con= sqlite3.connect(self.ruta_DB)
    cur = con.cursor()
    cur.execute(holder)

    keys=[]
    for item in cur.description:
        keys.append(item[0])

    movimientos = []
    for registro in cur.fetchall():
        i = 0
        dic={}
        for columna in keys:
            dic[columna] = registro[i]
            i +=1
        movimientos.append(dic)
    return keys, movimientos


  def Updater(self): #Funcion para calcular el valor total de cada una de las monedas que tenemos 
    placeholder = []
    con = sqlite3.connect(self.ruta_DB)
    cur = con.cursor()
    holder = "SELECT Moneda from Portfolio where Cantidad > 0"
    cur.execute(holder)
    Coins = cur.fetchall()
    holder = "SELECT Cantidad from Portfolio where Cantidad > 0"
    cur.execute(holder)
    cantidadMonedas = cur.fetchall()
    loops = 0
    valorcryptos = 0
    
    for item in Coins: #En este loop calculamos el precio de cada moneda que tenemos por unidad y lo multiplicamos por la cantidad de ellas que poseemos
      comprobar = {"From":"EUR","To": item[0],"cantidad": 1}
      placeholder = Consulta.Conversion(comprobar)
      inversionmoneda = float(cantidadMonedas[loops][0])*float(placeholder[5])
      holder = "UPDATE Portfolio set Valor = ? where Moneda = ?"
      cur.execute(holder, (inversionmoneda, item[0]))
      #Tras conseguir el valor de una moneda en concreto lo sumamos al total en una variable
      valorcryptos += inversionmoneda
      loops+=1

    holder = "SELECT EURGanados from Inversion"
    cur.execute(holder)
    ganados = cur.fetchall()
    ganados = ganados[0][0]

    holder = "SELECT EURInvertidos from Inversion"
    cur.execute(holder)
    invertidos = cur.fetchall()
    invertidos = invertidos[0][0]

    saldoeuros = ganados-invertidos
    saldoeuros = float("{:0.2f}".format(saldoeuros))

    saldototal = saldoeuros + valorcryptos
    saldototal = float("{:0.2f}".format(saldototal)) 

    valorcryptos = float("{:0.2f}".format(valorcryptos)) 

    con.commit()
    con.close()

    return invertidos, ganados, saldoeuros, valorcryptos, saldototal
   
  def Symbols(self):
    symbols = [
        {"symbol":"EUR", "selected" : False}, 
        {"symbol":"BTC", "selected" : False},
        {"symbol":"ETH", "selected" : False},
        {"symbol":"ADA", "selected" : False},
        {"symbol":"XRP", "selected" : False},
        {"symbol":"LTC", "selected" : False},
        {"symbol":"BCH", "selected" : False}, 
        {"symbol":"BNB", "selected" : False},
        {"symbol":"USDT", "selected" : False},
        {"symbol":"EOS", "selected" : False},
        {"symbol":"BSV", "selected" : False},
        {"symbol":"XLM", "selected" : False},
        {"symbol":"TRX", "selected" : False}
    ]
    return symbols
  
  def Arranque(self): #Definimos los parametros basicos de la Base de datos si no hay una previa o esta se encuentra vacia
    x =  self.Symbols()
    moneda = [coin["symbol"] for coin in x]
    moneda.remove("EUR")

    con = sqlite3.connect(self.ruta_DB)
    cur = con.cursor()

    holder = "INSERT OR IGNORE INTO Portfolio (Moneda, Cantidad, Valor) VALUES (?, ?, ?)"
    val = [("BTC", 0, 0),("ETH", 0, 0),("ADA", 0, 0),("XRP", 0, 0),("LTC", 0, 0),("BCH", 0, 0),("BNB", 0, 0),("USDT", 0, 0),("EOS", 0, 0),("BSV", 0, 0),("XLM", 0, 0),("TRX", 0, 0)]
    cur.executemany(holder, val)

    holder = "INSERT OR IGNORE INTO Inversion (id, EURInvertidos, EURGanados) VALUES (?, ?, ?)"
    cur.execute(holder, (1,0,0))
    con.commit()
    con.close()




from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sqlite3

class Consulta():
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
      precio = data["data"]["quote"]["{}".format(datos[2])]["price"]
      return precio, DiaHora, datos[0], datos[1], datos[2]
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

class DBManager():
  def Manager(recibido, Fecha, Hora,invertido, From, To):
    con = sqlite3.connect('data/wallet.db')
    cur = con.cursor()

    if From == "EUR" and To != "EUR":
        Concepto = "Compra"
    elif From != "EUR" and To != "EUR":
        Concepto = "Cambio"
    else:
        Concepto = "Venta"

    unit = float(invertido)/recibido

    if Concepto != "Venta":
      recibido = float("{:0.8f}".format(recibido))
    else:
      recibido = float("{:0.2f}".format(recibido))

    sql = "INSERT INTO movs VALUES (?,?,?,?,?,?,?,?)"
    cur.execute(sql, (Fecha, Hora, From, To, Concepto, invertido, recibido, unit))

    dictEur ={"From":"EUR", "cantidad": 1, "To":To}
    valor = Consulta.Conversion(dictEur)
    sqlconsulta = "SELECT Cantidad from Portfolio where (Moneda) = ?"
    cur.execute(sqlconsulta, [To])
    previoTo = cur.fetchall()
    cur.execute(sqlconsulta, [From])
    previoFrom = cur.fetchall()
    update = "UPDATE Portfolio set Cantidad = ?,Valor = ? where Moneda = ?"

    if Concepto == "Compra":
      total = previoTo[0][0] + recibido
      valor = valor[0]*total
      cur.execute(update, (total, valor, To))
      nuevaconsulta = "SELECT EURInvertidos from Inversion"
      cur.execute(nuevaconsulta)
      EURInvested= cur.fetchall()
      EUROSInv = float(invertido) + EURInvested[0][0]
      update = "UPDATE Inversion set EURinvertidos = ? where id = ?"
      cur.execute(update, (EUROSInv, 1))

    elif Concepto =="Venta":
      dictEur ={"From":"EUR", "cantidad": 1, "To":From}
      valor = Consulta.Conversion(dictEur)
      total = previoFrom[0][0] - float(invertido)
      valor = valor[0]*total
      cur.execute(update, (total, valor, From))
      nuevaconsulta = "SELECT EURGanados from Inversion"
      cur.execute(nuevaconsulta)
      EURRetrieved= cur.fetchall()
      EUROSret = float(recibido) + EURRetrieved[0][0]
      update = "UPDATE Inversion set EURGanados = ? where id = ?"
      cur.execute(update, (EUROSret, 1))

    else:
      total = previoTo[0][0] + recibido
      valor = valor[0]*total
      cur.execute(update, (total, valor, To))
      total2 = previoFrom[0][0] - float(invertido)
      dictEur ={"From":"EUR", "cantidad": 1, "To":From}
      valor = Consulta.Conversion(dictEur)
      valor = valor[0]*total2
      cur.execute(update, (total2, valor, From))
    con.commit()
    con.close()

  def CrearTabla():
    con= sqlite3.connect("data/wallet.db")
    cur = con.cursor()
    cur.execute("Select * from movs")

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


  def Updater():
    con = sqlite3.connect('data/wallet.db')
    cur = con.cursor()
    cur.execute("SELECT Moneda from Portfolio where Cantidad > 0")
    Coins = cur.fetchall()
    for item in Coins:
        x = Consulta.Conversion("EUR", 1,"{}".format(item[0]))
        print (x)
    con.commit()
    con.close()
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import sqlite3

class Consulta():
  def Conversion():
    url = " https://pro-api.coinmarketcap.com/v1/tools/price-conversion"
    FROM = input("Moneda from: ")
    TO = input("Moneda To: ")
    Amount = input("Cantidad de {} a invertir: ".format(FROM))

    parameters = {
      'amount':Amount,
      'symbol':FROM,
      'convert':TO
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
      precio = data["data"]["quote"]["{}".format(TO)]["price"]
      print(precio)
      print(DiaHora[0:10])
      print(DiaHora[11:19])
      return precio, DiaHora, Amount, FROM, TO
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

class DBManager():
  def Manager(recibido, fecha, Hora,invertido, From, To):
    con = sqlite3.connect('data/wallet.db')
    cur = con.cursor()

    Precio = float(input("Inserte precio: "))

    if From == "EUR" and To != "EUR":
        Concepto = "Compra"
    elif From != "EUR" and To != "EUR":
        Concepto = "Cambio"
    else:
        Concepto = "Venta"
    sql = "INSERT INTO movs VALUES (?,?,?,?,?,?,?,?)"
    cur.execute(sql, (fecha, Hora, From, To, Concepto, invertido, recibido, Precio))

    update = "UPDATE Portfolio set Cantidad = ?,Total = ? where Moneda = ?"
    cur.execute(update, (recibido, Precio, To))

    con.commit()
    con.close()
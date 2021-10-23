# Registro y compra/venta de criptomonedas

Programa de control de criptomonedas

# Instalación

1.  Instalar los requerimientos con pip

    ```
    pip install -r requirements.txt
    ``` 

2. Crear variables de entorno

    Duplicamos el archivo .env_template, renombramos uno de los archivos como .env y cambiamos en ese archivo FLASK_ENV escogiendo entre Production o Development.

    Ejemplo:
    ```
    FLASK_ENV=development
    ```
3. Crear base de datos

    En la carpeta principal creamos la carpeta "data" y un archivo de base de datos, con el nombre que se quiera y extension .db (aconsejamos wallet.db)

    Usamos las especificaciones de initial.sql para crear las 3 tablas necesarias en el archivo de base de datos

4. config

    Al igual que con el archivo .env duplicamos el archivo config_template y renombramos uno de ellos config.py

    En el archivo, en BASEDATOS introducimos la extension en la que se encuentra la base de datos, y en APIKEY una API key valida

    Ejemplo:
    ```
    BASEDATOS="data/wallet.db"
    APIKEY = "asdg23-sadf2-4524-h3f2-968asfeasd"
    ```



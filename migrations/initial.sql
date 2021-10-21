CREATE TABLE "movs" (
	"Fecha"	TEXT NOT NULL,
	"Hora"	TEXT NOT NULL,
	"From"	TEXT NOT NULL,
	"To"	TEXT NOT NULL,
	"Concepto"	TEXT NOT NULL,
	"Invertido"	REAL NOT NULL,
	"Recibido"	REAL NOT NULL
, "PrecioUnit"	REAL NOT NULL);

CREATE TABLE "Portfolio" (
	"Moneda"	TEXT NOT NULL,
	"Cantidad"	REAL,
	"Valor"	REAL,
	PRIMARY KEY("Moneda")
);

CREATE TABLE "Inversion" (
	"id"	INTEGER NOT NULL,
	"EURInvertidos"	REAL NOT NULL,
	"EURGanados"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)
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
	"Cantidad"	REAL NOT NULL,
	"Valor"	REAL NOT NULL,
	PRIMARY KEY("Moneda")
);

CREATE TABLE "Inversion" (
	"id"	INTEGER,
	"EURInvertidos"	REAL NOT NULL,
	"EURGanados"	REAL NOT NULL
)
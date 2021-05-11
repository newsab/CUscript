import sqlite3

def insertData(table, column, input):
    con = sqlite3.connect('PampDb.db')
    cur = con.cursor()
    cur.execute("INSERT INTO '" + table + "' (" + column + ") VALUES ('" + input + "')")
    con.commit()
    con.close()

def getLatestId(table):
    con = sqlite3.connect('PampDb.db')
    cur = con.cursor()
    cur.execute("SELECT max( measurementId ) FROM Measurement")
    id = cur.fetchone()
    con.commit()
    con.close()
    return id[0]

def checkIfOrganisationExists(table, name):
	con = sqlite3.connect('PampDb.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM " + table + " WHERE name='" + name + "'")
	ob = cur.fetchall()

	if not ob:
		cur.execute("INSERT INTO '" + table + "' (name) VALUES ('" + name + "')")
		con.commit()
		cur.execute("SELECT * FROM " + table + " WHERE name='" + name + "'")
		obj = cur.fetchall()
		corObj = obj[0]
		return corObj
	else:
		obje = ob[0]
		return obje
	con.commit()
	con.close()

def checkIfMeasuringObjectExists(table, name, fk):
	con = sqlite3.connect('PampDb.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM " + table + " WHERE name='" + name + "'")
	ob = cur.fetchall()
	bo = False
	if not ob:
		cur.execute("INSERT INTO '" + table + "' (name, organisationId) VALUES ('" + name + "', '" + str(fk) + "')")
		con.commit()
		cur.execute("SELECT * FROM " + table + " WHERE name='" + name + "'")
		obj = cur.fetchall()
		corObj = obj[0]
		return corObj
	else:
		for row in ob:
			if row[2] == fk:
				bo = True
				return row
		if not bo:
			cur.execute("INSERT INTO '" + table + "' (name, organisationId) VALUES ('" + name + "', '" + str(fk) + "')")
			con.commit()
			cur.execute("SELECT * FROM " + table + " WHERE name='" + name + "' AND organisationId='" + str(fk) + "'")
			obj = cur.fetchall()
			corObj = obj[0]
			return corObj
	con.commit()
	con.close()

def checkIfAntennaExists(table, name, fk):
	con = sqlite3.connect('PampDb.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM " + table + " WHERE name='" + name + "'")
	ob = cur.fetchall()
	bo = False
	if not ob:
		cur.execute("INSERT INTO '" + table + "' (name, measuringObjectId) VALUES ('" + name + "', '" + str(fk) + "')")
		con.commit()
		cur.execute("SELECT * FROM " + table + " WHERE name='" + name + "'")
		obj = cur.fetchall()
		corObj = obj[0]
		return corObj
	else:
		for row in ob:
			if row[2] == fk:
				bo = True
				return row
		if not bo:
			cur.execute("INSERT INTO '" + table + "' (name, measuringObjectId) VALUES ('" + name + "', '" + str(fk) + "')")
			con.commit()
			cur.execute("SELECT * FROM " + table + " WHERE name='" + name  + "' AND measuringObjectId='" + str(fk) + "'")
			obj = cur.fetchall()
			corObj = obj[0]
			return corObj
	con.commit()
	con.close()

def getAllName(table):
	con = sqlite3.connect('PampDb.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM " + table)
	names = cur.fetchall()
	con.commit()
	con.close()
	return names

def getAllWhereNameIs(table, name):
	con = sqlite3.connect('PampDb.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM " + table + " WHERE name like'" + name + "%'")
	ob = cur.fetchall()
	if not ob:
		return ""
	else:
		obje = ob[0]
		return obje
	con.commit()
	con.close()

"""
CREATE TABLE "Organisation" (
	"organisationId"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT
);

CREATE TABLE "MeasuringObject" (
	"measureingObjectId"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT,
	"organisationId"	INTEGER,
	FOREIGN KEY("organisationId") REFERENCES "Organisation"("organisationId")
);

CREATE TABLE "Antenna" (
	"antennaId"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT,
	"measuringObjectId"	INTEGER,
	FOREIGN KEY("measuringObjectId") REFERENCES "MeasuringObject"("measureingObjectId")
);

CREATE TABLE "Measurement" (
	"measurementId"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"time"	TEXT,
	"frequency"	REAL,
	"longitude"	REAL,
	"latitude"	REAL,
	"altitude"	REAL,
	"info"	TEXT,
	"antennaId"	INTEGER,
	FOREIGN KEY("antennaId") REFERENCES "Antenna"("antennaId")
);

CREATE TABLE "MeasurementData" (
	"measurementDataId"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"time"	TEXT,
	"longitude"	REAL,
	"latitude"	REAL,
	"altitude"	REAL,
	"dbValue"	REAL,
	"measurementId"	INTEGER,
	FOREIGN KEY("measurementId") REFERENCES "Measurement"("measurementId")
);
"""
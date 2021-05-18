import sqlite3

def insertData(table, column, input):
	"""
	Takes a parameter of a database table, database column and input value. 
	Open a connection to the database.
	Inserts the given input to the given database column in the given database table.
	Saves and closes the connection.
	"""
	try:
		con = sqlite3.connect('PampDb.db')
		cur = con.cursor()
		cur.execute("INSERT INTO '" + table + "' (" + column + ") VALUES ('" + input + "')")
		con.commit()
		con.close()
	except:
		print('Could not run function insertData from DbController')

def getLatestId(table):
	"""
	Takes a parameter of a database table. 
	Open a connection to the database.
	Asks for the latest added row in database.
	Saves and closes the connection.
	Returns the id of the row.
	"""
	try:
		con = sqlite3.connect('PampDb.db')
		cur = con.cursor()
		cur.execute("SELECT max( measurementId ) FROM Measurement")
		id = cur.fetchone()
		con.commit()
		con.close()
		return id[0]
	except:
		print('Could not run function getLatestId from DbController')

def checkIfOrganisationExists(table, name):
	"""
	Takes a parameter of a database table and a name. 
	Open a connection to the database.
	Selects all rows from given table where the name matches the given name.
	Checks if there is no rows and save the given name if not. 
	Returns an object of the organizations data.
	Saves and closes the connection.
	"""
	try:
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
	except:
		print('Could not run function checkIfOrganisationExists from DbController')

def checkIfMeasuringObjectExists(table, name, fk):
	"""
	Takes a parameter of a database table, a name and a foreign key. 
	Open a connection to the database.
	Selects all rows from given table where the name matches the given name.
	Checks if there is no rows with matching name and save the given name if not the return a object of the measurement object. 
	Otherwise loops through the list of rows to see if any one of the rows has the given foreign key as foreign key. If it does the boolean bo is set to true and a object of the measurement object is returned.
	If the boo is still False the given name will be saved to the given database table with the given foreign key and a object of the measurement object is returned.
	Saves and closes the connection.
	"""
	try:
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
	except:
		print('Could not run function checkIfMeasuringObjectExists from DbController')

def checkIfAntennaExists(table, name, fk):
	"""
	Takes a parameter of a database table, a name and a foreign key. 
	Open a connection to the database.
	Selects all rows from given table where the name matches the given name.
	Checks if there is no rows with matching name and save the given name if not the return a object of the antenna. 
	Otherwise loops through the list of rows to see if any one of the rows has the given foreign key as foreign key. If it does the boolean bo is set to true and a object of the antenna is returned.
	If the boo is still False the given name will be saved to the given database table with the given foreign key and a object of the antenna is returned.
	Saves and closes the connection.
	"""
	try:
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
	except:
		print('Could not run function checkIfAntennaExists from DbController')

def getAllName(table):
	"""
	Takes a parameter of a database table. 
	Open a connection to the database.
	Collects all rows from that table and return as a list.
	Saves and closes the connection.
	"""
	try:
		con = sqlite3.connect('PampDb.db')
		cur = con.cursor()
		cur.execute("SELECT * FROM " + table)
		names = cur.fetchall()
		con.commit()
		con.close()
		return names
	except:
		print('Could not run function getAllName from DbController')

def getAllWhereNameIs(table, name):
	"""
	Takes a parameter of a database table and a name. 
	Open a connection to the database.
	Select the rowa from given table where name matches the given name.
	If no match returns an empty string otherwise returns an object of the matching organization.
	Saves and closes the connection.
	"""
	try:
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
	except:
		print('Could not run function getAllWhereNameIs from DbController')

def getAllWhereNameIs2(table, name, orgName):
	"""
	Takes a parameter of a database table, a name and a organization name. 
	Open a connection to the database.
	Select the row from given table where name matches the given name and the foreign key matches the organisationsId from the organization with the given name.
	If no match returns an empty string otherwise returns an object of the matching organization.
	Saves and closes the connection.
	"""
	try:
		con = sqlite3.connect('PampDb.db')
		cur = con.cursor()
		cur.execute("SELECT * FROM " + table + " WHERE name like'" + name + "%' and organisationId like (SELECT organisationId FROM Organisation WHERE name like '" + orgName + "' )")
		ob = cur.fetchall()
		if not ob:
			return ""
		else:
			obje = ob[0]
			return obje
		con.commit()
		con.close()
	except:
		print('Could not run function getAllWhereNameIs2 from DbController')

def getAllWhereNameIs3(table, name, objectName, orgName):
	"""
	Takes a parameter of a database table, a name, a measuring object name and a organization name. 
	Open a connection to the database.
	Select the row from given table where name matches the given name and the foreign key matches the measuringObjectId from the measuring object with the given name, which foreign key should match the organisationsId from the organization with the given name.
	If no match returns an empty string otherwise returns an object of the matching organization.
	Saves and closes the connection.
	"""
	try:
		con = sqlite3.connect('PampDb.db')
		cur = con.cursor()
		cur.execute("SELECT * FROM " + table + " WHERE name like'" + name + "%' and measuringObjectId like (SELECT measureingObjectId FROM MeasuringObject WHERE name like'" + objectName + "' and organisationId like (SELECT organisationId FROM Organisation WHERE name like '" + orgName + "' ))")
		ob = cur.fetchall()
		if not ob:
			return "Den fanns inte"
		else:
			obje = ob[0]
			return obje
		con.commit()
		con.close()
	except:
		print('Could not run function getAllWhereNameIs3 from DbController')

	

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
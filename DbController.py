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
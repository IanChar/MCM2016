import mysql.connector

REPLACEMENT = -1
STATIC_ATTRS = ["UNITID", "INSTNM", "CITY", "STABBR"]

def readSuitable():
    f = open("suitable.csv")
    toReturn = f.readline().split(',')
    f.close()
    toReturn[-1] = toReturn[-1][:-1]
    return toReturn

def scanIn(filename, dynAttrs, staticAttrs = None):
    f = open(filename, 'r')
    headers = f.readline().split(',')
    headers[0] = "UNITID"

    dynIndex = []
    for a in dynAttrs:
        try:
            dynIndex.append(headers.index(a))
        except ValueError:
            print a, "not found"
    if staticAttrs is not None:
        staticIndex = []
        for a in staticAttrs:
            try:
                staticIndex.append(headers.index(a))
            except ValueError:
                print a, "not found"

    if staticAttrs is not None:
        staticData = []
    dynData = []
    for l in f:
        tmp = l.split(',')
        dynData.append([tmp[a] for a in dynIndex])
        if staticAttrs is not None:
            staticData.append([tmp[a] for a in staticIndex])
    f.close()
    if staticAttrs is not None:
        return dynData, staticData
    else:
        return dynData

def loadLocations(data):
    cnx = mysql.connector.connect(user='usr', password='',
            host='127.0.0.1', database="MCM")
    cursor = cnx.cursor()
    for d in data:
        u_id, name, city, state = d
        # Insert location (fail silently if exists)
        locInsert = ("INSERT IGNORE INTO Location"
                "(city, state)"
                "VALUES (%s, %s)"
                "ON DUPLICATE KEY UPDATE city=city")
        cursor.execute(locInsert, (city, state))
    cnx.commit()
    cursor.close()
    cnx.close()

def loadSchools(data):
    cnx = mysql.connector.connect(user='usr', password='',
            host='127.0.0.1', database="MCM")
    cursor = cnx.cursor()
    for d in data:
        u_id, name, city, state = d
        lookup = ("SELECT loc_id FROM Location WHERE city=%s"
                "AND state=%s")
        cursor.execute(lookup, (city, state))
        loc_id = cursor.fetchone()
        if loc_id is None:
            pass
            print u_id, name, "Location not found"
        else:
            loc_id = loc_id[0]
            insert = ("INSERT INTO School"
                    "(unit_id, name, loc_id)"
                    "VALUES (%s, %s, %s)")
            cursor.execute(insert, (u_id, name, loc_id))
    cnx.commit()
    cursor.close()
    cnx.close()

    
if __name__ == '__main__':
    dyn1, stat = scanIn("CollegeScorecard_Raw_Data/MERGED2008_PP.csv",
            readSuitable(), STATIC_ATTRS) 
    loadSchools(stat)


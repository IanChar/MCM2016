import mysql.connector
from lumina import Lumina

REPLACEMENT = -1.0
STATIC_ATTRS = ["UNITID", "INSTNM", "CITY", "STABBR"]

def convert(x):
    try:
        return float(x)
    except ValueError:
        return REPLACEMENT

def dollarToNum(x):
    return x[1:].replace(",","")

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
        dynData.append([convert(tmp[a]) for a in dynIndex])
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
        locInsert = ("INSERT INTO Location"
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

def loadTimeSlices(data, year):
    cnx = mysql.connector.connect(user='usr', password='',
            host='127.0.0.1', database="MCM")
    cursor = cnx.cursor()
    for d in data:
        tmp_str = ",".join(["%s" for _ in range(39)])
        d.append(year)
        insert = ("INSERT IGNORE INTO TimeSlice"
                "(unit_id, ug, ug_nra, ug_unkn, ug_whitenh, ug_blacknh,"
                " ug_api, ug_aianold, ug_hispold, tuition_in, tuition_out,"
                " tuitfte, inexpfte, d150_l4, yr2cmp, yr2wdr, fyr2cmp,"
                " fyr2wdr, yr3cmp, yr3wdr, yr4cmp, yr4wdr, findep, frstgen,"
                " parms, parhs, parps, indavg, depavg, debtgrad, debtngrad,"
                " debtdep, debtind, debtfem, debtmal, debtfrst, debtnfrst,"
                " repaydebt, year)"
                "VALUES (" + tmp_str + ")")
        cursor.execute(insert, tuple(d))
    cnx.commit()
    cursor.close()
    cnx.close()

def loadDonations(data):
    cnx = mysql.connector.connect(user='usr', password='',
            host='127.0.0.1', database="MCM")
    cursor = cnx.cursor()
    for d in data:
        print d
        lookup = ("SELECT unit_id, loc_id FROM School WHERE name=%s")
        cursor.execute(lookup, tuple([d[0]]))
        res = cursor.fetchone()
        if res is None:
            print d[0], "not found."
        else:
            insert = ("INSERT INTO Donation"
                    "(unit_id, loc_id, start_year, end_year, amount)"
                    "VALUES (%s,%s,%s,%s,%s)")
            params = (res[0], res[1], d[4], d[5], dollarToNum(d[2]))
            cursor.execute(insert, map(str, params))
    cnx.commit()
    cursor.close()
    cnx.close()

def loadAll():
    dyn, stat = scanIn("CollegeScorecard_Raw_Data/MERGED2013_PP.csv",
            readSuitable(), STATIC_ATTRS) 
    loadLocations(stat)
    loadSchools(stat)
    l = Lumina()
    loadDonations(l.findGrants())

    loadTimeSlices(dyn, 2013)
    for yr in range(1996, 2013):
         dyn, stat = scanIn("CollegeScorecard_Raw_Data/MERGED" + str(yr) 
                + "_PP.csv", readSuitable()) 
    

    
if __name__ == '__main__':
    dyn, stat = scanIn("CollegeScorecard_Raw_Data/MERGED2013_PP.csv",
            readSuitable(), STATIC_ATTRS) 
    # loadLocations(stat)
    # loadSchools(stat)
    # loadTimeSlices(dyn, 2008)
    l = Lumina()
    loadDonations(l.findGrants())


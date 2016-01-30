import mysql.connector

USERNAME = 'usr'
PASSWORD = ''
GRAD_2YR = 13
GRAD_3YR = 17
GRAD_4YR = 19

def getDonatedSchools(yearRange = 5):
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD,
            host="127.0.0.1", database="MCM")
    cursor = cnx.cursor()
    query = ("SELECT name, min(start_year), amount"
            " FROM School NATURAL JOIN Donation"
             " GROUP BY name")
    cursor.execute(query)
    schools = [(name, yr, amount) for name, yr, amount in cursor]
    res = {}
    for s in schools:
        query = ("SELECT * FROM TimeSlice NATURAL JOIN"
                " (SELECT * FROM School WHERE name=%s) AS skoo"
                " WHERE year > %s and year <= %s"
                " ORDER BY year")
        cursor.execute(query, (s[0], s[1], s[1] + yearRange))
        finList = []
        for c in cursor:
            finList.append(list(c)[2:-2])
        res[str(s[0])] = (amount, finList)
    cursor.close()
    cnx.close()
    return res

if __name__ == '__main__':
    res = getDonatedSchools()
    print map(lambda x: x[GRAD_4YR], res['Harvard University'][1])

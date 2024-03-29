import mysql.connector
import regression

USERNAME = 'usr'
PASSWORD = ''

# COEFS FOR DONATED SCHOOLS ONLYYYYYY
GRAD_2YR = 27 # Financially Dep Students
GRAD_3YR = 23 # Parents with middle school
GRAD_4YR = 24 # Parents with high school
FIRST_GEN = 22

def getDonatedSchools(yearRange = 5):
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD,
            host="127.0.0.1", database="MCM")
    cursor = cnx.cursor()
    query = ("SELECT name, min(start_year), amount"
            " FROM School NATURAL JOIN Donation"
             " GROUP BY name")
    cursor.execute(query)
    schools = [(name, yr, amount) for name, yr, amount in cursor]
    #print schools
    res = {}
    for s in schools:
        query = ("SELECT * FROM TimeSlice NATURAL JOIN"
                " (SELECT * FROM School WHERE name=%s) AS skoo"
                " WHERE year >= %s and year <= %s"
                " ORDER BY year")
        cursor.execute(query, (s[0], s[1], s[1] + yearRange))
        finList = []
        for c in cursor:
            finList.append(list(c)[2:-2])
        res[str(s[0])] = (s[2], finList)
    cursor.close()
    cnx.close()
    return res

def getAllRecent():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD,
            host="127.0.0.1", database="MCM")
    cursor = cnx.cursor()
    query = ("SELECT * FROM School NATURAL JOIN"
            " (SELECT * FROM TimeSlice WHERE year=2013) AS time")
    cursor.execute(query)
    res = {}
    for c in cursor:
        res[c[1]] = c[4:-1]
    cursor.close()
    cnx.close()
    return res

def getSummarySheet(data, extensive = False, year=2013):
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD,
            host="127.0.0.1", database="MCM")
    cursor = cnx.cursor()
    if extensive:
        query = ("SELECT * FROM"
                " (SELECT * FROM School NATURAL JOIN Location) AS A"
                " NATURAL JOIN (SELECT * FROM TimeSlice WHERE year=%s) AS B")
        cursor.execute(query, tuple([year]))
    else:
        query = ("SELECT * FROM School NATURAL JOIN Location")
        cursor.execute(query)
    res = []
    for c in cursor:
        res.append(c)
    rankCount = 1
    for d in data:
        dbInfo = 0
        for r in res:
            if r[2] == d[0]:
                dbInfo = r
                break
        print "------------------------------------------------"
        print "Name:", str(dbInfo[2])
        print "Rank:", rankCount
        rankCount += 1
        print "Score:", d[1]
        print "Location:", ", ".join(map(str, dbInfo[3:5]))
        if extensive:
            print "Year:", year
            printCounter = 6
            for msg in MESSAGES:
                print msg, dbInfo[printCounter]
                printCounter += 1
    print "------------------------------------------------"

MESSAGES = ["Undergraduates:", "Undergraduate (non-resident aliens:",
         "Undergraduates (unknown race):", "White Undergraduates:",
        "Black Undergraduates:", "Asian Undergraduates:",
        "Native American Undergraduates:",
        "Hispanic Undergraduates:", "In-state Tuition:",
        "Out-of-state Tuition:", 
        "Net Tuition Revenue (per student):",
        "Instructional Expenditures (per student):",
        "Adjusted Cohort Count Completion Rate:",
        "Percent Completed in 2 Years:",
        "Percent Withdrawn after 2 Years:",
        "Percent Completed in 2 Years (Female):",
        "Percent Withdrawn after 2 Years (Female):",
        "Percent Completed in 3 Years:",
        "Percent Withdrawn after 3 Years:",
        "Percent Completed in 4 Years:",
        "Percent Withdrawn after 4 Years:",
        "Percent Financially Dependent:",
        "Percent of First-Generation Students:",
        "Percent of Parents With Middle School (highest degree):",
        "Percent of Parents with High School (highest degree):",
        "Percent of Parents with Post-Secondary:",
        "Avg Family Income of Dependents:",
        "Avg Family Income of Independents:",
        "Median Debt of Students who Graduated:",
        "Median Debt of Students who Didn't Graduate:",
        "Median Debt of Dependent Students:",
        "Median Debt of Independent Students:",
        "Median Debt of Female Students:",
        "Median Debt of Male Students:",
        "Median Debt of First Generation Students:",
        "Median Debt of Non-first Generation Students:"]

if __name__ == '__main__':
    reg = regression.Regression(getDonatedSchools())
    judge = lambda x: float(x[2]) + float(x[3]) + float(x[4]) - float(x[1])/10
    getSummarySheet(reg.rankWinners(judge)[:5], True)

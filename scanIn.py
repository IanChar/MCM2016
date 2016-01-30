from mysql.connector import connection

STATIC_ATTRS = ["UNITID", "OPEID", "INSTNM", "CITY", "STABBR", "LOCALE"]
def readSuitable():
    f = open("suitable.csv")
    toReturn = f.readline().split(',')
    f.close()
    return toReturn

def scanIn(filename, dynAttrs, staticAttrs = None):
    f = open(filename, 'r')
    headers = f.readline().split(',')

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

if __name__ == '__main__':
    dyn1, stat = scanIn("CollegeScorecard_Raw_Data/MERGED2008_PP.csv",
            readSuitable(), STATIC_ATTRS)
    tmp = []
    for r in dyn1:
        for c in r:
            try:
                tmp.append(float(c))
            except:
                pass
    print tmp


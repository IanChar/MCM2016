# Reads in data returns (attrNames, rowData)
def scanInData(filename, rows=1000):
    f = open(filename, 'r')
   
    # Find attribute names
    attr = f.readline().split(',')
    attr[0] = "UID"

    # Find row data
    data = []
    for _ in xrange(rows):
        data.append(f.readline().split(','))

    return (attr, data)

# Decides which columns not good for RPCA and gives index of attr
def findSuitable(data, tolerance = 0.5):
    suitable = []

    # Helper function to cast data to float
    def floatGen(index):
        def castToFloat(elem):
            try:
                toReturn = float(elem[index])
            except ValueError:
                toReturn = 0
            return toReturn
        return castToFloat

    for index in range(len(data[0])):
        col = map(floatGen(index), data)
        count = 0
        for n in col:
            if n == 0 or n == 1:
                count += 1
        if count/float(len(col)) < tolerance:
            suitable.append(index)

    return suitable

if __name__=='__main__':
    attr, data = scanInData('CollegeScorecard_Raw_Data/cohorts.csv', 1000)
    suitable = findSuitable(data)
    results = [attr[s] for s in suitable]
    print ", ".join(results)

class AttributeDictionary(object):
    def __init__(self, dicPath):
        f = open(dicPath, 'r')
        self.dictionary = {}
        for l in f:
            tmp = l.split(',')
            # If string is not empty
            if len(tmp) >= 5 and not not tmp[4]:
                self.dictionary[tmp[4]] = tmp[0]
        
    def decode(self, key):
        return self.dictionary[key]


if __name__ == '__main__':
    ad = AttributeDictionary("CollegeScorecard_Raw_Data/dataDictionary.csv")
    print ad.decode("UNITID")

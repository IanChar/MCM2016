import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class Regression:

    def __init__(self, d):
        self.data = d

    def performRegression(self):
        coeffDictionary = {}
        dictionary = self.data.items()
        for item in dictionary:
            newKey = item[0]
            newAmount = np.asarray(item[1][0])
            newValue = np.asarray([x for x in item[1][1] if x[1] != -1])

            coeffDictionary[item[0]] = (newAmount, self.reg(newValue[:,0], newValue[:, 1]))



    def reg(self, X, Y):
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        return slope

    def constructMatrix(self):
        

if __name__ == "__main__":
    R = Regression({'School1': (10000, [[2000, 92], [2001, 92], [2002, 93], [2003, 94], [2004, 95], [2005, 96]]),
                    'School2': (2000, [[2000, 13], [2001, 35], [2002, 15], [2003, 16], [2004, 20], [2005, 30]]),
                    'School3': (3000, [[2003, 123], [2004, 155], [2005, 12], [2006, 94], [2007, 54], [2008, 72]]),
                    'School4': (5000, [[2000, -1], [2001, -1], [2002, -1], [2003, 92], [2004, 95], [2005, -1]]),
                    'School5': (9000, [[2000, 14], [2001, 92], [2002, 93], [2003, 94], [2004, 95], [2005, 96]]),
                    })
    print R.performRegression()

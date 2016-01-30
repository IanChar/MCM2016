import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import QueryDB as q

class Regression:

    def __init__(self, d):
        self.data = d

    def performRegression(self):

        dictionary = self.data.items()
        donations = []

        for item in dictionary:
            name = item[0]
            amount = int(item[1][0])

            del item[1][1][0]

            for year in item[1][1]:
                year[-1] = int(year[-1])

            twoYear = [x for x in item[1][1] if x[q.GRAD_2YR] != -1]
            threeYear = [x for x in item[1][1] if x[q.GRAD_3YR] != -1]
            fourYear = [x for x in item[1][1] if x[q.GRAD_4YR] != -1]

            twoYearCoeff = None
            threeYearCoeff = None
            fourYearCoeff = None

            if len(twoYear) >= 3:
                X = map(lambda x: x[-1], twoYear)
                Y = map(lambda x: x[q.GRAD_2YR], twoYear)
                twoYearCoeff = self.reg(X, Y)

            if len(twoYear) >= 3:
                X = map(lambda x: x[-1], twoYear)
                Y = map(lambda x: x[q.GRAD_3YR], twoYear)
                threeYearCoeff = self.reg(X, Y)

            if len(twoYear) >= 3:
                X = map(lambda x: x[-1], twoYear)
                Y = map(lambda x: x[q.GRAD_4YR], twoYear)
                fourYearCoeff = self.reg(X, Y)

            if twoYearCoeff is not None and threeYearCoeff is not None and fourYearCoeff is not None:
                donations.append([name, amount, twoYearCoeff, threeYearCoeff, fourYearCoeff])

        self.constructMatrix(donations)

    def reg(self, X, Y):
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        return slope

    def constructMatrix(self, donations):
        donationDict = {}
        count = 0
        matrix = []

        for donation in donations:
            self.data[donation[0]][1][0].pop()
            rowInMatrix = self.data[donation[0]][1][0] + donation[2:5]
            #donationDict[donation[0]] =
            matrix.append(rowInMatrix)
            matrix.append
            donationDict[donation[0]] = (count, )

            count = count + 1
if __name__ == "__main__":

    R = Regression(q.getDonatedSchools())
    R.performRegression()

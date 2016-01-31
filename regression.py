import numpy as np
import matplotlib.pyplot as plt
import QueryDB as q
import scipy.io as sio
import json
import findInDict as fd
import sklearn.datasets as d
import sklearn.cluster as s

from scipy import stats

COVER = 0.0

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
            firstGen = [x for x in item[1][1] if x[q.FIRST_GEN] != -1]

            twoYearCoeff = None
            threeYearCoeff = None
            fourYearCoeff = None
            firstGenCoeff = None

            if len(twoYear) >= 3:
                X = map(lambda x: x[-1], twoYear)
                Y = map(lambda x: x[q.GRAD_2YR], twoYear)
                twoYearCoeff = self.reg(X, Y)

            if len(threeYear) >= 3:
                X = map(lambda x: x[-1], threeYear)
                Y = map(lambda x: x[q.GRAD_3YR], threeYear)
                threeYearCoeff = self.reg(X, Y)

            if len(fourYear) >= 3:
                X = map(lambda x: x[-1], fourYear)
                Y = map(lambda x: x[q.GRAD_4YR], fourYear)
                fourYearCoeff = self.reg(X, Y)

            if len(firstGen) >= 3:
                X = map(lambda x: x[-1], firstGen)
                Y = map(lambda x: x[q.FIRST_GEN], firstGen)
                firstGenCoeff = self.reg(X, Y)

            if twoYearCoeff is not None and threeYearCoeff is not None and fourYearCoeff is not None and firstGenCoeff:
                donations.append([name, amount, twoYearCoeff, threeYearCoeff, fourYearCoeff, firstGenCoeff])

        return self.constructMatrix(donations)

    def reg(self, X, Y):
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        return slope

    def constructMatrix(self, donations):
        fullDict = q.getAllRecent()
        donationDict = {}
        donationDictReverse = {}
        count = 0
        checked = []
        m = []
        spectralm = []

        for donation in donations:
            self.data[donation[0]][1][0].pop()
            pastGrantYear = self.data[donation[0]][1][0] + donation[1:6]
            currentYear = list(fullDict[donation[0]]) + [COVER, COVER, COVER, COVER, COVER]

            m.append(pastGrantYear)
            m.append(currentYear)
            spectralm.append(self.data[donation[0]][1][0])
            spectralm.append(list(fullDict[donation[0]]))

            donationDictReverse[count] = donation[0]
            donationDictReverse[count + 1] = donation[0]
            donationDict[donation[0]] = (count, count + 1)
            checked.append(donation[0])
            count = count + 2


        for key, value in fullDict.items():
            if key not in set(checked):
                m.append(list(value) + [COVER, COVER, COVER, COVER, COVER])
                spectralm.append(list(value))
                donationDict[key] = (count)
                donationDictReverse[count] = key
                count = count + 1

        np.savetxt("test.csv", np.matrix(m), delimiter=",")
        sio.savemat('data.mat', {'a_dict': np.matrix(m)})
        with open('dict.json', 'w') as fp:
            json.dump(donationDict, fp)
        with open('dictReverse.json', 'w') as fp:
            json.dump(donationDictReverse, fp)


        return spectralm

    def findData(self):

        text_file = open("NewPredictedData.mat", "r")
        totalCoeff = []
        ranking = []
        count = 0

        


        m = [line.rstrip('\n').split(",") for line in text_file]

        for coeff in m:
            total = float(coeff[1]) + float(coeff[2]) + \
                    float(coeff[3]) + 3 * float(coeff[4])
            totalCoeff.append(total)

        amount = map(lambda x: x[0], m)
        twoYearCoeff = map(lambda x: x[1], m)
        threeYearCoeff = map(lambda x: x[2], m)
        fourYearCoeff = map(lambda x: x[3], m)
        firstGenCoeff = map(lambda x: x[4], m)

        text_file.close()

        for i, score in enumerate(firstGenCoeff):
            ranking.append((fd.findRow(str(i)), float(score), amount[i]))

        ranking = sorted(ranking, key=lambda school: school[1])

        for i in reversed(ranking):
            if count <= 100:
                print i
                count = count + 1

    def spectralClustering(self):
        S = s.SpectralClustering(n_clusters=2, gamma=1.0, \
                            affinity='rbf', n_neighbors=10, assign_labels='kmeans')

        mat = self.performRegression()
        mat = np.asmatrix(mat)
        #print np.size(mat[:, [35, 36]])

        X, test = d.make_circles(10000)
        print np.size(X)
        S.fit(X)
        print S.fit_predict(X)

if __name__ == "__main__":

    R = Regression(q.getDonatedSchools())
    R.findData()
    #R.spectralClustering()

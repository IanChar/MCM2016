from lxml import html
import requests
from itertools import chain, izip


class Lumina:

    def __init__(self):
        self.acc = []
        self.acc2 = []

    def findGrants(self):
        for i in range(1,29):
            page = requests.get('https://www.luminafoundation.org/grants-database/search/?q=university&pg=' + str(i))
            tree = html.fromstring(page.content)
            #This will create a list of buyers:
            grantInfo = tree.xpath('//div[@class="grant-detail"]/strong/text()')
            grantName = tree.xpath('//div[@class="grant-item clearfix"]/h1/a/text()')

            for i, x in enumerate(range(0, len(grantInfo), 4)):
                self.acc = self.acc + [[str(grantName[i])] + grantInfo[x:x+4]]

            for item in self.acc:
                item = item[0:4] + self.findYears(item[4])
                self.acc2.append(item)

        return self.acc2

    def findYears(self, item):
        item = item.replace("/", " ")
        item = item.split()
        return [item[2], item[6]]

if __name__ == '__main__':
    L = Lumina()
    print L.findGrants()

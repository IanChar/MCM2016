import json

with open('dict.json') as data_file:
    data = json.load(data_file)

with open('dictReverse.json') as data_file:
    dataReverse = json.load(data_file)

def findRow(rowNum):
    return dataReverse[rowNum]

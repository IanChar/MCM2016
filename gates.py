from lxml import html
import requests

page = requests.get('http://www.gatesfoundation.org/How-We-Work/Quick-Links/Grants-Database#q/k=university&program=US%20Program')
tree = html.fromstring(page.content)

#This will create a list of buyers:
buyers = tree.xpath('//a')

print 'Buyers: ', buyers

from lxml import html
import requests

page = requests.get('https://www.luminafoundation.org/grants-database/search/?q=university')
tree = html.fromstring(page.content)
print tree.text_content()
#This will create a list of buyers:
buyers = tree.xpath('//div[@class="grant-detail"]/strong/text()')

print 'Buyers: ', buyers

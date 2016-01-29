from requests import Session

session = Session()

# HEAD requests ask for *just* the headers, which is all you need to grab the
# session cookie
session.head('http://www.gatesfoundation.org/How-We-Work/Quick-Links/Grants-Database')

response = session.post(
    url='http://www.gatesfoundation.org/services/gfo/search.ashx',
    data={
        'N': '4294966750',
        'form-trigger': 'moreId',
        'moreId': '156#327',
        'pageType': 'EventClass'
    },
    headers={
        'Referer': 'http://www.gatesfoundation.org/How-We-Work/Quick-Links/Grants-Database'
    }
)

print response.text

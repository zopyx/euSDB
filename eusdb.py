import requests


CAS_QUERY = 'https://www.eusdb.de/api/1.1/search/?cas={cas}'
EUSDB_TOKEN = '1f3fc0231796424d85524d11d28424fd'

SIGNAL_WORDS = {
    'Dgr': 'GEFAHR'
}

def query(cas_no):


    url = CAS_QUERY.format(cas=cas_no.strip())
    headers = {
            'accept': 'application/json',
            'authorization': 'Token {token}'.format(token=EUSDB_TOKEN)
    }
    print(url)
    result = requests.get(url, headers=headers)
    if result.status_code != 200:
        raise ValueError('Unknown CAS number: {}'.format(cas_no))

    data = result.json()
    if data['count'] == 0:
        return None

    detail_url = data['results'][0]['url']
    detail_result = requests.get(detail_url, headers=headers)
    if detail_result.status_code != 200:
        raise ValueError('Detail URL {} returned with error {}'.format(detail_url, detail_result.status_code))
    detail_data = detail_result.json()

    cas_data = dict()
    cas_data['cas_no'] = cas_no 
    cas_data['names'] = set([r['name'] for r in data['results']])

    ghs_pictograms = detail_data['ghs_pictograms'].split(',')
    ghs_pictograms = [ghs.strip() for ghs in ghs_pictograms]
    ghs_pictograms = [ghs for ghs in ghs_pictograms if ghs.startswith('GHS')]
    cas_data['ghs'] = ghs_pictograms

    h_phrases = detail_data['h_phrases'].split(';')
    h_phrases = [h.strip() for h in h_phrases]
    h_phrases = [h for h in h_phrases if h.startswith('H')]
    cas_data['h_phrases'] = h_phrases

    cas_data['signalword'] = SIGNAL_WORDS[detail_data['signalword']]
    return cas_data

if __name__ == '__main__':
    import pprint
    pprint.pprint( query('67-64-1'))
    pprint.pprint(query('7631-99-4'))
    pprint.pprint(query('7440-66-6'))
#    print query('75-36-5')
#    print query('143-33-9')
#    print query('96-33-3')
#    print query('98-86-2')
#    print query('108-88-3')
#    print query('50-00-0')

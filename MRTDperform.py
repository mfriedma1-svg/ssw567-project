import time
import MRTD
import json

time.perf_counter()

with open('records_decoded.json', 'r') as file:
    data = json.load(file)

for record in data['records_decoded']:
    info = {}

    # line 1
    info['document_code'] = 'P<'
    info['country'] = record['line1'['issuing_country']]
    info['lastname'] = record['line1'['last_name']]
    info['name'] = record['line1'['given_name']]

    # line 2
    info['birthdate'] = record['line2'['birth_date']]
    info['nationality'] = record['line2'['country_code']]
    info['passnumber'] = record['line2'['passport_number']]
    info['sex'] = record['line2'['sex']]
    info['expiredate'] = record['line2'['expiration_date']]
    info['personalnumber'] = record['line2'['personal_number']]
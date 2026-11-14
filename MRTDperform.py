import time
import MRTD
import MTTDtest
import json

with open('records_decoded.json', 'r') as file:
    data = json.load(file)

def perform(data, is_test):
    start = time.perf_counter()
    counter = 1
    times = []
    for record in data['records_decoded']:
        info = {}

        # line 1
        info['document_code'] = 'P<'
        info['country'] = record['line1']['issuing_country']
        info['lastname'] = record['line1']['last_name']
        info['name'] = record['line1']['given_name']

        # line 2
        info['birthdate'] = record['line2']['birth_date']
        info['nationality'] = record['line2']['country_code']
        info['passnumber'] = record['line2']['passport_number']
        info['sex'] = record['line2']['sex']
        info['expiredate'] = record['line2']['expiration_date']
        info['personalnumber'] = record['line2']['personal_number']

        # the good part
        if is_test == True:
            # test stuff
            pass
        else:
            line1, line2 = MRTD.encode(info)
            result = line1 + ";" + line2

        if(counter == 100 or (counter % 1000 == 0)):
            end = time.perf_counter()
            time_elapsed = end - start
            times.append(time_elapsed)
        counter += 1
    return times

times = perform(data, False)
times_test = perform(data, True)
counters = [100, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
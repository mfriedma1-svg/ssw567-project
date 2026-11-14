import time
import MRTD
import MTTDtest
import json

with open('records_decoded.json', 'r') as file:
    data_en = json.load(file)

with open('records_encoded.json', 'r') as file:
    data_de = json.load(file)

def perform(is_test, data1 = data_en, data2 = data_de):
    start = time.perf_counter()
    counter = 1
    times = []
    line_count = 2
    lines = []
    for record in data1['records_decoded']:
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
        line1, line2 = MRTD.encode(info)
        result = line1 + ";" + line2
        if is_test == True:
            assert len(line1) == 44
            assert len(line2) == 44
            assert result == data2['records_encoded'][counter-1]

        line_count += 15
        if(counter == 10000):
            line_count += 2
        if(counter == 100 or (counter % 1000 == 0)):
            end = time.perf_counter()
            time_elapsed = end - start
            times.append(time_elapsed)
            lines.append(line_count)
        counter += 1
    return times, lines

times, lines = perform(False)
times_test, lines = perform(True)
counters = [100, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

# csv creation goes here


# modified function for the table
def perform_chart(is_test, type, count, data1 = data_en, data2 = data_de):
    start = time.perf_counter()
    counter = 1
    if type == "encode":
        for record in data1['records_decoded']:
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

            line1, line2 = MRTD.encode(info)
            result = line1 + ";" + line2
            if is_test == True:
                assert len(line1) == 44
                assert len(line2) == 44
                assert result == data2['records_encoded'][counter-1]

            if(counter == count):
                end = time.perf_counter()
                time_elapsed = end - start
                return (time_elapsed / count)
            counter += 1

    elif type == "decode":
        for record in data2['records_encoded']:
            lines = record.split(";")

            info, checkdigits = MRTD.decode(lines[0], lines[1])
            if is_test == True:
                assert info['country'] == data1['records_decoded'][counter-1]['line1']['issuing_country']
                assert info['lastname'] == data1['records_decoded'][counter-1]['line1']['last_name']
                assert info['name'] == data1['records_decoded'][counter-1]['line1']['given_name']
                assert info['birthdate'] == data1['records_decoded'][counter-1]['line2']['birth_date']
                assert info['nationality'] == data1['records_decoded'][counter-1]['line2']['country_code']
                assert info['passnumber'] == data1['records_decoded'][counter-1]['line2']['passport_number']
                assert info['sex'] == data1['records_decoded'][counter-1]['line2']['sex']
                assert info['expiredate'] == data1['records_decoded'][counter-1]['line2']['expiration_date']
                assert info['personalnumber'] == data1['records_decoded'][counter-1]['line2']['personal_number']

            if(counter == count):
                end = time.perf_counter()
                time_elapsed = end - start
                return (time_elapsed / count)
            counter += 1

# table part
inputs = [10, 100, 1000, 10000]
for i in inputs:
    a = perform_chart(True, "encode", i)
    b = perform_chart(False, "encode", i)
    c = perform_chart(True, "decode", i)
    d = perform_chart(False, "decode", i)
    result = [a, b, c, d]
    print(result)
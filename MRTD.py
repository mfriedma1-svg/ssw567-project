def scanMRZ():
    pass

def decode(s1, s2):
    info = {
        "type": "a",
        "country": "b",
        "lastname": "c",
        "name": "d",
        "passnumber": "e",
        "birthdate": "f",
        "sex": "g",
        "expirdate": "h",
        "personalnumber": "i"
    }
    # first string
    info["type"] = s1[0]
    info["country"] = s1[2:5]

    # second string
    info["passnumber"] = s2[0:9]
    info["birthdate"] = s2[13:19]
    info["sex"] = s2[20]
    info["expirdate"] = s2[21:27]
    info["personalnumber"] = s2[28:37]
    checks = [info["passnumber"], info["birthdate"], info["expirdate"], info["personalnumber"]]
    checkdigits = [s2[9], s2[19], s2[27], s2[43]]

    reportMismatch(checks, checkdigits)
    return info

def encode(f1, f2):
    pass

def reportMismatch(checks, checkdigits):
    new_checks = []
    # convert all checks to lists of numbers
    for check in checks:
        new_check = []
        for char in check:
            if char.isnumeric() == False:
                char = (ord(char) - 64)
            new_check.append(char)
        new_check.append(new_check)

    new_checkdigits = []
    # run the luhn algorithm
    for check in new_checks:
        sum = 0
        for number in check:
            if number < 10:
                sum += number
            else:
                sum += ((number // 10) + (number % 10))
        new_checkdigits.append(sum % 10)

    # compare each provided digit to the calculated one
    i = 0
    for digit in checkdigits:
        if digit != new_checkdigits[i]:
            print(f"Mismatch found! Expected {checkdigits[i]} but calculated {new_checkdigits[i]}")
        i += 1
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
        "expiredate": "h",
        "personalnumber": "i"
    }
    # first string
    info["type"] = s1[0]
    info["country"] = s1[2:5]

    # second string
    info["passnumber"] = s2[0:9]
    info["birthdate"] = s2[13:19]
    info["sex"] = s2[20]
    info["expiredate"] = s2[21:27]
    info["personalnumber"] = s2[28:37]
    checks = [info["passnumber"], info["birthdate"], info["expiredate"], info["personalnumber"]]
    checkdigits = [s2[9], s2[19], s2[27], s2[43]]

    reportMismatch(checks, checkdigits)
    return info

def encode(type, country, lastname, name, passnumber, birthdate, sex, expiredate, personalnumber):
    def scan():
        pass
    pass

def luhnalgorithm(inputs):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(inputs)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def is_luhn_valid(pass_number):
    return luhnalgorithm(pass_number) == 0

def reportMismatch(checks, checkdigits):
    pass
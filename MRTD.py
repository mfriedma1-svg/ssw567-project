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
    pass
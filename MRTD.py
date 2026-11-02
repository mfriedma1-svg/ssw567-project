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

def encode(info):

    #first line
    document_code = info.get("document_code", "PP")
    issuer = info["country"].upper()

    if len(document_code) != 2 or document_code[0] != "P":
        raise ValueError("Invalid passport document code")

    if len(issuer) != 3 or not issuer.isalpha() or not issuer.isascii():
        raise ValueError("Issuing country must be a 3-letter code")

    name = format_name(
        info["lastname"],
        info["name"]
    )

    line1 = document_code + issuer + name

    #second line

    # Passport number
    passport = format_passnumber(info["passnumber"])
    cd1 = luhnalgorithm(passport)

    # Nationality
    nationality = info.get("nationality", issuer).upper()

    if len(nationality) != 3 or not nationality.isascii() or not nationality.isalpha():
        raise ValueError("Nationality must be a 3-letter code")

    # Birthdate
    birthdate = info["birthdate"]

    if len(birthdate) != 6 or not birthdate.isdigit():
        raise ValueError("Birthdate must be YYMMDD")

    cd2 = luhnalgorithm(birthdate)

    # Sex
    sex = info["sex"].upper()

    if sex not in ("M", "F", "<"):
        raise ValueError("Sex must be M, F, or <")

    # Expiration date
    expiredate = info["expiredate"]

    if len(expiredate) != 6 or not expiredate.isdigit():
        raise ValueError("Expiration date must be YYMMDD")

    cd3 = luhnalgorithm(expiredate)

    # Personal number / optional data
    personal = info.get("personalnumber", "").upper().replace(" ", "<")

    if any(
        not (char == "<" or char.isdigit() or "A" <= char <= "Z")
        for char in personal
    ):
        raise ValueError("Invalid personal number characters")

    personal = pad_field(personal, 14)
    cd4 = luhnalgorithm(personal)

    #create line 2 before composite check digit
    line2 = (
        passport + cd1 +
        nationality +
        birthdate + cd2 +
        sex +
        expiredate + cd3 +
        personal + cd4
    )

    #composite check digit
    cd5 = luhnalgorithm(
        line2[0:10] +
        line2[13:20] +
        line2[21:43]
    )

    line2 += cd5

    return line1, line2

def generate_mrz(passport_id):

    info = accessData(passport_id)

    if info is None:
        raise ValueError("Passport information not found")

    return encode(info)

def accessData(): #empty database access function
    pass

def mrz_value(char):
    if char.isdigit():
        return int(char)
    elif char.isalpha():
        return ord(char) - 55
    elif char == "<":
        return 0
    else:
        raise ValueError("Invalid MRZ character")


def luhnalgorithm(value):
    weights = [7, 3, 1]
    checksum = 0

    for i, char in enumerate(value):
        checksum += mrz_value(char) * weights[i % 3]

    return str(checksum % 10)

def pad_field(value, length):
    value = value.upper()

    if len(value) > length:
        raise ValueError("Field exceeds maximum length")

    return value.ljust(length, "<")


def format_passnumber(value):
    value = value.upper()

    value = "".join(
        char if char.isascii() and char.isalnum() else "<"
        for char in value
    )

    if len(value) > 9:
        raise ValueError("Passport number exceeds 9 characters")

    return pad_field(value, 9)

def format_name(lastname, firstname):
    lastname = " ".join(lastname.upper().split())
    firstname = " ".join(firstname.upper().split())

    for char in lastname + firstname:
        if char != " " and not ('A' <= char <= 'Z'):
            raise ValueError("Names must be transliterated to A-Z")

    name = lastname.replace(" ", "<") + "<<" + firstname.replace(" ", "<")

    if len(name) > 39:
        raise ValueError("Name exceeds 39 characters")

    return name.ljust(39, "<")

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
        new_checkdigits.append(luhnalgorithm(check))

    # compare each provided digit to the calculated one
    i = 0
    for digit in checkdigits:
        if digit != new_checkdigits[i]:
            print(f"Mismatch found! Expected {checkdigits[i]} but calculated {new_checkdigits[i]}")
        i += 1
import random
import string
import time
import re

FALLBACK_MAPPINGS = {
    "_char": 3, 
    "_supports98": True, 
    "a": "100", 
    "b": "101", 
    "c": "102", 
    "d": "103", 
    "e": "104", 
    "f": "105", 
    "g": "106", 
    "h": "107", 
    "i": "108", 
    "j": "109", 
    "k": "110", 
    "l": "111", 
    "m": "112", 
    "n": "113", 
    "o": "114", 
    "p": "115", 
    "q": "116", 
    "r": "117", 
    "s": "118", 
    "t": "119", 
    "u": "120", 
    "v": "121", 
    "w": "122", 
    "x": "123", 
    "y": "124", 
    "z": "125", 
    "A": "126", 
    "B": "127", 
    "C": "128", 
    "D": "129", 
    "E": "130", 
    "F": "131", 
    "G": "132", 
    "H": "133", 
    "I": "134", 
    "J": "135", 
    "K": "136", 
    "L": "137", 
    "M": "138", 
    "N": "139", 
    "O": "140", 
    "P": "141", 
    "Q": "142", 
    "R": "143", 
    "S": "144", 
    "T": "145", 
    "U": "146", 
    "V": "147", 
    "W": "148", 
    "X": "149", 
    "Y": "150", 
    "Z": "151", 
    "0": "152", 
    "1": "153", 
    "2": "154", 
    "3": "155", 
    "4": "156", 
    "5": "157", 
    "6": "158", 
    "7": "159", 
    "8": "160", 
    "9": "161", 
    " ": "162", 
    "!": "163", 
    "\"": "164", 
    "#": "165", 
    "$": "166", 
    "%": "167", 
    "&": "168", 
    "'": "169", 
    "(": "170", 
    ")": "171", 
    "*": "172", 
    "+": "173", 
    ",": "174", 
    "-": "175", 
    ".": "176", 
    "/": "177", 
    ":": "178", 
    ";": "179", 
    "<": "180", 
    "=": "181", 
    ">": "182", 
    "?": "183", 
    "@": "184", 
    "[": "185", 
    "\\": "186", 
    "]": "187", 
    "^": "188", 
    "_": "189", 
    "`": "190", 
    "{": "191", 
    "|": "192", 
    "}": "193", 
    "~": "194"
}

def loadMappings(file_path):
    # in the future load mappings from file
    try:
        log(f"loaded {file_path}")
        mappings = loadQmapFile(file_path)
        if not mappings:
            raise ValueError
        return mappings
    except:
        log(f"{RED}ERROR - USING FALLBACK MAPPINGS")
        return FALLBACK_MAPPINGS

def animation(mappings):
    log("Loading mappings...")
    for key in mappings.keys():
        if not(len(key) > 1 and key.startswith("_")):
            time.sleep(0.01)
            log(f"Mapped {RED}{key} {GREEN}to {RED}{mappings[key]}{GREEN}!")

def askForMode():
    return ask("Decode or Encode? (d/e)")

def encode(string, mappings):
    enc = ""
    log(f"Started encoding [{string}]")
    for char in string:
        enc = enc + mappings[char]
        log(f"Progress: [{enc}]")
    enc = enc + "99"
    return enc

def decode(string, mappings):
    if not string.endswith("99"):
        log(f"{RED}Error: Invalid string!")
        return
    log(f"Started decoding [{string}]")
    string = string[:-2]
    i = 0
    charlist = []
    tempstr = ""
    for char in string:
        tempstr = tempstr + char
        i += 1
        if i == mappings["_char"]:
            i = 0
            charlist.append(tempstr)
            tempstr = ""
    dec = ""
    for char in charlist:
        try:
            dec = dec + next(key for key, value in mappings.items() if value == char)
        except:
            log(f"{YELLOW}WARNING: Skipping malformed char {RED}{char}")
        log(f"Progress: [{dec}]")
    return dec

def checkForValidMapping(mapping):
    try:
        char = mapping["_char"]
        support = mapping["_supports98"]
        canBe98 = True
        for key in mapping.keys():
            if not key.startswith("_"):
                if len(key) > 1:
                    log(f"{YELLOW}WARNING: Invalid key [{RED}{key}{YELLOW}]")
                if not len(mapping[key]) == char:
                    log(f"{YELLOW}WARNING: Invalid value length [{RED}{mapping[key]}{YELLOW}]")
                try:
                    int(mapping[key])
                except:
                    canBe98 = False
        if canBe98 and support == False:
            log(f"{YELLOW}WARNING: 98 is disabled, could be allowed!")
        if not canBe98 and support == True:
            log(f"{YELLOW}WARNING: 98 is enabled, may not work!")

    except:
        log(f"{RED}Error: Invalid Mapping!")

def get_key_by_value(dictionary, value):
    for key, val in dictionary.items():
        if val == value:
            return key
    return None  # Return None if the value is not found

def getPw(input_string):
    return ''.join(str(mappings[char]) for char in input_string)

def saltIt(input, password):
    if not input.endswith("99"):
        raise ValueError
    input = input[:-2]
    return int_to_str(int(input)*int(password)).__add__("-98")

def unSalt(input, password):
    return int_to_str(int(input)//int(password)).__add__("99")

def int_to_str(n):
    if n == 0:
        return "0"
    negative = n < 0
    n = abs(n)
    digits = []
    while n:
        digits.append(str(n % 10))
        n //= 10
    result = "".join(digits[::-1])
    return "-" + result if negative else result

def main(mappings):
    animation(mappings)
    checkForValidMapping(mappings)
    while True:
        mode = askForMode()
        if mode == "e":
            string = ask("String to encode")
            use98 = True if ask("Use QWERTZ 98 (password) [y/n]") == "y" else False
            if use98:
                password = ask("Password to use", 98)
            done = encode(string, mappings)
            if use98:
                done = saltIt(done, getPw(password))
            log(f"Done! [{RED}{done}{GREEN}]")
        elif mode == "d":
            string = ask("String to decode")
            if string.endswith("-98"):
                password = ask("String uses QWERTZ 98. Password to use", 98)
                string = unSalt(string[:-3], getPw(password))
            done = decode(string, mappings)
            log(f"Done! [{RED}{done}{GREEN}]")

def ask(message, type = 99):
    if type == 99:
        return input(f"{YELLOW}[{BLUE}QWERTZ 99{YELLOW}]{GREEN} {message}: ")
    elif type == 98:
        return input(f"{BLUE}[{YELLOW}QWERTZ 98{BLUE}]{GREEN} {message}: ")
def log(message, type = 99):
    if type == 99:
        print(f"{YELLOW}[{BLUE}QWERTZ 99{YELLOW}]{GREEN} {message}")
    elif type == 98:
        print(f"{BLUE}[{YELLOW}QWERTZ 98{BLUE}]{GREEN} {message}")

def loadQmapFile(file_path):
    mappings = {}
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            if not content.startswith('[QMAP]'):
                raise ValueError("Invalid QMAP file format")

            content = content[6:]  # Remove [QMAP]

            # Extract _char and _supports98
            char_match = re.search(r'\{c:(\d+)\}', content)
            support_match = re.search(r'\{s:([01])\}', content)

            if char_match and support_match:
                mappings['_char'] = int(char_match.group(1))
                mappings['_supports98'] = bool(int(support_match.group(1)))
            else:
                raise ValueError("Missing _char or _supports98 specification")

            # Extract mappings
            mapping_pairs = re.findall(r'\((\d+)\|(\d+)\)', content)
            for ord_val, mapping in mapping_pairs:
                char = chr(int(ord_val))
                mappings[char] = mapping

        return mappings
    except Exception as e:
        log(f"{RED}Error loading .qmap file: {e}")
        return None

def saveMappingsToQmap(mappings, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write('[QMAP]')
            file.write(f"{{c:{mappings['_char']}}}")
            file.write(f"{{s:{1 if mappings['_supports98'] else 0}}}")
            for char, value in mappings.items():
                if not char.startswith('_'):
                    file.write(f"({ord(char)}|{value})")
        log(f"Mappings saved to {file_path}")
    except Exception as e:
        log(f"{RED}Error saving .qmap file: {e}")


def generate_random_mapping(file_path):
    mappings = {
        '_char': 3,
        '_supports98': True
    }

    # Generate unique 3-digit codes for each character
    available_codes = list(range(100, 999))  # 3-digit codes from 100 to 998
    random.shuffle(available_codes)

    # Assign codes to the first 999 ASCII characters
    for i in range(899):
        char = chr(i)
        if char.isprintable() and char not in '\r\n\t\f\v':
            code = str(available_codes.pop())
            mappings[char] = code

    log(f"{GREEN}Random mapping generated and saved to {file_path}")
    saveMappingsToQmap(mappings, file_path)

    return mappings

if __name__ == "__main__":
    GREEN = ""
    RED = ""
    YELLOW = ""
    BLUE = ""
    log("Trying to load color support...")
    try:
        from colorama import Fore, Back, Style
        GREEN = Fore.GREEN
        RED = Fore.RED
        YELLOW = Fore.YELLOW
        BLUE = Fore.BLUE
        log("Colors loaded!")
    except:
        log("Error loading colors!")
    mppng = ask("Mapping file to load? [*.qmap]")
    mappings = loadMappings(mppng)
    main(mappings)
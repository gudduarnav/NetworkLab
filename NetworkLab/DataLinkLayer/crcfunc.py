# CRC Helper function
# https://en.wikipedia.org/wiki/Cyclic_redundancy_check

def xor1bit(a, b):
    if a == b:
        return "0"
    else:
        return "1"



def remainder(message : str, poly : str, filler: str, printStep=False):
    if printStep: print(message, poly, filler)
    l_message = list(message)
    l_poly = list(poly)
    l_filler = list(filler)

    count_1_poly = l_poly.count("1")

    l_message_filler = l_message.copy()
    l_message_filler.extend(l_filler[0:count_1_poly])

    while "1" in l_message_filler[0:len(message)]:
        index =l_message_filler[0:len(message)].index("1")

        for offset in range(len(l_poly)):
            l_message_filler[index+offset] = xor1bit(l_message_filler[index+offset], l_poly[offset])

        if printStep: print("".join(l_message_filler))

    return "".join(l_message_filler[len(message):])


def sendmessage(message: str, poly: str):
    count_1 = poly.count("1")
    crc = remainder(message = message, poly = poly, filler="0"*count_1, printStep=False)
    return message + crc

def receivemessage(messagecrc: str, poly: str):
    count_filler = poly.count("1")
    message = messagecrc[0:(len(messagecrc)-count_filler)]
    filler = messagecrc[(len(messagecrc)-count_filler):]

    crc = remainder(message=message, poly=poly, filler=filler, printStep=False)

    return True if "1" not in crc else False


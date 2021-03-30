
import crcfunc
import random
import time

# x3 + x1 + x0 => 1 x3 + 0 x2 + 1 x1 + 1 x0 = '1011'
def detectcrcpoly(s : str):
    l = list()
    tok = s.split("+")
    for tok1 in tok:
        term = int(tok1[(tok1.index("x")+1):len(tok1)])
        l.append(term)

    poly = list("0"*(max(l)+1))
    for one in l:
        poly[one] = "1"

    poly.reverse()
    return "".join(poly)


def main():
    crcpol = input("Enter CRC poly:")
    message = input("Input Message:")
    poly = detectcrcpoly(crcpol)
    print("Poly for", crcpol, "is", poly)

    crcmessage = crcfunc.sendmessage(message=message, poly=poly)
    isok = crcfunc.receivemessage(messagecrc=crcmessage, poly=poly)

    print("CRC appended message is", crcmessage) # rightmost part will contain CRC
    print("Received message is", crcmessage, "checked OK?", isok)

    # introduce 10 random errors
    l_crcmessage = list(crcmessage)
    N = len(l_crcmessage)
    for _ in range(10):
        error_position = random.randint(0, N)
        error_bit = random.randint(0, 1)
        l_crcmessage[error_position] = str(error_bit)
        crcmessage = "".join(l_crcmessage)

        isok = crcfunc.receivemessage(messagecrc=crcmessage, poly=poly)

        print("ERROR bit", error_bit, "set at position", error_position, "error message=", crcmessage, "CRC Check OK?", isok)
        time.sleep(0.25)



if __name__ == "__main__":
    main()


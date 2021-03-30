import crcfunc

print("CRC=", crcfunc.remainder(message="11010011101100", poly="1011", filler="000"))

msg = crcfunc.sendmessage(message="11010011101100", poly="1011")

isOk = crcfunc.receivemessage(messagecrc=msg, poly="1011")
print("Send message with CRC=", msg)
print("receive message=", isOk)
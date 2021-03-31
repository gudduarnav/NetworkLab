# Simplex Stop and Wait
try:
    from multiprocessing import SimpleQueue, set_start_method, Process
except ImportError as __ex:
    print("Install multiprocessing. Exception:", str(__ex))

from time import sleep
from random import randint

def machineTX(q1 : SimpleQueue, q2 : SimpleQueue, n : int, sleeptime : float, maxwait : int):
    counter = 0
    packet = 0
    isfirst = True
    waitcounter = 0
    while True:
        counter = counter + 1
        # add some delay
        sleep(sleeptime)

        if isfirst:
            isfirst = False
            # dont wait for ACK on first packet
            q1.put(packet)
            print("machineTX #{}: packet {} sent".format(counter, packet))
            waitcounter = 0
        else:
            # check if we have some ACK
            if not q2.empty():
                status = q2.get()

                # check ACK report
                if "ACK" in status:
                    print("machineTX #{}: received {}".format(counter, status))
                    packetID = int(status.split()[1])

                    # packet acknowledged ....so send next
                    if packetID == packet:
                        packet = packet+1
                        # check if all packets sent
                        if packet > n:
                            break

                        print("machineTX #{}: will transmit next packet {}".format(counter, packet))
                        q1.put(packet)
                        print("machineTX #{}: new packet {} sent".format(counter, packet))
                        waitcounter = 0

                else:
                    waitcounter = waitcounter + 1
                    print("machineTX #{}: waiting for ACK waittime={} maxwait={}".format(counter, waitcounter, maxwait))
            else:
                waitcounter = waitcounter + 1
                print("machineTX #{}: waiting for ACK waittime={} maxwait={}".format(counter, waitcounter, maxwait))

        # if wait counter exceeds threshold for wait
        # resend packet without waiting
        if waitcounter > maxwait:
            print("machineTX #{}: wait for ACK exceeded max wait time. RESEND PACKET".format(counter))
            q1.put(packet)
            print("machineTX #{}: resent packet {}".format(counter, packet))
            waitcounter = 0

    print("machineTX: all {} packets sent".format(n))

def isPacketValid():
    number = randint(0,1)
    status = True if number==1 else False
    print("\tisPacketValid()=>", number, status)
    return status

def machineRX(q1 : SimpleQueue, q2 : SimpleQueue, n : int, sleeptime : float):
    counter = 0 # count packets
    while True:
        counter = counter + 1
        # add some delay
        sleep(sleeptime)

        # check if i have packet
        if not q1.empty():
            # i have packet
            packet = q1.get()
            print("machineRX #{}: Packet {} received".format(counter, packet))

            # check if packet valid
            if isPacketValid():
                print("machineRX #{}: Packet {} is VALID".format(counter, packet))
                status = "ACK {}".format(packet)
                q2.put(status)
                print("machineRX #{}: {} SENT".format(counter, status))
                if packet >= n:
                    break
            else:
                print("machineRX #{}: Packet {} is INVALID. NO ACK SENT".format(counter, packet))

    print("machineRX #{}: {} packets received DONE".format(counter, n))



def main():
    set_start_method("spawn")

    # Transmit queue
    q1 = SimpleQueue()
    q2 = SimpleQueue()

    # number of packet to send
    n = 20

    # delay time
    sleeptime = 1

    # max wait for ACK
    maxwait = 4

    # spawn receiver
    p = Process(target=machineRX, args=(q1, q2, n, sleeptime))
    p.start()

    # spawn transmitter
    machineTX(q1, q2, n, sleeptime ,maxwait)

    # wait till end
    p.join()

if __name__ == "__main__":
    main()

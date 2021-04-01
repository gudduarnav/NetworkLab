# Go Back N
try:
    from multiprocessing import SimpleQueue, set_start_method, Process
except ImportError as __ex:
    print("Install multiprocessing. Exception:", str(__ex))

from time import sleep
from random import randint, seed
from datetime import datetime

class Sender:
    def __init__(self,
                 q_sender : SimpleQueue,
                 q_receiver : SimpleQueue,
                 sleeptime : float,
                 npackets : int,
                 maxwaitcount : int):

        self.q_sender = q_sender
        self.q_receiver = q_receiver
        self.sleeptime = sleeptime
        self.npackets = npackets
        self.maxwaitcount = maxwaitcount
        self.packetQ = list()
        self.ackpacketQ = list()
        self.packetIndex = 0
        seed(datetime.now())

        self.start()

    def rest(self):
        sleep(self.sleeptime)

    def start(self):
        while self.isMorePackets():
            self.rest()
            self.SendPacket()
            self.WaitACK()

    def SendPacket(self):
        # check if we are allowed to send
        if self.packetIndex >= self.npackets:
            print("Sender have sent all", self.npackets,"packets. NO MORE PACKETS TO SEND")
            return

        # send packet indicated
        one_packet = [self.packetIndex, 0]
        self.packetQ.append(one_packet)
        self.q_sender.put(one_packet[0])
        print("Sender sent one packet #", one_packet[0])

        # point to next packet to send
        self.packetIndex += 1

    def WaitACK(self):
        # check for ACK
        if self.q_receiver.empty():
            print("Sender did not receive any ACK")
            self.increaseWaitTime()
            self.checkWaitTime()
            return

        # read the ACK
        ack_packet = self.q_receiver.get()
        print("Sender received ACK", ack_packet)
        self.ackpacketQ.append(ack_packet)
        self.ackpacketQ.sort()

        indexToPop = -1
        for index in range(len(self.packetQ)):
            if self.packetQ[index][0] == ack_packet:
                indexToPop = index
            else:
                self.packetQ[index][1] += 1
                print("Sender updated waittime of packets", self.packetQ[index])

        if indexToPop>=0:
            self.packetQ.pop(indexToPop)
            self.checkWaitTime()

    def increaseWaitTime(self):
        for index in range(len(self.packetQ)):
            self.packetQ[index][1] += 1
            print("Sender updated waittime of packets", self.packetQ[index])

    def checkWaitTime(self):
        packetsLost = list()
        for index in range(len(self.packetQ)):
            if self.packetQ[index][1] > self.maxwaitcount:
                packetsLost.append(self.packetQ[index][0])

        if len(packetsLost)>0:
            packetsLost.sort()
            firstPacketLost = packetsLost[0]
            print("\n\t\t*** Sender GO BACK", firstPacketLost, "***\n")
            self.packetQ.clear()
            self.packetIndex = firstPacketLost

            self.ackpacketQ.sort()
            for index in range(firstPacketLost, self.npackets):
                if index in self.ackpacketQ:
                    self.ackpacketQ.remove(index)
                    print("Sender discarded packet", index)



    def ResendPacket(self):
        one_packet = self.packetQ[0]
        self.packetQ.pop(0)

        # point to the packet to resend
        self.packetIndex = one_packet[0]

        print("Sender need to resend packet", one_packet[0], "PACKET LOST")





    def isMorePackets(self):
        for index in range(0, self.npackets):
            if index not in self.ackpacketQ:
                return True

        return False


class Receiver:
    def __init__(self,
                 q_sender : SimpleQueue,
                 q_receiver : SimpleQueue,
                 sleeptime : float,
                 npackets : int):
        self.q_sender = q_sender
        self.q_receiver = q_receiver
        self.sleeptime = sleeptime
        self.npackets = npackets
        self.packetQ = list()

        seed(datetime.now())
        self.start()

    def rest(self):
        sleep(self.sleeptime)

    def isPacketValid(self):
        number = randint(0,1)
        status = True if number==1 else False
        #print("\tisPacketValid()=>", number, status)
        return status

    def start(self):
        while self.isMorePackets():
            self.rest()
            self.ReceivePacket()

    def isMorePackets(self):
        for index in range(0, self.npackets):
            if index not in self.packetQ:
                return True

        return False

    def ReceivePacket(self):
        if self.q_sender.empty():
            return

        packet = self.q_sender.get()
        status = self.isPacketValid()

        if status:
            print("Receiver received packet", packet)
            packetQ1 = list()
            for index in range(len(self.packetQ)):
                if self.packetQ[index] < packet:
                    packetQ1.append(self.packetQ[index])

            self.packetQ = packetQ1
            self.packetQ.append(packet)

            self.q_receiver.put(packet)
            print("Receiver ACK", packet,"SENT")
            self.showCollectedPackets()
        else:
            print("Receiver packet", packet, "FAILED")
            print("Receiver NACK", packet)

    def showCollectedPackets(self):
        packet1 = self.packetQ.copy()
        packet1.sort()
        print("\n\t\t*** RECEIVER COLLECTED PACKETS:", packet1,"***\n")





def machineTX(q1 : SimpleQueue, q2 : SimpleQueue, n : int, sleeptime : float, maxwait : int):
    Sender(q1, q2, sleeptime, n, maxwait)

def machineRX(q1 : SimpleQueue, q2 : SimpleQueue, n : int, sleeptime : float):
    Receiver(q1, q2, sleeptime, n)






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

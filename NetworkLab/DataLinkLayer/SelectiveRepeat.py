# Selective Repeat
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
        self.ack_PacketQ = list()
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
        # send packet indicated
        for index in range(len(self.packetQ)):
            if self.packetQ[index][1] > self.maxwaitcount:
                print("Sender will SELECTIVE RESEND", self.packetQ[index][0])

                self.q_sender.put(self.packetQ[index][0])
                self.packetQ[index][1] = 0
                print("Sender RESEND packet", self.packetQ[index][0])
                return

        if self.packetIndex < self.npackets:
            self.q_sender.put(self.packetIndex)
            self.packetQ.append([self.packetIndex, 0])
            print("Sender sent NEW PACKET", self.packetIndex)

            self.packetIndex += 1

    def WaitACK(self):
        if self.q_receiver.empty():
            self.increaseTime()
        else:
            ack_packet = self.q_receiver.get()

            for index in range(len(self.packetQ)):
                if self.packetQ[index][0] == ack_packet:
                    self.packetQ.pop(index)
                    break

            self.ack_PacketQ.append(ack_packet)
            self.ack_PacketQ.sort()
            print("Sender received ACK", ack_packet)
            self.increaseTime()

    def increaseTime(self):
        for index in range(len(self.packetQ)):
            self.packetQ[index][1] += 1


    def isMorePackets(self):
        for index in range(self.npackets):
            if index not in self.ack_PacketQ:
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
        print("\n\t\t\t *** RECEIVER COLLECTED PACKETS:", packet1, "***\n")





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

# Simplex Stop and Wait
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
        one_packet = [self.packetIndex, 0]
        self.packetQ.append(one_packet)
        self.q_sender.put(one_packet[0])
        print("Sender sent one packet #", one_packet[0])

    def WaitACK(self):
        # wait for ACK
        while self.q_receiver.empty():
            self.rest()

            # Increase wait count
            self.packetQ[0][1] = self.packetQ[0][1] + 1
            print("Sender Waiting for ACK on Packet", self.packetQ[0][0], "waittime=", self.packetQ[0][1])

            # if waitcount excedded threshold...packet is dead. resend
            if self.packetQ[0][1] > self.maxwaitcount:
                self.ResendPacket()
                return

        ack_packet = self.q_receiver.get()
        self.packetQ.pop(0)
        # point to next packet
        self.packetIndex = self.packetIndex + 1
        print("Sender received ACK", ack_packet)


    def ResendPacket(self):
        one_packet = self.packetQ[0]
        self.packetQ.pop(0)

        # point to the packet to resend
        self.packetIndex = one_packet[0]

        print("Sender need to resend packet", one_packet[0], "PACKET LOST")





    def isMorePackets(self):
        if len(self.packetQ) == 0:
            # there is no item in queue
            if self.packetIndex >= self.npackets:
                print("Sender sent all packets successfully. Packets sent", self.packetIndex)
                return False

        return True


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

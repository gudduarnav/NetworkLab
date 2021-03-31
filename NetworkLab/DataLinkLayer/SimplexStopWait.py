# Simplex Stop and Wait
try:
    from multiprocessing import SimpleQueue, set_start_method, Process
except ImportError as __ex:
    print("Install multiprocessing. Exception:", str(__ex))

from time import sleep

def machineTX(q1 : SimpleQueue, q2 : SimpleQueue, n : int, sleeptime : float):
    counter = 0 # counter for keeping track of packets
    while counter <= n:
        # some delay
        sleep(sleeptime)

        # for first packet, send and dont wait
        if counter == 0:
            q1.put(counter)
            print("machineTX: Packet {} sent".format(counter))
            counter = counter + 1
        elif counter < n:
            # wait for ACK
            while q2.empty():
                sleep(sleeptime)

            # get a new ACK packet
            status = q2.get()

            # ACK received then transmit new packet
            if status == "ACK":
                print("machineTX: ACK received")
                q1.put(counter)
                counter = counter + 1
        else:
            # wait for ACK
            while q2.empty():
                sleep(sleeptime)

            # get a new ACK packet
            status = q2.get()

            # ACK received for last packet
            if status == "ACK":
                print("machineTX: ACK received for last packet")
                counter = counter + 1
                break
    print("machineTX: {} packets sent DONE".format(n))


def machineRX(q1 : SimpleQueue, q2 : SimpleQueue, n : int, sleeptime : float):
    counter = 0 # count packets
    while counter < n:
        # add some delay
        sleep(sleeptime)

        # wait for packet
        while q1.empty():
            sleep(sleeptime)
        packet = q1.get()
        print("machineRX: packet {} received".format(packet))
        q2.put("ACK")
        print("machineRX: packet {} acknowledged (ACK)".format(packet))

        counter = counter + 1


    print("machineRX: {} packets received DONE".format(n))



def main():
    set_start_method("spawn")

    # Transmit queue
    q1 = SimpleQueue()
    q2 = SimpleQueue()

    # number of packet to send
    n = 10

    # delay time
    sleeptime = 2

    # spawn receiver
    p = Process(target=machineRX, args=(q1, q2, n, sleeptime, ))
    p.start()

    # spawn transmitter
    machineTX(q1, q2, n, sleeptime )

    # wait till end
    p.join()

if __name__ == "__main__":
    main()

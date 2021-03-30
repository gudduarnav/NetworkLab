# Queue

try:
    import multiprocessing as mp
except ImportError as __ex:
    print("Install multiprocessing. Exception:", str(__ex))

from datetime import datetime
from time import sleep



# parent will put to queue
def parentProcess(q:mp.Queue):
    for _ in range(0,10):
        s = str(datetime.now())
        q.put(s)
        print("\nPARENT PUT", s)
        sleep(1)

    q.put("exit")
    print("\nPARENT DONE")

def childProcess(q : mp.Queue):
    while True:
        s = q.get(block=True)
        if s == "exit":
            print("\nCHILD DONE")
            break
        else:
            print("\nCHILD GET:", s)



def main():
    # use this once
    mp.set_start_method("spawn")

    # Queue
    q = mp.Queue()

    # spawn the child process
    p = mp.Process(target=childProcess, args=(q, ))
    p.start()

    # invoke the parent process
    parentProcess(q)

    # wait for the child to end
    p.join()

if __name__ == "__main__":
    main()
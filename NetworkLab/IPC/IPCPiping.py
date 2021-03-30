# Pipes In-process

try:
    import multiprocessing as mp
except ImportError as __ex:
    print("Install multiprocessing. Exception:", str(__ex))

# parent will write text to child
def parentProcess(conn):
    print("\nParent writing text...")
    data = [1, True, "Hello"]
    conn.send(data)
    print("\nParent send data", data)
    print("\nParent write COMPLETE")

def childProcess(conn):
    print("\nChild reading text...");
    data = conn.recv()
    print("\nChild read COMPLETE")
    print("\nChild received data:", data)

def main():
    # create parent and child pipe
    parent_conn, child_conn = mp.Pipe()

    # spawn the child process
    p = mp.Process(target=childProcess, args=(child_conn, ))
    p.start()

    # invoke the parent process
    parentProcess(parent_conn)

    # wait for the child to end
    p.join()

if __name__ == "__main__":
    main()
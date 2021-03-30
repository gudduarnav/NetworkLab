# Spawn a child process from parent process

try:
    import multiprocessing as mp
except ImportError as __ex:
    print("Install multiprocessing. Exception:", str(__ex))

def parentProcess():
    print("Parent Process")

def childProcess():
    print("Child Process")

def main():
    p = mp.Process(target=childProcess, args=())
    p.start()
    parentProcess()
    p.join()

if __name__ == "__main__":
    main()
import threading
from threading import Thread
from time import sleep

count_global = 0

class CoolMessage(Thread):
    def __init__(self):
        Thread.__init__(self)
        print(f"{self.name} is being created")
        self.count_local = 0

    def print_message(self):
        self.count_local += 1
        global count_global
        count_global += 1
        print(f"{self.name}, count_local={self.count_local}, count_global={count_global}")

    def run(self):
        print(f"{self.name} starting")
        for x in range(10):
            self.print_message()
            sleep(0.5)
        print(f"{self.name} ending")

def print_message_thread(value):
        global count_global
        count_global += value

def create_threads():
    print("--- Process Started ---")

    # Two ways to create a thread:
    # 1) Create a class that extends Thread and then instantiate that class
    # 2) Instantiate Thread and give it a target and arguments

    # TODO #1) create a class that extends Thread and then instantiate 2 objects
    cool_message1 = CoolMessage()
    cool_message2 = CoolMessage()
    cool_message3 = CoolMessage()

    # TODO start the threads
    cool_message1.start()
    cool_message2.start()
    cool_message3.start()
    
    # TODO sleep for a bit to simulate I/O bound
    sleep(0.3)
    
    # TODO join the threads back to main thread
    cool_message1.join()
    cool_message2.join()
    cool_message3.join()

    # TODO #2) create a Thread
    a = 13
    t = threading.Thread(target=print_message_thread, args=(a,))

    # TODO start it
    t.start()
    print(f"{count_global=}")

    # TODO don't join it just yet
    t.join()

if __name__ == '__main__':
    create_threads()
    print("--- End of Program ---")

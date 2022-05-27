"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Matthew James and Joshua Capron and now Connor Baltich

Purpose: Check for prime values

Instructions:

- You can't use thread/process pools
- Follow the graph in I-Learn
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
from queue import Queue
import time
import threading
import multiprocessing as mp
import random

#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 3

def is_prime(n: int):

    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def reader_thread(filename, que):
    with open(filename, 'r') as f:
        for line in f:
            que.put(line.strip())
        for _ in range(PRIME_PROCESS_COUNT):
            que.put(None)

   


# TODO create prime_process function

def prime_process(prime_que, manager_list):
    # for _ in range(1, prime_que.qsize()):
    #     number = int(prime_que.get())
    #     if is_prime(number):
    #         print(number)
    #         manager_list.append(number)
    while True:
        number = prime_que.get()
       
        if number == None:
            break
        if is_prime(int(number)):
            manager_list.append(number)
   
    # return manager_list
           

def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')
           



def main():
    """ Main function """

    filename = 'data.txt'

    # Once the data file is created, you can comment out this line
    # create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    primes = mp.Manager().list()
    que = mp.Queue()
   

    # TODO create reading thread
    read_thread = threading.Thread(target=reader_thread, args=(filename, que))
   
    # TODO create prime processes


    processes = [mp.Process(target=prime_process, args=(que, primes)) for i in range(3)]

   
    # TODO Start them all
    read_thread.start()
   
    for i in range(PRIME_PROCESS_COUNT):
        processes[i].start()    

    # TODO wait for them to complete
    read_thread.join()
    for i in range(PRIME_PROCESS_COUNT):
        processes[i].join()
   
   
    # for i in range(1, que.qsize()):
    #     print(que.get())
       
   
   
       
    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()
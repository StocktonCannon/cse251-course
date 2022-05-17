"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

"""

from multiprocessing import Semaphore
import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 40        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(queue, log):  
    """ Process values from the data_queue """

    while True:
        queue_empty = queue.get()
        if queue_empty == NO_MORE_VALUES:
            return 0
        else:
            url = queue_empty[0]

        url_processed = requests.get(url)

        if url_processed.status_code == 200:
            response = url_processed.json()
            log.write(response['name'])


def file_reader(log, queue): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """

    with open("cse251-course/week04/team/data.txt", "r") as f:
        for line in f:
            queue.put(line.split())

    log.write('finished reading file')

    for x in range(RETRIEVE_THREADS):
        queue.put(NO_MORE_VALUES)


def main(RETRIEVE_THREADS):
    """ Main function """
    log = Log(show_terminal=True)

    q = queue.Queue()

    # Pass any arguments to these thread need to do their job
    thread_list = []
    for x in range(RETRIEVE_THREADS):
        t = threading.Thread(target= retrieve_thread, args= (q, log))
        thread_list.append(t)

    t = threading.Thread(target= file_reader, args= (log, q))
    thread_list.append(t)

    log.start_timer()

    for x in thread_list:
        x.start()

    for x in thread_list:
        x.join()

    return log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    results = []
    for i in range(1,10):
        results.append(main(i))
    for result in range(1,10):
        print(f'thread count = {i}, result = {results[i-1]}')
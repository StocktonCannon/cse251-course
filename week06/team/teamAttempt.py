"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import ctypes
import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp
import multiprocessing 

# Include cse 251 common Python files
from cse251 import *

END_MESSAGE = 'End'

def sender(conn: multiprocessing.Pipe,filename1,counter):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(filename1,'r') as file:
        for line in file:
            words = line.split(" ")
            for word in words:
                counter.value += 1
                conn.send(word)

        conn.send(END_MESSAGE)

        conn.close()


def receiver(conn: multiprocessing.Pipe, filename2, counter):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(filename2, 'w', newline='\n') as f:
        while True:
            word = conn.recv()
            # print(f'recieving {word}')
            if word == END_MESSAGE:
                break    
            if "\n" in word:
                f.write(word)
            else:
                f.write(word + ' ')


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    parent_conn, child_conn = multiprocessing.Pipe()
    
    # TODO create variable to count items sent over the pipe
    counter = multiprocessing.Value(ctypes.c_int)

    # TODO create processes 
    senderProcess = multiprocessing.Process(target=sender, args=(parent_conn,filename1,counter))
    receiverProcess = multiprocessing.Process(target=receiver, args=(child_conn,filename2,counter))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    senderProcess.start()
    receiverProcess.start()
    
    # TODO wait for processes to finish
    senderProcess.join()
    receiverProcess.join()

    stop_time = log.get_time()

    total_time = stop_time - start_time

    log.stop_timer(f'Total time to transfer content = {counter.value}: ')
    log.write(f'items / second = {counter.value / (total_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    # copy_file(log, 'week06/team/gettysburg.txt', 'week06/team/gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    copy_file(log, 'week06/team/bom.txt', 'week06/team/bom-copy.txt')


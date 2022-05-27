



import multiprocessing
import time

END_MESSAGE = "End"


def sender(conn: multiprocessing.Pipe):
    msgs = ["hello","hey","how", "are","you"]
    
    for msg in msgs:
        conn.send(msg)

    conn.send(END_MESSAGE)

    conn.close()

def receiver(conn: multiprocessing.Pipe):
    while True:
        msg = conn.recv()

        if msg == END_MESSAGE:
            conn.close()
            break

        print(f'message = {msg}')

    conn.close()

def main():
    parent_conn, child_conn = multiprocessing.Pipe()

    p1 = multiprocessing.Process(target= sender, args=(parent_conn,))
    p2 = multiprocessing.Process(target= receiver, args=(child_conn,))

    p1.start()
    p2.start()

    print('call recv again')
    child_conn.recv()
    print('recv called again')

    p1.join()
    p1.join()

    

if __name__ == "__main__":
    main()




import ctypes
import multiprocessing

def f(number,arr):
    number.value = 3.145927

    for i in range(len(arr)):
        arr[i] = -arr[i]

if __name__ == '__main__':

    # value = multiprocessing.Value('d')
    number = multiprocessing.Value(ctypes.c_double)
    # number = multiprocessing.Manager().Value(ctypes.c_int)

    arr = multiprocessing.Array(ctypes.c_int, range(10))

    p1 = multiprocessing.Process(target=f,args=(number,arr))

    p1.start()
    p1.join()

    print(number.value)
    print(arr[:])

    print(*arr)


import threading


print("\n---- STRINGS ----\n")

a = "first"
b = "first"

print(f"memory adress of a is {id(a)}")
print(f"memory adress of b is {id(b)}")

# keyword 'is' compares memory address
print(a is b)

# == compares by value
print(a == b)

a = "second"
print(f"memory adress of a is {id(a)}")


print("\n---- LISTS ----\n")

a = [10, 20, 30]
b = [10, 20, 30]

print(f"memory adress of a is {id(a)}")
print(f"memory adress of b is {id(b)}")

print(a is b)

print(a == b)

print("\n---- MATH ----\n")

a = 21
b = 2

# float division
print(f"a/b = {a/b}")
# floor division
print(f"a/b = {a//b}")

print("\n---- WITH ----\n")

lock = threading.Lock()
lock.acquire()
a += 100000
lock.release()

with lock:
    a += 100000

try:
    lock.acquire()
    a +=10000
finally:
    lock.release()
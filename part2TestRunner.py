import Sender2
import Receiver2
from threading import Thread
from multiprocessing import Process
import os
import time

hostname = "localhost"
port = 12345
filename = "part2Test.jpg"


testValues = [5,10,15,20,25,30,40,50,75,100]
for test in testValues:
    print()
    print("TESTING: ", test)
    for i in range(5):
        receiver = Thread(target = Receiver2.main, args=(port, filename))
        sender = Thread(target = Sender2.main, args = (hostname, port, "test.jpg", test))
        receiver.start()
        sender.start()
        receiver.join()
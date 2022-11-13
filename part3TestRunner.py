import Sender3
import Receiver3
from threading import Thread
from multiprocessing import Process
import os
import time

hostname = "localhost"
port = 12345
filename = "part3Test.jpg"
timeoutList = [15, 55, 205]
timeout = timeoutList[2]
###CHANGE FOR EXPERIMENT SPECS


testValues = [1, 2, 4, 8 ,16 ,32, 64, 128, 256]
for windowTest in testValues:
    print()
    print("Task3TESTING: ", windowTest)
    for i in range(5):
        receiver = Process(target = Receiver3.main, args=(port, "part3Test.jpg"))
        sender = Process(target = Sender3.main, args = (hostname, port, "test.jpg", timeout, windowTest))
        receiver.start()
        sender.start()
        receiver.join()
import Sender4
import Receiver4
from threading import Thread
from multiprocessing import Process
import os
import time

hostname = "localhost"
port = 12345
filename = "part3Test.jpg"
timeout = 55
###CHANGE FOR EXPERIMENT SPECS


testValues = [1, 2, 4, 8 ,16 ,32, 64, 128, 256]
for windowTest in testValues:
    print()
    print("Task4TESTING: ", windowTest)
    for i in range(5):
        receiver = Process(target = Receiver4.main, args=(port, "part3Test.jpg", windowTest))
        sender = Process(target = Sender4.main, args = (hostname, port, "test.jpg", timeout, windowTest))
        receiver.start()
        sender.start()
        receiver.join()
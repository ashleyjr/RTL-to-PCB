import numpy as np
import time


f = open("/home/ashleyjr/RTL-to-PCB/tools/cpp/tests/full/log.txt","r+")
lines = f.read()
f.close()

seek_net = int(input("Enter net to find: "))

top = np.zeros((100,100))
bot = np.zeros((100,100))
for line in lines.split("\n")[0:-1]:

    c = line.split("(")[1]
    c = c.split(")")[0]
    x = int(c.split(",")[0])
    y = int(c.split(",")[1])
    net = line.split("[")[1]
    net = int(net.split("]")[0])
    if(line[0] == "+"):
        if(line[1] == "t"):
            top[x][y] = 1
        else:
            bot[x][y] = 1
    else:
        if(line[1] == "t"):
            top[x][y] = 0
        else:
            bot[x][y] = 0

    if(net == seek_net):
        if(line[0] == "+"):
            for y in range(100):
                for x in range(100):
                    t = (top[x][y] == 1)
                    b = (bot[x][y] == 1)
                    if t and b:
                        print("+",end="")
                    elif(t):
                        print("-",end="")
                    elif(b):
                        print("|",end="")
                    else:
                        print(".",end="")
                print()
            time.sleep(0.05)
            print(chr(27) + "[2J")


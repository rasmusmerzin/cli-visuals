#ascii animation player

import time
import os

file = input("text file:")

with open(file, "r") as f:
    frames = f.read().split("\n::seperator::\n")
    while 1:
        for i in frames:
            os.system("clear")
            print(i)
            time.sleep(.1)

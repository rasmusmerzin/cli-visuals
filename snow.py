#!/usr/bin/env python


import os, sys, random, time, signal


print("\033[?25l")
def exit(sig, frame):
    print("\033[?25h")
    os.system("clear")
    sys.exit(0)

signal.signal(signal.SIGINT, exit)



def get_scr_size():
    return [int(x) for x in os.popen("stty size", "r").read().split()]

def init():
    global scr, img
    os.system("clear")
    scr = get_scr_size()

chars = [
    [""],
    [".", "`", "'"],
    ["-", '"'],
    ["*", ";", ":", "~"],
    ["$", "&", "="],
    ["#", "@", "%"]
]


def char(p):
    for i in range(len(chars)):
        if i +1 >= (1 -p) *len(chars):
            return chars[i][random.randint(0, len(chars[i]) -1)]
    return ""

def ang2vec(a, r): return [int(math.cos(a /180 *math.pi) *r), int(math.sin(a /180 *math.pi) *r)]   #y, x

def dis(p0, p1): return ((abs(p0[0] -p1[0]) *2) **2 +abs(p0[1] -p1[1]) **2) **.5

def dot(y, x, r):
    for m in range(r *2 +1):
        for n in range(r *4 +1):
            p = [y -r +m, x -r *2 +n]
            print("\033[" +str(p[0]) +";" +str(p[1]) +"H" +char(dis([y, x], p) /r))



init()

while 1:
    time.sleep(.04)
    r = random.randint(3, 5)
    dot(random.randint(r +1, scr[0] -r -1), random.randint(r +1, scr[1] -r -3), r)

#!/usr/bin/env python


import os, sys, random, time, signal, math


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
    [".", "'"],
    [":", ";"],
    ["*", "="],
    ["$", "&"],
    ["#", "@", "%"]
]


def char(p):
    for i in range(len(chars)):
        if i +1 >= (1 -p) *len(chars):
            return chars[i][random.randint(0, len(chars[i]) -1)]
    return ""

def ang2vec(a, r): return [int(math.cos(a) *r), int(math.sin(a) *r *1.5)]   #y, x

def dis(p0, p1): return ((abs(p0[0] -p1[0]) *2) **2 +abs(p0[1] -p1[1]) **2) **.5

def dot(y, x, r, c=37):
    for m in range(r *2 +1):
        for n in range(r *4 +1):
            p = [y -r +m, x -r *2 +n]
            ch = char(dis([y, x], p) /r)
            if ch: print("\033[" +str(c) +"m\033[" +str(p[0]) +";" +str(p[1]) +"H" +ch +"\033[0m")



init()

pos = [int(scr[0] /2), int(scr[1] /2)]
ang = 90

while 1:
    d = random.randint(-60, 60) *math.pi /360
    c = random.randint(31, 36)
    for _ in range(8):
        ang += d
        vec = ang2vec(ang, 3)
        pos = [min(scr[0] -4, max(4, pos[0] +vec[0])), min(scr[1] -4, max(4, pos[1] +vec[1]))]
        time.sleep(.04)
        dot(pos[0], pos[1], 6, c)

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
    ["*", "#"],
    ["$", "&"],
    ["#"]
]


def char(p):
    for i in range(len(chars)):
        if i +1 >= (1 -p) *len(chars):
            return chars[i][random.randint(0, len(chars[i]) -1)]
    return ""

def ang2vec(a, r): return [int(math.cos(a) *r), int(math.sin(a) *r *1.5)]   #y, x

def vec2ang(v): return math.atan(v[1] /v[0]) +(v[0] < 0 and 180 or 0)

def dis(p0, p1): return ((abs(p0[0] -p1[0]) *2) **2 +abs(p0[1] -p1[1]) **2) **.5

def tile2win(p): return [p[0] %(scr[0] -1) +1, p[1] %scr[1] +1]


trail = []
colors = [1, 5, 4, 6, 2, 3]


count = 1
erase = 1
tailsize = 1000

for i in sys.argv[1:]:
    if i[:3] == "-c=":
        try: count = int(i[3:])
        except: pass
    elif i[:8] == "--count=":
        try: count = int(i[8:])
        except: pass
    elif i[:3] == "-e=":
        try: erase = int(i[3:])
        except: pass
    elif i[:8] == "--erase=":
        try: erase = int(i[8:])
        except: pass
    elif i[:3] == "-t=":
        try: tailsize = int(i[3:])
        except: pass
    elif i[:8] == "--tailsize=":
        try: tailsize = int(i[11:])
        except: pass


def dot(y, x, r, c=37):
    global erase, trail
    for m in range(r *2 +1):
        for n in range(r *4 +1):
            p = tile2win([y -r +m, x -r *2 +n])
            ch = char(dis([y, x], p) /r)
            ch = ch == "#" and chr(random.randint(33, 126)) or ch
            if ch:
                print("\033[" +str(30 +colors[c]) +"m\033[" +str(p[0]) +";" +str(p[1]) +"H" +ch +"\033[0m")
                if erase: trail.insert(0, p)

def cleanup():
    global tailsize, trail
    spark = "%%%/!.^'"
    for i in range(len(trail) -1, tailsize, -1):
        if i > tailsize +100:
            if random.randint(0, 1) == 0:
                if trail[:tailsize].count(trail[i]) == 0:
                    print("\033[" +str(trail[i][0]) +";" +str(trail[i][1]) +"H ")
                trail.pop(i)
        else:
            if random.randint(0, 10) == 0:
                if trail[:tailsize].count(trail[i]) == 0:
                    print("\033[" +str(trail[i][0]) +";" +str(trail[i][1]) +"H" +spark[random.randint(0, len(spark) -1)])


init()

pos = [[int(scr[0] /2), int(scr[1] /2)]] *count
ang = [0] *count
c = []
for _ in range(count): c += [random.randint(0, 5)]



while 1:
    for i in c: i = (i +1) %6
    for _ in range(4):
        d = []
        for i in range(count): d += [random.randint(-60, 60) *math.pi /360]
        for _ in range(8):
            for i in range(count):
                ang[i] += d[i]
                vec = ang2vec(ang[i], 3)
                pos[i] = tile2win([pos[i][0] +vec[0], pos[i][1] +vec[1]])
                time.sleep(.02)
                dot(pos[i][0], pos[i][1], 5, c[i])
            if erase: cleanup()

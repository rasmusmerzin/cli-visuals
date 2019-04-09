#!/usr/bin/env python


import os, random, time, sys, signal


print("\033[?25l")
def exit(sig, frame):
    print("\033[?25h")
    os.system("clear")
    sys.exit(0)

signal.signal(signal.SIGINT, exit)


def get_screen_size():
    return [int(x) for x in os.popen("stty size", "r").read().split()]

def draw(txt, pos=0):
    print((pos and ("\033[" +str(pos[0]) +";" +str(pos[1]) +"H") or "") +txt)

def clear():
    os.system("clear")



erase = 0
tailsize = 500
trail = []


for i in sys.argv[1:]:
    if i[:3] == "-e=":
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


def draw_line():
    global erase, trail

    c = "\033[" +str(random.randint(31, 37)) +"m"
    h = random.randint(1, screen_size[0] +screen_size[1] -2)

    d = random.randint(1, 2)

    if h > screen_size[0]:
        for i in range(1, screen_size[0] +1):
            p = (d == 1 and i or (screen_size[0] -i +1), h -screen_size[0])
            draw(c +"|" +chr(random.randint(33, 126)) +"|\033[0m", p)
            if erase:
                trail.insert(0, p)
                trail.insert(0, (p[0], p[1] +1))
                trail.insert(0, (p[0], p[1] +2))
            if i %8 == 0:
                time.sleep(.03)
                if erase: cleanup()
    else:
        for i in range(1, screen_size[1] +1):
            p = (h, d == 1 and i or (screen_size[1] -i +1))
            draw(c +"%\033[0m", p)
            if erase: trail.insert(0, p)
            if i %40 == 0:
                time.sleep(.03)
                if erase: cleanup()


def cleanup():
    global tailsize, trail
    spark = "%%%/!.^'"
    for i in range(len(trail) -1, tailsize, -1):
        if i > tailsize +200:
            if random.randint(0, 1) == 0:
                if trail[:tailsize].count(trail[i]) == 0:
                    print("\033[" +str(trail[i][0]) +";" +str(trail[i][1]) +"H ")
                trail.pop(i)
        else:
            if random.randint(0, 2) == 0:
                if trail[:tailsize].count(trail[i]) == 0:
                    print("\033[" +str(trail[i][0]) +";" +str(trail[i][1]) +"H" +spark[random.randint(0, len(spark) -1)])


screen_size = get_screen_size()
screen_size[0] -= 1
screen_size[1] -= 1

clear()


while 1:
    draw_line()

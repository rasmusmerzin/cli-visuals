#!/usr/bin/env python


import os, random, time


def get_screen_size():
    return [int(x) for x in os.popen("stty size", "r").read().split()]

def draw(txt, pos=0):
    print((pos and ("\033[" +str(pos[0]) +";" +str(pos[1]) +"H") or "") +txt)

def clear():
    os.system("clear")

def draw_line():
    c = "\033[" +str(random.randint(31, 37)) +"m"
    h = random.randint(1, screen_size[0] +screen_size[1] -2)

    dir = random.randint(1, 2)

    if h > screen_size[0]:
        for i in range(1, screen_size[0] +1):
            draw(c +"|" +chr(random.randint(33, 126)) +"|\033[0m", (dir == 1 and i or (screen_size[0] -i +1), h -screen_size[0]))
            if i %8 == 0: time.sleep(.03)
    else:
        for i in range(1, screen_size[1] +1):
            draw(c +"%\033[0m", (h, dir == 1 and i or (screen_size[1] -i +1)))
            if i %40 == 0: time.sleep(.03)


print("initializing..")
time.sleep(1)

screen_size = get_screen_size()
screen_size[0] -= 1
screen_size[1] -= 1

clear()


while 1:
    draw_line()


#!/usr/bin/env python


import os, random, time


def get_screen_size():
    return [int(x) for x in os.popen("stty size", "r").read().split()]

def draw(txt, pos=0):
    print((pos and ("\033[" +str(pos[0]) +";" +str(pos[1]) +"H") or "") +txt)

def clear():
    os.system("clear")

def draw_x():
    c = "\033[" +str(random.randint(31, 37)) +"m"
    x, y = random.randint(1, screen_size[1] -1), random.randint(1, screen_size[0] -1)

    o = ["x", "+"][random.randint(0, 1)]
    draw(c +"\033[7m" +o +"\033[0m", (y, x))

    if o == "x":
        for i in range(1, max(screen_size) -2):
            w = 0
            if x -i > 0 and y -i > 0:
                draw(c +chr(92) +"\033[0m", (y -i, x -i))
                w = 1
            if x -i > 0 and y +i < screen_size[0]:
                draw(c +"/\033[0m", (y +i, x -i))
                w = 1
            if x +i < screen_size[1] and y +i < screen_size[0]:
                draw(c +chr(92) +"\033[0m", (y +i, x +i))
                w = 1
            if x +i < screen_size[1] and y -i > 0:
                draw(c +"/\033[0m", (y -i, x +i))
                w = 1

            if not w: break
            if i %12 == 0: time.sleep(.03)
    else:
        for i in range(1, max(screen_size) -2):
            w = 0
            if x -i > 0:
                draw(c +"-\033[0m", (y, x -i))
                w = 1
            if y +i < screen_size[0]:
                draw(c +"|\033[0m", (y +i, x))
                w = 1
            if x +i < screen_size[1]:
                draw(c +"-\033[0m", (y, x +i))
                w = 1
            if y -i > 0:
                draw(c +"|\033[0m", (y -i, x))
                w = 1

            if not w: break
            if i %40 == 0: time.sleep(.03)


print("initializing..")
time.sleep(1)

screen_size = get_screen_size()

clear()


while 1:
    draw_x()


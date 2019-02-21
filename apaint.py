

import curses, traceback
import os, time




def main(scr):
    global y, x

    curses.start_color()
    curses.use_default_colors()

    y, x = 0, 0
    corner = [0, 0]
    mode, scheme = 0, 0

    content = {}
    

    for i in range(7): curses.init_pair(i, i, 0)

    def bar_text(x, text, m=0):
        scr.addstr(scr.getmaxyx()[0] -1, x, text, m)

    def update_bar():
        bar_text(0, mode == 1 and "-- INSERT --" or mode == 2 and "-- VISUAL --" or " " *12, curses.A_BOLD)

        bar_text(scr.getmaxyx()[1] -16, str(y) +"," +str(x))
        bar_text(scr.getmaxyx()[1] -2, "#", curses.color_pair(scheme))


    def check_bounds():
        global y, x
        y = mode == -1 and (scr.getmaxyx()[0] -1) or min(max(y, 0), scr.getmaxyx()[0] -2)
        x = min(max(x, 0), scr.getmaxyx()[1] -2)

    update_bar()


    while 1:
        scr.move(y, x)
        c = scr.getch()

        bar_text(scr.getmaxyx()[1] -7, " " *4)
        bar_text(scr.getmaxyx()[1] -7, str(c))


        if c == 258: y += 1
        elif c == 259: y -= 1
        elif c == 260: x -= 1
        elif c == 261: x += 1

        elif c == 338: y = scr.getmaxyx()[0]
        elif c == 339: y = 0
        elif c == 262: x = 0
        elif c == 360: x = scr.getmaxyx()[1]

        if mode != 0:
            if c == 27: mode = 0

        if mode == 0:
            if c == 105 or c == 331: mode = 1
            elif c == 118:
                mode = 2
                corner = [y, x]
            elif c == 58:
                mode = -1
                scr.addstr(scr.getmaxyx()[0] -1, 0, ":")
                y, x = scr.getmaxyx()[0] -1, 1
        elif mode == 1:
            if c > 31 and c < 127:
                scr.addstr(y, x, chr(c), curses.color_pair(scheme))
                x += 1
            elif c == 330: scr.addstr(y, x, " ")
            elif c == 9: scheme = (scheme +1) %7
        elif mode == -1:
            if c > 31 and c < 127:
                scr.addstr(y, x, chr(c), curses.color_pair(scheme))
                x += 1
            elif c == 263:
                x -= 1
                scr.addstr(y, x, " ")


        check_bounds()
        update_bar()






curses.wrapper(main)

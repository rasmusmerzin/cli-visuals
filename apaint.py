

import curses, traceback
import os, time




def main(scr):
    curses.start_color()
    curses.use_default_colors()

    y, x = 0, 0
    scheme = 0

    for i in range(7): curses.init_pair(i, i, 0)
    for i in range(1, 8): curses.init_pair(6 +i, 0, i)

    def update_scheme(): scr.addstr(0, scr.getmaxyx()[1] -1, str(hex(scheme))[2:].upper(), curses.color_pair(scheme))

    update_scheme()

    while 1:
        scr.move(y, x)
        c = scr.getch()

        if c == 258:
            y += y < scr.getmaxyx()[0]-1 and 1 or 0
        elif c == 259:
            y -= y > 0 and 1 or 0
        elif c == 260:
            x -= x > 0 and 1 or 0
        elif c == 261:
            x += x < scr.getmaxyx()[1]-1 and 1 or 0
        elif c > 31 and c < 127:
            scr.addstr(y, x, chr(c), curses.color_pair(scheme))
        elif c == 9:
            scheme = (scheme +1) %14
            update_scheme()
        elif c == 330:
            scr.addstr(y, x, " ")
        else:
            scr.addstr(str(c))








curses.wrapper(main)

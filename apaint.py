

import curses, traceback
import os, time


lt = time.localtime(time.time())
timemark = "{0}-{1}-{2}_{3}-{4}-{5}".format(lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)


def main(scr):
    global y, x, autopush, content, colortable, bar_title, running, timemark, status

    curses.start_color()
    curses.use_default_colors()

    y, x = 0, 0
    shadow = [0, 0]
    mode, scheme = 0, 0
    bar_title = [""]
    autopush = ""
    running = 1
    status = 1

    content = {}
    colortable = {}
    

    for i in range(7): curses.init_pair(i, i, -1)

    def add_bar_text(x, text, m=0):
        scr.addstr(scr.getmaxyx()[0] -1, x, text, m)

    def update_bar_title(title="", bold=0):
        bar_title = [title, bold]
        add_bar_text(0, ("{:" +str(scr.getmaxyx()[1] -24) +"s}").format(title)[:scr.getmaxyx()[1] -24], bold and curses.A_BOLD)

    def update_bar_info():
        global status
        update_bar_title(*bar_title)
        if status:
            add_bar_text(scr.getmaxyx()[1] -20, ("{:18s}").format(str(y) +"," +str(x))[:18])
            add_bar_text(scr.getmaxyx()[1] -2, "#", curses.color_pair(scheme))
        else:
            add_bar_text(scr.getmaxyx()[1] -20, " " *19)


    def check_bounds():
        global y, x
        y = mode == -1 and (scr.getmaxyx()[0] -1) or min(max(y, 0), scr.getmaxyx()[0] -2)
        x = min(max(x, 0), scr.getmaxyx()[1] -2)

    def write_to_file(file_name="autosave_" +timemark +".txt"):
        text = [""] *2
        for i in range(2):
            mp = [content, colortable][i]
            brks = 0
            for y in range(scr.getmaxyx()[0] -1):
                if y in mp:
                    ln = mp[y].rstrip()
                    if len(ln) > 0:
                        text[i] += "\n" *brks +ln
                        brks = 0
                brks += 1
        bar_title = ["write to " +file_name +" & " +file_name +".colortable"]
        with open(file_name, "w") as f: f.write(text[0])
        if len(text[1]) > 0:
            with open(file_name +".colortable", "w") as f: f.write(text[1])

    def load_from_file(file_name="save"):
        try: 
            with open(file_name, "r") as f: pass
        except:
            bar_title[0] = "ERROR: no file in working directory named '{0}'".format(file_name)
            return

        h, w = scr.getmaxyx()[0] -2, scr.getmaxyx()[1] -2

        def colorize(f):
            lines = f.read().split("\n")
            for y in range(h):
                txt = " " *w
                if len(lines) > y:
                    txt = ("{:" +str(w) +"s}").format(lines[y])[:w]
                if y in content: content[y] = ("{:" +str(w) +"s}").format(content[y])[:w]
                else: content[y] = " " *w
                for x in range(w):
                    scr.addstr(y, x, content[y][x], curses.color_pair(int(txt[x].strip() or 0)))
                colortable[y] = txt

        if file_name.lower()[-11:] == ".colortable":
            with open(file_name, "r") as f: colorize(f)
        else:
            with open(file_name, "r") as f:
                lines = f.read().split("\n")
                for y in range(h):
                    txt = " " *w
                    if len(lines) > y:
                        txt = ("{:" +str(w) +"s}").format(lines[y])[:w]
                    scr.addstr(y, 0, txt)
                    content[y] = txt
            try:
                with open(file_name +".colortable", "r") as f: colorize(f)
            except: pass


    def execute(*cmd):
        global autopush, running, bar_title, status, content, colortable
        if cmd[0] == "autopush":
            if len(cmd) > 1: autopush = cmd[1]
            else: bar_title[0] = cmd[0] +": direction (D|U|L|R|-) required"
        elif cmd[0] == "status":
            status = 1 -status
            if not status:
                time.sleep(.1)
                bar_title[0] = ""
        elif cmd[0] == "q!": running = 0
        elif cmd[0] == "clear!":
            content, colortable = {}, {}
            scr.addstr(0, 0, ("\n" +" " *(scr.getmaxyx()[1] -1)) *(scr.getmaxyx()[0] -1))
        elif cmd[0] == "w" or cmd[0] == "write" or cmd[0] == "wq":
            if len(cmd) > 1: write_to_file(cmd[1])
            else: write_to_file()
            if cmd[0] == "wq": running = 0
        elif cmd[0] == "l" or cmd[0] == "load":
            if len(cmd) > 1: load_from_file(cmd[1])
            else: bar_title[0] = cmd[0] +": file name required"
        elif cmd[0] == "q" or cmd[0] == "exit" or cmd[0] == "quit": bar_title[0] = "use 'q!' or 'wq'"
        else: bar_title[0] = "no command '{0}'".format(cmd[0])

    update_bar_info()


    while running:
        scr.move(y, x)
        c = scr.getch()

        add_bar_text(scr.getmaxyx()[1] -7, " " *4)
        add_bar_text(scr.getmaxyx()[1] -7, str(c))


        if mode != -1:
            if c == 258: y += 1
            elif c == 259: y -= 1
            elif c == 260: x -= 1
            elif c == 261: x += 1

            elif c == 338: y = scr.getmaxyx()[0]
            elif c == 339: y = 0
            elif c == 262: x = 0
            elif c == 360: x = scr.getmaxyx()[1]

            shadow = [y, x]

        if mode != 0:
            if c == 27:
                mode = 0
                bar_title = [""]
                y, x = shadow[0], shadow[1]

        if mode == 0:
            if c == 105 or c == 331:
                mode = 1
                bar_title = ["-- INSERT --", 1]
            elif c == 115:
                mode = 2
                bar_title = ["-- SELECT --", 1]
                corner = [y, x]
            elif c == 58:
                mode = -1
                bar_title = [":"]
                y, x = scr.getmaxyx()[0] -1, 1
        elif mode == 1:
            if c > 31 and c < 127 or c == 330:
                char = c == 330 and " " or chr(c)
                
                byt = char
                for i in [content, colortable]:
                    txt = y in i and i[y] or ""
                    prev = txt[:scr.getmaxyx()[1] -2] +(" " *(scr.getmaxyx()[1] -2 -len(txt)))
                    i[y] = prev[:x] +byt +(len(prev) > x +1 and prev[x +1] or "")
                    byt = str(scheme == 0 and " " or scheme)

                scr.addstr(y, x, char, curses.color_pair(scheme))
                if c != 330:
                    y += autopush.count("d") -autopush.count("u")
                    x += autopush.count("r") -autopush.count("l")
            elif c == 9: scheme = (scheme +1) %7
        elif mode == -1:
            if c > 31 and c < 127:
                bar_title[0] += chr(c)
                x += 1
            elif c == 263:
                if len(bar_title[0]) > 1:
                    bar_title[0] = bar_title[0][:-1]
                    x -= 1
            elif c == 10: #ADD: or c == <numpad_enter>
                cmd = bar_title[0][1:]
                bar_title[0] = ">" +cmd
                execute(*cmd.lower().split())
                mode = 0
                y, x = shadow[0], shadow[1]


        check_bounds()
        update_bar_info()






curses.wrapper(main)

#!/usr/bin/env python3
from code import InteractiveConsole
import curses
import locale
import sys

# Note to anyone who wants to read through this file:
# curses' coordinate system generally uses Y first instead of your traditional
# X, Y coordinates. All coordinate arguments here are essentially reversed,
# with vertical coordinate being the first argument.


class CursesConsole(InteractiveConsole):

    # noinspection PyProtectedMember
    stdscr = None  # type: curses._CursesWindow

    def __init__(self, stdscr, *args, **kwargs):
        self.stdscr = stdscr

        super().__init__(*args, **kwargs)

    def write(self, data):
        for line in data.splitlines():  # this might be bad for writes without newlines
            pos = self.stdscr.getyx()

            self.stdscr.move(pos[0] + 1, 0)
            self.stdscr.clrtoeol()
            self.stdscr.addstr(line)

    def flush(self):
        pass  # bad idea? seems to work well enough.


class HISH:
    repl: CursesConsole

    # noinspection PyProtectedMember
    stdscr = None  # type: curses._CursesWindow

    cmd_continue = False
    do_prompt = True

    scroll = 0

    def run(self):
        def actual_init(_stdscr):
            self.stdscr = curses.newpad(curses.LINES * 2, curses.COLS)
            self.repl = CursesConsole(self.stdscr, filename="<hish>")

            sys.stdout = self.repl  # the write() method should be compatible

            self.stdscr.keypad(True)  # Get proper keys
            self.stdscr.scrollok(True)  # Scrolling is OK for our use case
            self.loop()

        locale.setlocale(locale.LC_ALL, "")
        curses.wrapper(actual_init)

    def loop(self):
        self.stdscr.addstr(0, 0, "# Highly Improved SHell - (c) 2020")

        self.stdscr.addstr(
            1, 0, "# Use arrow keys to move around, Enter to run a line."
        )

        self.stdscr.addstr(
            2, 0, "exit() # To exit. You can also press Enter on this line"
        )

        self.stdscr.move(3, 0)

        while True:
            if self.do_prompt:
                self.prompt()

            self.stdscr.refresh(self.scroll, 0, 0, 0, curses.LINES - 1, curses.COLS - 1)
            c = self.stdscr.get_wch()

            if type(c) == int or c in ["\n", "\t"]:
                self.handle_special_key(c)
            else:
                self.type_char(c)

    def type_char(self, char: str):
        self.stdscr.addstr(char)

    def handle_special_key(self, key: str):
        pos = self.stdscr.getyx()

        if key == curses.KEY_UP and pos[0] > 0:
            self.stdscr.move(pos[0] - 1, pos[1])
        elif key == curses.KEY_DOWN and pos[0] < curses.LINES - 1:
            self.stdscr.move(pos[0] + 1, pos[1])
        elif key == curses.KEY_LEFT and pos[1] >= 1:
            self.stdscr.move(pos[0], pos[1] - 1)
        elif key == curses.KEY_RIGHT and pos[1] < curses.COLS - 1:
            self.stdscr.move(pos[0], pos[1] + 1)
        elif key == curses.KEY_BACKSPACE and pos[1] >= 1:
            self.stdscr.addch(pos[0], pos[1] - 1, " ")
            self.stdscr.move(pos[0], pos[1] - 1)
        elif key == "\t" and pos[1] < curses.COLS - 1:
            self.stdscr.move(pos[0], pos[1] + 4)
        elif key == "\n":
            self.run_line()

    def prompt(self):
        self.do_prompt = False
        pos = self.stdscr.getyx()

        if pos[0] > curses.LINES - 3:
            self.scroll = (pos[0] - curses.LINES) + 3

        self.stdscr.move(pos[0] + 1, 0)
        self.stdscr.clrtoeol()
        self.stdscr.addstr("|" if self.cmd_continue else ">")

    def run_line(self):
        pos = self.stdscr.getyx()
        line = self.stdscr.instr(pos[0], 0, curses.COLS).decode()

        # remove prompt from input
        if line.startswith(">") or line.startswith("|"):
            line = line[1:]

        if self.cmd_continue:
            # continuation lines might have indentation, so only remove trailing whitesapce
            line = line.rstrip()
        else:
            line = line.strip()

        self.do_prompt = True
        self.cmd_continue = self.repl.push(line)


if __name__ == "__main__":
    HISH().run()

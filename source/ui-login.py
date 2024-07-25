#!/usr/bin/python3

import curses

screen = curses.initscr()

def initTerm():
    # Initialize terminal screen.
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    
    # Reset terminal screen (so it won't be messed up afterwards).
    curses.echo()
    curses.nocbreak()
    curses.keypad(False)
    curses.endwin()


# TODO: move to main.py (but for testing let it be here)
initTerm()

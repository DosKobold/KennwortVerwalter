#!/usr/bin/python3

import curses

screen = curses.initscr()

# Initialize terminal screen.
def initTerm():
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    
# Reset terminal screen (so it won't be messed up afterwards).
def resetTerm():
    curses.echo()
    curses.nocbreak()
    screen.keypad(False)
    curses.endwin()

def drawUsername():
    screen.addstr(6, 10, "Username:")

def drawPassword():
    screen.addstr(11, 10, "Password:")


# TODO: move to main.py (but for testing let it be here)
initTerm()
drawUsername()
drawPassword()
screen.refresh()

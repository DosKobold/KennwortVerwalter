#!/usr/bin/python3
import curses
import curses.textpad

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

def drawText():
    screen.addstr(6, 10, "Username:")
    screen.addstr(11, 10, "Password:")
    screen.refresh()

def drawInput():
    curses.flash()

    winUsername = curses.newwin(1, 30, 6, 22)
    winPassword = curses.newwin(1, 30, 11, 22)
    username = curses.textpad.Textbox(winUsername, insert_mode=True)
    password = curses.textpad.Textbox(winPassword, insert_mode=True)
    inputUsername = username.edit()
    inputPassword = password.edit()
    winUsername.clear()
    winPassword.clear()
    winUsername.refresh()
    winPassword.refresh()
    winUsername.getch()
    winPassword.getch()


# TODO: move to main.py (but for testing let it be here)
initTerm()
drawText()
drawInput()
screen.refresh()
#resetTerm()

#!/usr/bin/python3
"""
File: frontend.py
Desc: Implements the terminal based user interface to the application.
      Multiple screens are provided and can be drawn by calling the
      corresponding function.
"""

import curses
import curses.textpad

class Frontend:

    __screen = None

    # Initialize terminal screen.
    def __initTerm(self) -> None:
        self.__screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.__screen.keypad(True)

    # Reset terminal screen (so it won't be messed up afterwards).
    def resetTerm(self) -> None:
        curses.echo()
        curses.nocbreak()
        self.__screen.keypad(False)
        curses.endwin()

    def loginScreen(self) -> None:
        self.__initTerm()
        self.__screen.addstr(6, 10, "Username:")
        self.__screen.addstr(11, 10, "Password:")
        self.__screen.refresh()

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
frontend = Frontend()
frontend.loginScreen()
#resetTerm()

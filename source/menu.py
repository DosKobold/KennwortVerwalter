#!/usr/bin/env python

import curses
from curses import panel

class Menu:

    __items    = None
    __window   = None
    __panel    = None
    __position = None

    def __init__(self, items, screen):
        self.__window = screen.subwin(0, 0)
        self.__window.keypad(1)
        self.__panel = panel.new_panel(self.__window)
        self.__panel.hide()
        panel.update_panels()

        self.__position = 0
        self.__items = items

    def navigate(self, n: int) -> None:
        self.__position += n
        if self.__position < 0:
            self.__position = 0
        elif self.__position >= len(self.__items):
            self.__position = len(self.__items) - 1

    def display(self) -> None:
        self.__panel.top()
        self.__panel.show()
        self.__window.clear()

        while True:
            self.__window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.__items):
                if index == self.__position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = "%d. %s" % (index, item[0])
                self.__window.addstr(1 + index, 1, msg, mode)

            key = self.__window.getch()

            if key in [curses.KEY_ENTER, ord("\n")]:
                if self.__position == len(self.__items) - 1:
                    break
                else:
                    self.__items[self.__position][1]()

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.__window.clear()
        self.__panel.hide()
        panel.update_panels()
        curses.doupdate()

#!/usr/bin/env python3

import curses

class Popup:
    def __init__(self, screen: curses.window) -> None:
        self.screen = screen
        self.height = CURSES.LINES
        self.width  = CURSES.COLS

    def display_text(self, text: str) -> None:
        screen_height, screen_width = self.screen.getmaxyx()

        posY = (screen_height - self.height) // 2
        posX = (screen_width - self.width) // 2

        popup = curses.newwin(self.height, self.width, posY, posX)
        popup.border()

        text_y = self.height // 2
        text_x = (self.width - len(text)) // 2
        popup.addstr(text_y, text_x, text)
        popup.refresh()
        popup.getch()
        popup.clear()
        self.screen.refresh()

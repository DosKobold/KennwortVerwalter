#!/usr/bin/env python3
import curses
from typing import List, Optional

class SearchBar:
    def __init__(self, screen: curses.window, items: List[str]):
        self.__screen: curses.window = screen
        self.__items: List[str] = items
        self.__filtered_items: List[str] = items
        self.__query: str = ""

    def display(self) -> str:
        selected: str = ""

        self.__screen.clear()
        self.__screen.refresh()

        while True:
            self.__screen.clear()
            self.draw_search_bar()
            self.filter_items()
            self.display_results()

            key: int = self.__screen.getch()

            if key in (curses.KEY_EXIT, 27):
                break
            elif key in (curses.KEY_BACKSPACE, 127):
                self.__query = self.__query[:-1]
            elif key in (curses.KEY_ENTER, 10, 13):
                selected = self.handle_selection()
                break
            elif key in (curses.KEY_UP, curses.KEY_DOWN):
                continue
            else:
                self.__query += chr(key)
        return selected

    def draw_search_bar(self) -> None:
        self.__screen.addstr(0, 0, "Search: " + self.__query)
        self.__screen.refresh()

    def filter_items(self) -> None:
        self.__filtered_items = [item for item in self.__items if self.__query.lower() in item.lower()]

    def display_results(self) -> None:
        max_height: int
        max_width: int
        max_height, max_width = self.__screen.getmaxyx()
        for idx, item in enumerate(self.__filtered_items[:max_height - 2]):
            self.__screen.addstr(idx + 2, 0, item[:max_width - 1])
        self.__screen.refresh()

    def handle_selection(self) -> str:
        selected_item: str = ""
        if self.__filtered_items:
            selected_item = self.__filtered_items[0]
            self.__screen.clear()
            self.__screen.addstr(0, 0, f"Selected: {selected_item}")
            self.__screen.refresh()
            self.__screen.getch()
        return selected_item

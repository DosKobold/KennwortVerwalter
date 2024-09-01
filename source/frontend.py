#!/usr/bin/python3
"""
File: frontend.py
Desc: Implements the terminal based user interface to the application.
      Multiple screens are provided and can be drawn by calling the
      corresponding function.
"""

import curses
import curses.textpad
import os
from dataHandler import DataHandler
from search import SearchBar
from cryptor import Cryptor

class Frontend:
    __screen: curses.window
    dataHandler: DataHandler

    def __init__(self, dataHandler: DataHandler) -> None:
        self.dataHandler = dataHandler

    def __initTerm(self) -> None:
        self.__screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.__screen.keypad(True)

    def resetTerm(self) -> None:
        if self.__screen is not None:
            self.__screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def loginScreen(self) -> None:
        self.__initTerm()
        curses.curs_set(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.__screen.clear()
        self.__screen.refresh()

        # Title
        title = "Welcome to Password Manager"
        self.__screen.addstr(1, curses.COLS // 2 - len(title) // 2, title, curses.A_BOLD | curses.A_UNDERLINE)

        # File Path Input
        while True:
            path_prompt = "Enter path to database file (default: autoCreated.kwv): "
            path_y = 4
            path_x = curses.COLS // 2 - len(path_prompt) // 2
            self.__screen.addstr(path_y, path_x, path_prompt)
            self.__screen.refresh()
            curses.echo()
            db_path = self.get_input(self.__screen, path_y, path_x + len(path_prompt))
            if not db_path.strip():
                db_path = "autoCreated.kwv"
            curses.noecho()

            # Check if the file exists or can be created
            try:
                if not os.path.exists(db_path):
                    self.__screen.addstr(6, curses.COLS // 2 - 20, f"File {db_path} not found. Creating new file...", curses.A_BOLD)
                    self.__screen.refresh()
                    self.dataHandler.createFile(db_path, "default_user", "default_key")
                self.dataHandler.openFile(db_path)
                break  # Exit the loop if the path is valid
            except Exception as e:
                # Display error message
                error_message = f"Error: {str(e)} - Invalid path! Please try again."
                self.__screen.addstr(6, curses.COLS // 2 - len(error_message) // 2, error_message, curses.A_BOLD)
                self.__screen.refresh()
                self.__screen.getch()  # Wait for user to press a key

                # Clear the error message
                self.__screen.move(6, 0)
                self.__screen.clrtoeol()

        # User selection or creation
        users = self.dataHandler.getUsers()
        self.__screen.addstr(8, curses.COLS // 2 - 20, "Select a user or create a new one:", curses.A_BOLD)
        self.__screen.refresh()

        selected_user = self.select_user(users)

        # New user creation
        if selected_user == "create_new":
            self.__screen.clear()
            self.__screen.refresh()
            new_user_prompt = "Enter new username: "
            new_user_y = 10
            new_user_x = curses.COLS // 2 - len(new_user_prompt) // 2
            self.__screen.addstr(new_user_y, new_user_x, new_user_prompt)
            self.__screen.refresh()
            new_user = self.get_input(self.__screen, new_user_y, new_user_x + len(new_user_prompt))

            new_pass_prompt = "Enter new password: "
            new_pass_y = new_user_y + 2
            new_pass_x = curses.COLS // 2 - len(new_pass_prompt) // 2
            self.__screen.addstr(new_pass_y, new_pass_x, new_pass_prompt)
            self.__screen.refresh()
            new_pass = self.get_input(self.__screen, new_pass_y, new_pass_x + len(new_pass_prompt), password=True)

            self.dataHandler.addUser(new_user, self.dataHandler._DataHandler__cryptor.hashKey(new_pass, True))
            self.__screen.addstr(new_pass_y + 2, curses.COLS // 2 - 10, f"User {new_user} created.", curses.A_BOLD)
            self.__screen.refresh()
            self.__screen.getch()
            selected_user = new_user

        # Password input
        self.__screen.clear()
        self.__screen.refresh()
        password_prompt = f"Enter password for {selected_user}: "
        pass_y = 10
        pass_x = curses.COLS // 2 - len(password_prompt) // 2
        self.__screen.addstr(pass_y, pass_x, password_prompt)
        self.__screen.refresh()
        entered_password = self.get_input(self.__screen, pass_y, pass_x + len(password_prompt), password=True)

        # Authentication
        if self.dataHandler._DataHandler__cryptor.isCorrectKey(entered_password, self.dataHandler.getKey(selected_user)):
            self.dataHandler.startSession()
            self.__screen.addstr(pass_y + 2, pass_x, "Login successful! Press any key to continue.", curses.A_BOLD)
            self.__screen.refresh()
            self.__screen.getch()
            self.main_menu(self.__screen)
        else:
            self.__screen.addstr(pass_y + 2, pass_x, "Incorrect password! Press any key to exit.", curses.A_BOLD)
            self.__screen.refresh()
            self.__screen.getch()
            self.resetTerm()
            exit()

    def main_menu(self, stdscr: curses.window) -> None:
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        stdscr.clear()
        stdscr.refresh()

        current_row = 0
        menu: list[str] = [
            'Add Entry', 'View Entries', 'Edit Entry', 'Delete Entry', 
            'Delete Current User', 'Logout and Return to Login Screen', 'Exit'
        ]

        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()

            for idx, row in enumerate(menu):
                x = w // 2 - len(row) // 2
                y = h // 2 - len(menu) // 2 + idx
                if idx == current_row:
                    stdscr.attron(curses.color_pair(1))
                    stdscr.addstr(y, x, row)
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.addstr(y, x, row)

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                if current_row == 0:
                    self.add_entry(stdscr)
                elif current_row == 1:
                    self.view_entries(stdscr)
                elif current_row == 2:
                    self.edit_entry(stdscr)
                elif current_row == 3:
                    self.delete_entry(stdscr)
                elif current_row == 4:
                    self.delete_current_user(stdscr)
                elif current_row == 5:
                    self.back_to_login(stdscr)
                elif current_row == 6:
                    self.resetTerm()
                    break

            stdscr.refresh()
    
        exit()

    def ensure_default_category(self) -> None:
        categories = self.dataHandler.getCategories()
        if "default" not in categories:
            self.dataHandler.addCategory("default")

    def add_entry(self, stdscr: curses.window) -> None:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()

        fields = [("Title: ", 2, 0), ("Username: ", 3, 0), ("Password: ", 4, 0),
                  ("URL: ", 5, 0), ("Notes: ", 6, 0)]
        inputs: list[str] = []

        for field, y, x in fields:
            stdscr.addstr(y, x, field)
            stdscr.refresh()
            input_value = self.get_input(stdscr, y, x + len(field))
            inputs.append(input_value)

        title, username, password, url, notes = inputs
        timestamp = "2024-07-28"

        self.ensure_default_category()

        self.dataHandler.addEntry("default", title, username, password, url, notes, timestamp)

        stdscr.addstr(8, 0, "Entry added! Press any key to return to the main menu.")
        stdscr.getch()

    def get_input(self, stdscr: curses.window, y: int, x: int, password: bool = False) -> str:
        curses.noecho()
        max_width = curses.COLS
        win = curses.newwin(1, max_width, y, x) 
        win.keypad(True)
        curses.curs_set(1)
        box: list[str] = []

        while True:
            key = win.get_wch()
            
            if isinstance(key, str) and key in ("\n", "\r"):  # Enter key
                break

            elif key == 263:  # Backspace key
                if len(box) > 0:
                    box.pop()  
                    win.clear()  
                    display_text = ''.join(['*' if password else c for c in box])  # Masked input
                    win.addstr(0, 0, display_text)  
                    win.move(0, len(box)) 

            elif isinstance(key, str) and key.isprintable():
                box.append(key)  
                display_text = ''.join(['*' if password else c for c in box])  

                # Display
                win.clear()
                win.addstr(0, 0, display_text)
                win.move(0, len(display_text))

            win.refresh()

        curses.curs_set(0)
        return ''.join(box)

    def select_user(self, users: list[str]) -> str:
        self.__screen.clear()
        self.__screen.refresh()
        
        title = "Select a User"
        self.__screen.addstr(1, curses.COLS // 2 - len(title) // 2, title, curses.A_BOLD | curses.A_UNDERLINE)
        
        menu_items = users + ["Create New User"]
        current_row = 0

        while True:
            self.__screen.clear()
            h, w = self.__screen.getmaxyx()

            # Display the user selection menu
            for idx, user in enumerate(menu_items):
                x = w // 2 - len(user) // 2
                y = h // 2 - len(menu_items) // 2 + idx
                if idx == current_row:
                    self.__screen.attron(curses.color_pair(1))
                    self.__screen.addstr(y, x, user)
                    self.__screen.attroff(curses.color_pair(1))
                else:
                    self.__screen.addstr(y, x, user)

            self.__screen.refresh()
            key = self.__screen.getch()

            # Navigate the menu
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
                current_row += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                # If "Create New User" is selected, return a special string
                if current_row == len(menu_items) - 1:
                    return "create_new"
                else:
                    return menu_items[current_row]

    def view_entries(self, stdscr: curses.window) -> None:
        items: list[str] = []

        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()

        self.ensure_default_category()

        stdscr.addstr(4, 10, "search: ")
        categories = self.dataHandler.getCategories()
        for cat in categories:
            items += self.dataHandler.getEntries(cat)
        search_bar = SearchBar(stdscr, items)
        search_bar.display()
        stdscr.addstr(len(entries) + 8, 0, "Press any key to return to the main menu.")
        stdscr.getch()

    def edit_entry(self, stdscr: curses.window) -> None:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr(0, 0, "Edit Entry")

        self.ensure_default_category()

        entries = self.dataHandler.getEntries("default")

        if not entries:
            stdscr.addstr(2, 0, "No entries to edit in the 'default' category.")
            stdscr.addstr(4, 0, "Press any key to return to the main menu.")
            stdscr.getch()
            return

        stdscr.addstr(2, 0, "Select an entry to edit:")
        for idx, entry in enumerate(entries):
            if isinstance(entry, dict):
                stdscr.addstr(3 + idx, 0, f"{idx + 1}. {entry['title']}")

        selected_index = int(self.get_input(stdscr, 3 + len(entries), 0)) - 1
        selected_entry = entries[selected_index]

        stdscr.addstr(4 + len(entries), 0, "Enter property to change (title, name, password, url, notices, timestamp): ")
        prop = self.get_input(stdscr, 5 + len(entries), 0)

        stdscr.addstr(6 + len(entries), 0, "Enter new value: ")
        value = self.get_input(stdscr, 7 + len(entries), 0)

        self.dataHandler.changeEntry("default", selected_entry['title'], prop, value)

        stdscr.addstr(9 + len(entries), 0, "Entry updated! Press any key to return to the main menu.")
        stdscr.getch()

    def delete_entry(self, stdscr: curses.window) -> None:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr(0, 0, "Delete Entry")

        stdscr.addstr(2, 0, "Enter entry title to delete: ")
        title = self.get_input(stdscr, 2, 20)

        self.ensure_default_category()

        entries = self.dataHandler.getEntries("default")

        for idx, entry in enumerate(entries):
            if isinstance(entry, dict) and "title" in entry and entry["title"] == title:
                entries.pop(idx)
                break

        stdscr.addstr(4, 0, "Entry deleted! Press any key to return to the main menu.")
        stdscr.getch()

    def delete_current_user(self, stdscr: curses.window) -> None:
        stdscr.clear()
        stdscr.addstr(0, 0, "Delete Current User")
        stdscr.addstr(2, 0, "Are you sure you want to delete your account? (y/n): ")
        choice = stdscr.get_wch()

        if choice in ('y', 'Y'):
            self.dataHandler.remUser()
            stdscr.addstr(4, 0, "User deleted! Press any key to exit.")
            stdscr.getch()
            self.loginScreen()
        else:
            stdscr.addstr(4, 0, "Cancelled. Press any key to return to the main menu.")
            stdscr.getch()

    def back_to_login(self, stdscr: curses.window) -> None:
        # Close the current session if open
        self.dataHandler.closeSession()
        # Clear the screen and reinitialize the login process
        stdscr.clear()
        stdscr.refresh()
        self.loginScreen()

def main() -> None:
    cryptor = Cryptor()
    
    dataHandler = DataHandler(cryptor)
    
    frontend = Frontend(dataHandler)
    
    # Startet den erweiterten Login-Screen, der Pfadangabe, Nutzerverwaltung und Login enthält
    frontend.loginScreen()
    
    # Wenn der Login erfolgreich war, startet das Hauptmenü
    curses.wrapper(frontend.main_menu)
    
    # Session wird geschlossen, nachdem der Benutzer das Hauptmenü verlässt
    dataHandler.closeSession()
    print("Session closed.")
    
if __name__ == "__main__":
    main()

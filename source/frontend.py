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
    __dataHandler: DataHandler

    def __init__(self, dataHandler: DataHandler) -> None:
        self.__dataHandler = dataHandler

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
            db_path = self.get_input(path_y, path_x + len(path_prompt))
            if not db_path.strip():
                db_path = "autoCreated.kwv"
            curses.noecho()

            # Check if the file exists or can be created
            try:
                if not os.path.exists(db_path):
                    self.__screen.addstr(6, curses.COLS // 2 - 20, f"File {db_path} not found. Creating new file...", curses.A_BOLD)
                    self.__screen.refresh()
                    self.__dataHandler.createFile(db_path, "default_user", "default_key")
                self.__dataHandler.openFile(db_path)
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
        users = self.__dataHandler.getUsers()
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
            new_user = self.get_input(new_user_y, new_user_x + len(new_user_prompt))

            new_pass_prompt = "Enter new password: "
            new_pass_y = new_user_y + 2
            new_pass_x = curses.COLS // 2 - len(new_pass_prompt) // 2
            self.__screen.addstr(new_pass_y, new_pass_x, new_pass_prompt)
            self.__screen.refresh()
            new_pass = self.get_input(new_pass_y, new_pass_x + len(new_pass_prompt), password=True)

            self.__dataHandler.addUser(new_user, self.__dataHandler._DataHandler__cryptor.hashKey(new_pass, True))
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
        entered_password = self.get_input(pass_y, pass_x + len(password_prompt), password=True)

        # Authentication
        if self.__dataHandler._DataHandler__cryptor.isCorrectKey(entered_password, self.__dataHandler.getKey(selected_user)):
            self.__dataHandler.startSession()
            self.__screen.addstr(pass_y + 2, pass_x, "Login successful! Press any key to continue.", curses.A_BOLD)
            self.__screen.refresh()
            self.__screen.getch()
            self.main_menu()
        else:
            self.__screen.addstr(pass_y + 2, pass_x, "Incorrect password! Press any key to exit.", curses.A_BOLD)
            self.__screen.refresh()
            self.__screen.getch()
            self.resetTerm()
            exit()

    def main_menu(self) -> None:
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self.__screen.clear()
        self.__screen.refresh()

        current_row = 0
        menu: list[str] = [
            'Add Entry', 'View Entries', 'Edit Entry', 'Delete Entry', 
            'Delete Current User', 'Logout and Return to Login Screen', 'Exit'
        ]

        while True:
            self.__screen.clear()
            h, w = self.__screen.getmaxyx()

            for idx, row in enumerate(menu):
                x = w // 2 - len(row) // 2
                y = h // 2 - len(menu) // 2 + idx
                if idx == current_row:
                    self.__screen.attron(curses.color_pair(1))
                    self.__screen.addstr(y, x, row)
                    self.__screen.attroff(curses.color_pair(1))
                else:
                    self.__screen.addstr(y, x, row)

            key = self.__screen.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
            elif key in (curses.KEY_ENTER, 10, 13):
                if current_row == 0:
                    self.add_entry()
                elif current_row == 1:
                    self.view_categories()
                elif current_row == 2:
                    self.edit_entry()
                elif current_row == 3:
                    self.delete_entry()
                elif current_row == 4:
                    self.delete_current_user()
                elif current_row == 5:
                    self.back_to_login()
                elif current_row == 6:
                    self.resetTerm()
                    break

            self.__screen.refresh()
    
        exit()

    def ensure_default_category(self) -> None:
        categories = self.__dataHandler.getCategories()
        if "default" not in categories:
            self.__dataHandler.addCategory("default")

    def add_entry(self) -> None:
        curses.curs_set(1)
        self.__screen.clear()
        self.__screen.refresh()

        fields = [("Title: ", 2, 0), ("Username: ", 3, 0), ("Password: ", 4, 0),
                  ("URL: ", 5, 0), ("Notes: ", 6, 0)]
        inputs: list[str] = []

        for field, y, x in fields:
            self.__screen.addstr(y, x, field)
            self.__screen.refresh()
            input_value = self.get_input(y, x + len(field))
            inputs.append(input_value)

        title, username, password, url, notes = inputs
        timestamp = "2024-07-28"

        self.ensure_default_category()

        self.__dataHandler.addEntry("default", title, username, password, url, notes, timestamp)

        self.__screen.addstr(8, 0, "Entry added! Press any key to return to the main menu.")
        self.__screen.getch()

    def get_input(self, y: int, x: int, password: bool = False) -> str:
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

    def view_categories(self) -> None:
        curses.curs_set(0)
        current_selection = 0
        
        self.ensure_default_category()
        items = self.__dataHandler.getCategories()

        while True:
            self.__screen.clear()
    
            max_height, max_width = self.__screen.getmaxyx()
    
            total_width = sum(len(item) + 4 for item in items) - 1
            start_x = (max_width // 2) - (total_width // 2)
            y_position = 0
            
            current_x = start_x
            
            for idx, item in enumerate(items):
                item_with_padding = f"[ {item} ]"
                if idx == current_selection:
                    self.__screen.attron(curses.A_REVERSE)
                    self.__screen.addstr(y_position, current_x, item_with_padding)
                    self.__screen.attroff(curses.A_REVERSE)
                else:
                    self.__screen.addstr(y_position, current_x, item_with_padding)
                current_x += len(item_with_padding) + 1
    
            key = self.__screen.getch()
    
            if key in (curses.KEY_ENTER, 10, 13):
                self.view_entries(items[current_selection])
            elif key == curses.KEY_LEFT and current_selection > 0:
                current_selection -= 1
            elif key == curses.KEY_RIGHT and current_selection < len(items) - 1:
                current_selection += 1
            elif key in (27, curses.KEY_EXIT):
                break
    
            self.__screen.refresh()

    def view_entries(self, category: str) -> None:
        curses.curs_set(0)
        self.__screen.clear()
        self.__screen.refresh()
        self.__screen.addstr(4, 10, "search: ")

        items: list[str] = self.__dataHandler.getEntries(category)
        search_bar = SearchBar(self.__screen, items)
        search_bar.display()
        self.__screen.addstr(len(items) + 8, 0, "Press any key to return to the main menu.")
        self.__screen.getch()

    def edit_entry(self) -> None:
        curses.curs_set(1)
        self.__screen.clear()
        self.__screen.refresh()
        self.__screen.addstr(0, 0, "Edit Entry")

        self.ensure_default_category()

        entries = self.__dataHandler.getEntries("default")

        if not entries:
            self.__screen.addstr(2, 0, "No entries to edit in the 'default' category.")
            self.__screen.addstr(4, 0, "Press any key to return to the main menu.")
            self.__screen.getch()
            return

        self.__screen.addstr(2, 0, "Select an entry to edit:")
        for idx, entry in enumerate(entries):
            if isinstance(entry, dict):
                self.__screen.addstr(3 + idx, 0, f"{idx + 1}. {entry['title']}")

        selected_index = int(self.get_input(3 + len(entries), 0)) - 1
        selected_entry = entries[selected_index]

        self.__screen.addstr(4 + len(entries), 0, "Enter property to change (title, name, password, url, notices, timestamp): ")
        prop = self.get_input(5 + len(entries), 0)

        self.__screen.addstr(6 + len(entries), 0, "Enter new value: ")
        value = self.get_input(7 + len(entries), 0)

        self.__dataHandler.changeEntry("default", selected_entry['title'], prop, value)

        self.__screen.addstr(9 + len(entries), 0, "Entry updated! Press any key to return to the main menu.")
        self.__screen.getch()

    def delete_entry(self) -> None:
        curses.curs_set(1)
        self.__screen.clear()
        self.__screen.refresh()
        self.__screen.addstr(0, 0, "Delete Entry")

        self.__screen.addstr(2, 0, "Enter entry title to delete: ")
        title = self.get_input(2, 20)

        self.ensure_default_category()

        entries = self.__dataHandler.getEntries("default")

        for idx, entry in enumerate(entries):
            if isinstance(entry, dict) and "title" in entry and entry["title"] == title:
                entries.pop(idx)
                break

        self.__screen.addstr(4, 0, "Entry deleted! Press any key to return to the main menu.")
        self.__screen.getch()

    def delete_current_user(self) -> None:
        self.__screen.clear()
        self.__screen.addstr(0, 0, "Delete Current User")
        self.__screen.addstr(2, 0, "Are you sure you want to delete your account? (y/n): ")
        choice = self.__screen.get_wch()

        if choice in ('y', 'Y'):
            self.__dataHandler.remUser()
            self.__screen.addstr(4, 0, "User deleted! Press any key to exit.")
            self.__screen.getch()
            self.loginScreen()
        else:
            self.__screen.addstr(4, 0, "Cancelled. Press any key to return to the main menu.")
            self.__screen.getch()

    def back_to_login(self) -> None:
        # Close the current session if open
        self.__dataHandler.closeSession()
        # Clear the screen and reinitialize the login process
        self.__screen.clear()
        self.__screen.refresh()
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

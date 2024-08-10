#!/usr/bin/python3
"""
File: frontend.py
Desc: Implements the terminal based user interface to the application.
      Multiple screens are provided and can be drawn by calling the
      corresponding function.
"""

import curses
import curses.textpad
import os  # Hinzufügen des Imports für das os-Modul
import getpass  # Hinzufügen des Imports für getpass
from dataHandler import DataHandler
from cryptor import Cryptor
from typing import Any, List

class Frontend:
    __screen: Any
    data_handler: DataHandler

    def __init__(self, data_handler: DataHandler) -> None:
        self.data_handler = data_handler

    # Initialize terminal screen.
    def __initTerm(self) -> None:
        self.__screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.__screen.keypad(True)

    # Reset terminal screen (so it won't be messed up afterwards).
    def resetTerm(self) -> None:
        if self.__screen is not None:
            self.__screen.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def loginScreen(self) -> None:
        self.__initTerm()
        self.__screen.addstr(3, 35, "KennwortVerwaltung", curses.A_UNDERLINE)
        self.__screen.addstr(8, 10, "Username:")
        self.__screen.addstr(13, 10, "Password:")
        self.__screen.refresh()

        winUsername = curses.newwin(1, 30, 8, 22)
        winPassword = curses.newwin(1, 30, 13, 22)
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

    def main_menu(self, stdscr: Any) -> None:
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        stdscr.clear()
        stdscr.refresh()

        current_row = 0
        menu: List[str] = [
            'Add Entry', 'View Entries', 'Edit Entry', 'Delete Entry', 
            'Exit'
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
                    break

            stdscr.refresh()

    def ensure_default_category(self) -> None:
        """Ensure that the default category exists."""
        categories = self.data_handler.getCategories()
        if "default" not in categories:
            self.data_handler.addCategory("default")

    def add_entry(self, stdscr: Any) -> None:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()

        # Set up input fields
        fields = [("Title: ", 2, 0), ("Username: ", 3, 0), ("Password: ", 4, 0),
                  ("URL: ", 5, 0), ("Notes: ", 6, 0)]
        inputs: List[str] = []

        for field, y, x in fields:
            stdscr.addstr(y, x, field)
            stdscr.refresh()
            input_value = self.get_input(stdscr, y, x + len(field))
            inputs.append(input_value)

        title, username, password, url, notes = inputs
        timestamp = "2024-07-28"  # Hier könnte eine aktuelle Zeitstempel-Funktion hinzugefügt werden

        self.ensure_default_category()

        self.data_handler.addEntry("default", title, username, password, url, notes, timestamp)

        stdscr.addstr(8, 0, "Entry added! Press any key to return to the main menu.")
        stdscr.getch()

    def get_input(self, stdscr: Any, y: int, x: int) -> str:
        curses.noecho()
        win = curses.newwin(1, 30, y, x)
        win.keypad(True)
        curses.curs_set(1)
        box: List[str] = []
        pos = 0  # Cursor-Position

        while True:
            key = win.getch()

            if key in (curses.KEY_ENTER, 10, 13):  # Enter key
                break
            elif key in (curses.KEY_BACKSPACE, 8, 127):  # Backspace key
                if pos > 0:
                    pos -= 1  # Bewegt die Cursor-Position nach links
                    box.pop(pos)  # Entfernt das Zeichen an der aktuellen Position
                    win.move(0, 0)
                    win.clrtoeol()  # Löscht die Zeile, um sicherzustellen, dass das Zeichen entfernt wird
                    win.addstr(0, 0, ''.join(box))  # Zeigt die verbleibenden Zeichen an
                    win.move(0, pos)  # Bewegt den Cursor zurück an die richtige Position
            elif 32 <= key <= 126:  # Zeichenbare Zeichen
                if len(box) < 30:  # Sicherstellen, dass wir die Fensterbreite nicht überschreiten
                    box.insert(pos, chr(key))  # Fügt das Zeichen an der aktuellen Position hinzu
                    pos += 1  # Bewegt die Cursor-Position nach rechts
                    win.clear()  # Löscht das Eingabefeld
                    win.addstr(0, 0, ''.join(box))  # Zeigt die aktuelle Eingabe an
                    win.move(0, pos)  # Setzt den Cursor an die neue Position

            win.refresh()

        curses.curs_set(0)
        return ''.join(box)

    def view_entries(self, stdscr: Any) -> None:
        curses.curs_set(0)
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr(0, 0, "View Entries")

        self.ensure_default_category()

        entries = self.data_handler.getEntries("default")

        for idx, entry in enumerate(entries):
            if isinstance(entry, dict):
                stdscr.addstr(2 + idx, 0, f"{idx + 1}. {entry['title']} - {entry['name']}")
            else:
                stdscr.addstr(2 + idx, 0, f"{idx + 1}. {entry}")

        stdscr.addstr(len(entries) + 2, 0, "Press any key to return to the main menu.")
        stdscr.getch()

    def edit_entry(self, stdscr: Any) -> None:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr(0, 0, "Edit Entry")

        # Zuerst die Kategorie überprüfen und sicherstellen, dass die "default"-Kategorie existiert
        self.ensure_default_category()

        # Einträge in der "default"-Kategorie abrufen
        entries = self.data_handler.getEntries("default")

        # Falls keine Einträge vorhanden sind, Benutzer informieren und zurückkehren
        if not entries:
            stdscr.addstr(2, 0, "No entries to edit in the 'default' category.")
            stdscr.addstr(4, 0, "Press any key to return to the main menu.")
            stdscr.getch()
            return

        # Die Liste der Einträge anzeigen
        stdscr.addstr(2, 0, "Select an entry to edit:")
        for idx, entry in enumerate(entries):
            stdscr.addstr(3 + idx, 0, f"{idx + 1}. {entry['title']}")

        # Benutzer wählt einen Eintrag aus
        selected_index = int(self.get_input(stdscr, 3 + len(entries), 0)) - 1
        selected_entry = entries[selected_index]

        # Benutzer gibt die zu ändernde Eigenschaft und den neuen Wert ein
        stdscr.addstr(4 + len(entries), 0, "Enter property to change (title, name, password, url, notices, timestamp): ")
        prop = self.get_input(stdscr, 5 + len(entries), 0)

        stdscr.addstr(6 + len(entries), 0, "Enter new value: ")
        value = self.get_input(stdscr, 7 + len(entries), 0)

        # Aktualisierung des Eintrags
        self.data_handler.changeEntry("default", selected_entry['title'], prop, value)

        stdscr.addstr(9 + len(entries), 0, "Entry updated! Press any key to return to the main menu.")
        stdscr.getch()


    def delete_entry(self, stdscr: Any) -> None:
        curses.curs_set(1)
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr(0, 0, "Delete Entry")

        stdscr.addstr(2, 0, "Enter entry title to delete: ")
        title = self.get_input(stdscr, 2, 20)

        self.ensure_default_category()

        entries = self.data_handler.getEntries("default")

        for idx, entry in enumerate(entries):
            if isinstance(entry, dict) and "title" in entry and entry["title"] == title:
                entries.pop(idx)
                break

        stdscr.addstr(4, 0, "Entry deleted! Press any key to return to the main menu.")
        stdscr.getch()

def main() -> None:
    print("Initializing Cryptor...")
    cryptor = Cryptor()
    print("Cryptor initialized.")
    
    print("Initializing DataHandler...")
    data_handler = DataHandler(cryptor)
    print("DataHandler initialized.")
    
    # Dateiname
    file_name = "autoCreated.kwv"
    
    # Prüfen, ob die Datei existiert, und bei Bedarf erstellen
    if os.path.exists(file_name):
        print(f"{file_name} exists. Deleting file...")
        os.remove(file_name)
    
    print(f"{file_name} does not exist. Creating file...")
    # Datei erstellen mit einem Beispielbenutzer und einem Beispielpasswort
    data_handler.createFile(file_name, "paul", cryptor.hashKey("test123", True))
    print(f"File {file_name} created.")
    
    print(f"Opening file {file_name}...")
    data_handler.openFile(file_name)
    print(f"File {file_name} opened.")
    
    master_password = getpass.getpass("Enter your master password: ")
    print("Master password entered.")
    
    if cryptor.isCorrectKey(master_password, data_handler.getKey("paul")):
        print("Master password is correct.")
        data_handler.startSession()
        print("Session started.")
        
        frontend = Frontend(data_handler)
        curses.wrapper(frontend.main_menu)
        
        data_handler.closeSession()
        print("Session closed.")
    else:
        print("Incorrect master password.")

if __name__ == "__main__":
    main()

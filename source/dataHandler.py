#!/bin/python3
"""
File: datahandler.py
Desc: Implements a simple interface for datahandling. Handles files, its content and the processed
      data.
"""

import sys
import csv
import json
import cryptor
import objectAlreadyExistsException

class DataHandler:
    """Class for handling data"""

    def __init__(self, otherCryptor: cryptor.Cryptor) -> None:
        self.__cryptor = otherCryptor
        self.__path: str
        self.__user: str
        self.__entries: dict[str, dict[str, dict[str, str]]]
        self.__oldPasswords: list[str]
        self.__sessionIsOpen = False
        self.__fileIsOpen = False
        self.__keyIsSet = False

    def __ifSessionIsNotOpen(self, msg: str) -> None:
        if self.__sessionIsOpen is False:
            print(msg)
            sys.exit(1)

    def __ifFileIsNotOpen(self, msg: str) -> None:
        if self.__fileIsOpen is False:
            print(msg)
            sys.exit(1)

    def __getFileContent(self) -> list[dict [str, str]]:
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
        return data

    def getCryptor(self) -> cryptor.Cryptor:
        return self.__cryptor

    def getPath(self) -> str:
        return self.__path

    def createFile(self, path: str, user: str, key: str) -> None:
        """0th step: create file"""
        with open(path, "w", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["account", "key", "data"])
            writer.writerow([user.replace(',',''), key, self.__cryptor.encryptText("{\"entries\":{},\"oldPasswords\":[]}")])

    def openFile(self, path: str,) -> None:
        """1st step: open a file"""
        self.__path = path
        self.__fileIsOpen = True

    def startSession(self) -> None:
        """5th step: hold the decrypted data in memory"""
        if self.__keyIsSet is False:
            print("Key is not set! Wrong order of calls!")
            sys.exit(1)
        data = self.__getFileContent()
        for dictonary in data:
            if dictonary["account"] == self.__user:
                encryptedData = dictonary["data"]
                break
        jsonData = json.loads(self.__cryptor.decryptText(encryptedData))
        self.__entries = jsonData["entries"]
        self.__oldPasswords = jsonData["oldPasswords"]
        self.__sessionIsOpen = True

    def closeSession(self) -> None:
        """last step: write the encrypted data and close the file"""
        self.__ifSessionIsNotOpen("No session to close! Wrong order of calls!")
        data = self.__getFileContent()
        for dictonary in data:
            if dictonary["account"] == self.__user:
                dictonary["data"] = self.__cryptor.encryptText(json.dumps({"entries":self.__entries, "oldPasswords":self.__oldPasswords}))
                break
        with open(self.__path, "w", encoding="utf-8") as file:
            fieldnames = ["account", "key", "data"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for dictonary in data:
                writer.writerow(dictonary)
        self.__path = ""
        self.__user = ""
        self.__entries = {}
        self.__oldPasswords = []
        self.__sessionIsOpen = False
        self.__fileIsOpen = False
        self.__keyIsSet = False

    def saveEntries(self) -> None:
        data = self.__getFileContent()
        for dictonary in data:
            if dictonary["account"] == self.__user:
                dictonary["data"] = self.__cryptor.encryptText(json.dumps({"entries":self.__entries, "oldPasswords":self.__oldPasswords}))
                break
        with open(self.__path, "w", encoding="utf-8") as file:
            fieldnames = ["account", "key", "data"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for dictonary in data:
                writer.writerow(dictonary)

    def getUsers(self) -> list[str]:
        """2nd step: get all users"""
        self.__ifFileIsNotOpen("No file opened! Wrong order of calls!")
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row["account"])
        return data

    def addUser(self, user: str, key: str) -> None:
        """3rd step: add a user"""
        self.__ifFileIsNotOpen("No file opened! Wrong order of calls!")
        if user in self.getUsers():
            raise objectAlreadyExistsException.ObjectAlreadyExistsException
        with open(self.__path, "a", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow([user.replace(',',''), key, self.__cryptor.encryptText("{\"entries\":{},\"oldPasswords\":[]}")])

    def remUser(self) -> None:
        """6th step: remove the choosen user"""
        self.__ifFileIsNotOpen("No file opened! Wrong order of calls!")
        data = self.__getFileContent()
        dataCopy = data
        for dictonary in dataCopy:
            if dictonary["account"] == self.__user:
                data.remove(dictonary)
                break
        with open(self.__path, "w", encoding="utf-8") as file:
            fieldnames = ["account", "key", "data"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for dictonary in data:
                writer.writerow(dictonary)
        self.__path = ""
        self.__user = ""
        self.__entries = {}
        self.__oldPasswords = []
        self.__sessionIsOpen = False
        self.__fileIsOpen = False
        self.__keyIsSet = False

    def getKey(self, user:str) -> str:
        """3rd step: get the key of the user"""
        self.__ifFileIsNotOpen("No file opened! Wrong order of calls!")
        self.__user = user
        data = self.__getFileContent()
        for dictonary in data:
            if dictonary["account"] == user:
                key = dictonary["key"]
                break
        self.__keyIsSet = True
        return key

    def getCategories(self) -> list[str]:
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        return list(self.__entries.keys())

    def addCategory(self, category: str) -> None:
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        if category in self.__entries.keys():
            raise objectAlreadyExistsException.ObjectAlreadyExistsException
        self.__entries[category] = {}

    def remCategory(self, category: str) -> None:
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        del self.__entries[category]

    def getEntries(self, category: str) -> list[str]:
        """6th step: get all entries of one category"""
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        return list(self.__entries[category].keys())

    def getEntry(self, category: str, title: str) -> dict[str, str]:
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        return self.__entries[category][title]

    def addEntry(self, category: str, title: str, name: str, password: str, url: str, notices: str, timestamp: str) -> None:
        """6th step add an entry"""
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        if title in self.__entries[category].keys():
            raise objectAlreadyExistsException.ObjectAlreadyExistsException
        self.__entries[category][title] = {
            "name": name,
            "password": password,
            "url": url,
            "notices": notices,
            "timestamp": timestamp
        }

    def changeEntry(self, category: str, title: str, prop: str, value: str) -> None:
        """6th step: change and entry"""
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        self.__entries[category][title][prop] = value

    def searchEntry(self, keyWord: str) -> dict[str, list[str]]:
        """6th step: Search an entry with a given keyword and returns the found entry"""
        result: dict[str, list[str]] = {}
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        for category in self.__entries.keys():
            for title in self.__entries[category].keys():
                for prop in self.__entries[category][title].keys():
                    if keyWord in self.__entries[category][title][prop] or keyWord in title or keyWord in category:
                        #Have to check keys, not values
                        if not category in result.keys(): #pylint: disable=consider-iterating-dictionary
                            result[category] = []
                        if not title in result[category]:
                            result[category].append(title)
        return result

    def remEntry(self, category: str, title: str) -> None:
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        del self.__entries[category][title]

    def getOldPasswords(self) -> list[str]:
        """6th step: get all old password"""
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        return self.__oldPasswords

    def addOldPassword(self, oldPassword: str) -> None:
        """6th step: add an old password"""
        self.__ifSessionIsNotOpen("No session opened! Wrong order of calls!")
        self.__oldPasswords.append(oldPassword)
        if len(self.__oldPasswords) > 10:
            del self.__oldPasswords[0]

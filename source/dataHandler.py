#!/bin/python3
"""
File: datahandler.py
Desc: Implements a simple interface for the main.
"""

import csv
import json
import cryptor
from typing import List

class DataHandler:
    """Class for handling data"""

    __path: str
    __user: str
    __entries: dict[str, dict[str, dict[str, str]]]
    __oldPasswords: list[str]
    __cryptor: cryptor.Cryptor()

    def __init__(self, cryptor: cryptor.Cryptor()) -> None:
        self.__cryptor = cryptor

    def createFile(self, path: str, user: str, key: str) -> None:
        """0th step: create file"""
        with open(path, "w", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["account", "key", "data"])
            writer.writerow([user, key, self.__cryptor.encryptText("{\"entries\":{\"EgCategory\":{\"Example\":{\"name\":\"Example\",\"password\":\"Example\",\"url\":\"Example\",\"notices\":\"Example\",\"timestamp\":\"Example\"}}},\"oldPasswords\":[\"Example\",\"Example2\"]}")])

    def openFile(self, path: str,) -> None:
        """1st step: open a file"""
        self.__path = path

    def startSession(self) -> None:
        """5th step: hold the decrypted data in memory"""
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
        for dictonary in data:
            if dictonary["account"] == self.__user:
                encryptedData = dictonary["data"]
                break
        jsonData = json.loads(self.__cryptor.decryptText(encryptedData))
        print("DEBUG " + str(jsonData))
        self.__entries = jsonData["entries"]
        self.__oldPasswords = jsonData["oldPasswords"]

    def closeSession(self) -> None:
        """last step: write the encrypted data and close the file"""
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
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

    def getUsers(self) -> List[str]:
        """2nd step: get all users"""
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row["account"])
        return data

    def addUser(self, user: str, key: str) -> None:
        """3rd step: add a user"""
        with open(self.__path, "a", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow([user, key, self.__cryptor.encryptText("{\"entries\":{\"EgCategory\":{\"title\":{\"Example\",\"name\":\"Example\",\"password\":\"Example\",\"url\":\"Example\",\"notices\":\"Example\",\"timestamp\":\"Example\"}}},\"oldPasswords\":[\"Example\",\"Example2\"]}")])

    def remUser(self) -> None:
        """6th step: remove the choosen user"""
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
        for dictonary in data:
            if dictonary["account"] == self.__user:
                data.remove(dictonary)
        with open(self.__path, "w", encoding="utf-8") as file:
            fieldnames = ["account", "key", "data"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for dictonary in data:
                writer.writerow(dictonary)

    def getKey(self, user:str) -> str:
        """3rd step: get the key of the user"""
        self.__user = user
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
        for dictonary in data:
            if dictonary["account"] == user:
                key = dictonary["key"]
                break
        return key

    def getCategories(self) -> list[str]:
        return list(self.__entries.keys())

    def addCategory(self, category: str) -> None:
        self.__entries[category]: dict[str, [dict[str, str]]]

    def remCategory(self, category: str) -> None:
        del self.__entries[category]

    def getEntries(self, category: str) -> dict[str, [dict[str, str]]]:
        """6th step: get all entries of one category"""
        return self.__entries[category]
   
    def getEntry(self, category: str, title: str) -> dict[str, str]:
        return self.__entries[category][title]

    def addEntry(self, category: str, title: str, name: str, password: str, url: str, notices: str, timestamp: str) -> None:
        """6th step add an entry"""
        self.__entries[category][title] = {
            "name": name,
            "password": password,
            "url": url,
            "notices": notices,
            "timestamp": timestamp
        }

    def changeEntry(self, category: str, title: str, prop: str, value: str) -> None:
        """6th step: change and entry"""
        self.__entries[category][title][prop] = value

    def remEntry(self, category: str, title: str) -> None:
        del self.__entries[category][title]

    def getOldPasswords(self) -> list[str]:
        """6th step: get all old password"""
        return self.__oldPasswords

    def addOldPassword(self, oldPassword: str) -> None:
        """6th step: add an old password"""
        self.__oldPasswords.append(oldPassword)

### TODO DEVELOPMENT AREA TO BE REMOVED ###
if __name__ == "__main__":
    print("--- Dev test of Datahandler ---")

    cryptor = cryptor.Cryptor()
    dataHandler = DataHandler(cryptor)
    dataHandler.createFile("autoCreated.kwv", "Paul", "dfgfjhfgs3432rwsfw")
    dataHandler.openFile("autoCreated.kwv")
    print(dataHandler.getUsers())
    dataHandler.addUser("Dieter", "myKey")
    dataHandler.addUser("Hans", "hisKey")
    dataHandler.remUser("Dieter")
    print(dataHandler.getKey("Paul"))
    print(dataHandler.getEncryptedData())
    print(dataHandler.setDecryptedData("{\"entries\":{\"EgCategory\":[{\"title\":\"Example\",\"name\":\"Example\",\"password\":\"Example\",\"url\":\"Example\",\"notices\":\"Example\",\"timestamp\":\"Example\"}]},\"oldPasswords\":[\"Example\",\"Example2\"]}"))
    print(dataHandler.getDecryptedData())
    dataHandler.closeFile(dataHandler.getDecryptedData())

    print("-------------------------------")
###########################################

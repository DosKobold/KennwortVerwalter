#!/bin/python3
"""
File: datahandler.py
Desc: Implements a simple interface for the main.
"""

import csv
import json
from typing import List

class Datahandler:
    """Class for handling data"""

    __path: str
    __user: str
    __entries: dict[str, list[dict[str, str]]]
    __oldPasswords: list[str]

    def createFile(self, path: str, user: str, key: str) -> None:
        """0th step: create file"""
        with open(path, "w", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(["account", "key", "data"])
            writer.writerow([user, key, "{\"entries\":{\"EgCategory\":[{\"title\":\"Example\",\"name\":\"Example\",\"password\":\"Example\",\"url\":\"Example\",\"notices\":\"Example\",\"timestamp\":\"Example\"}]},\"oldPasswords\":[\"Example\",\"Example2\"]}"])

    def openFile(self, path: str,) -> None:
        """1st step: open a file"""
        self.__path = path

    def closeFile(self, encryptedData: str) -> None:
        """last step: write the encrypted data and close the file"""
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
        for dictonary in data:
            if dictonary["account"] == self.__user:
                dictonary["data"] = encryptedData
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
            writer.writerow([user, key, ""])

    def remUser(self, user: str) -> None:
        """6th step: remove the choosen user"""
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
        for dictonary in data:
            if dictonary["account"] == user:
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

    def getEncryptedData(self) -> str:
        """4th step: get the secured data of the called user"""
        with open(self.__path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = []
            for row in reader:
                data.append(row)
        for dictonary in data:
            if dictonary["account"] == self.__user:
                encryptedData = dictonary["data"]
                break
        return encryptedData

    def getDecryptedData(self) -> str:
        """7th step: get the hold data of the called user"""
        print(self.__entries)
        return json.dumps({"entries":self.__entries, "oldPassword":self.__oldPasswords})

    def setDecryptedData(self, decryptedData: str) -> None:
        """5th step: hold the decrypted data in memory"""
        jsonData = json.loads(decryptedData)
        self.__entries = jsonData["entries"]
        self.__oldPasswords = jsonData["oldPasswords"]

    def getEntries(self, category: str) -> list[dict[str, str]]:
        """6th step: get all entries of one category"""
        return self.__entries[category]

    def addEntry(self, category: str, title: str, name: str, password: str, url: str, notices: str, timestamp: str) -> None:
        """6th step add an entry"""
        self.__entries[category].append({
            "title": title,
            "name": name,
            "password": password,
            "url": url,
            "notices": notices,
            "timestamp": timestamp
        })

    def changeEntry(self, category: str, title: str, prop: str, value: str) -> None:
        """6th step: change and entry"""
        for entry in self.__entries:
            if entry["title"] == title:
                entry[prop] = value
                break

    def getOldPasswords(self) -> list[str]:
        """6th step: get all old password"""
        return oldPasswords

    def addOldPassword(self, oldPassword: str) -> None:
        """6th step: add an old password"""
        self.__oldPasswords.append(oldPassword)

### TODO DEVELOPMENT AREA TO BE REMOVED ###
if __name__ == "__main__":
    print("--- Dev test of Datahandler ---")

    dataHandler = Datahandler()
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

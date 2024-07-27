#!/bin/python3
"""
File: datahandler.py
Desc: Implements a simple interface for the main.
"""

import csv
from typing import List

class Datahandler:
	"""Class for handling data"""

	__path = None
	__user = None

	def createFile(self, path: str, user: str, key: str) -> None:
		"""0th step: create file"""
		with open(path, "w") as file:
			writer = csv.writer(file, delimiter=",")
			writer.writerow(["account", "key", "data"])
			writer.writerow([user, key, ""])
			writer.writerow(["Hans", "dfgkdfjg", "segdfg"]) #TODO TEST

	def openFile(self, path: str,) -> None:
		"""1st step: open a file"""
		self.__path = path

	def closeFile(self, encryptedData: str) -> None:
		"""last step: write the encrypted data and close the file"""
		self.__file.write(encryptedData)
		self.__file.close()

	def getUsers(self) -> List[str]:
		"""2nd step: get all users"""
		with open(self.__path, "r") as file:
			reader = csv.DictReader(file)
			data = []
			for row in reader:
				data.append(row["account"])
		return data

	def addUser(self, user: str, key: str) -> None:
		"""3rd step: add a user"""
		with open(self.__path, "a") as file:
			writer = csv.writer(file, delimiter=",")
			writer.writerow([user, key, ""])

	def remUser(self) -> None:
		"""6th step: remove the choosen user"""
		with open(self.__path, "r") as file:
			reader = csv.DictReader(file)
			data = []
			for row in reader:
				data.append(row)
		#TODO Next things to code: Remove the user entry and overwrite the file

	def getKey(self, user:str) -> str:
		"""3rd step: get the key of the user"""
		self.__user = user
		pass

	def getEncryptedData(self) -> str:
		"""4th step: get the secured data of the called user"""
		pass

	def getDecryptedData(self) -> str:
		"""7th step: get the hold data of the called user"""
		pass

	def setData(self, data: str) -> None:
		"""5th step: hold the decrypted data in memory"""
		pass

	def getEntries(self, category: str) -> List[List[str]]:
		"""6th step: get all entries of one category"""
		pass

	def addEntry(self, category: str, title: str, name: str, password: str, url: str, notices: str, timestamp: str):
		"""6th step add an entry"""
		pass

	def changeEntry(self, key: str, value: str) -> None:
		"""6th step: change and entry"""
		pass

	def getOldPasswords(self) -> List[str]:
		"""6th step: get all old password"""
		pass

	def addOldPassword(self, password: str) -> None:
		"""6th step: add an old password"""
		pass

### TODO DEVELOPMENT AREA TO BE REMOVED ###
if __name__ == "__main__":
	print("--- Dev test of Datahandler ---")

	dataHandler = Datahandler()
	dataHandler.createFile("autoCreated.kwv", "Paul", "dfgfjhfgs3432rwsfw")
	dataHandler.openFile("autoCreated.kwv")
	print(dataHandler.getUsers())
	dataHandler.addUser("Dieter", "myKey")

	print("-------------------------------")
###########################################

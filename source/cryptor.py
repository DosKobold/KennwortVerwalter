#!/bin/python3

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import secrets
import os
import base64
import string
import requests

class Cryptor:

	__fernet = None

	def __setMasterKey(self, key: str):
		key = key.encode("utf-8")
		salt = os.urandom(16)
		kdf = PBKDF2HMAC(
			algorithm=hashes.SHA256(),
			length=32,
			salt=salt,
			iterations=480000,
		)
		masterKey = base64.urlsafe_b64encode(kdf.derive(key))
		self.__fernet = Fernet(masterKey)

	def __wrongUsage(self):
		print("[Cryptor] ERROR: Wrong usage of Cryptor! Wrong order of method calls! No master key set!")
		exit()

	def hashPassword(self, text: str, externalCall: bool) -> str:
		sha3_512 = hashlib.sha3_512()
		sha3_512.update(text.encode("utf-8"))
		if(externalCall):
			self.__setMasterKey(text)
		return sha3_512.hexdigest()
		
	def isCorrectPassword(self, text: str, sha3_512 :str) -> bool:
		isCorrect = False
		if(self.hashPassword(text, False) == sha3_512):
			isCorrect = True
			self.__setMasterKey(text)
		return isCorrect

	def encryptText(self, text: str) -> str:
		if(self.__fernet is None):
			self.__wrongUsage()
		token = self.__fernet.encrypt(text.encode("utf-8"))
		return token.decode("utf-8")

	def decryptText(self, text: str) -> str:
		if(self.__fernet is None):
			self.__wrongUsage()
		token = self.__fernet.decrypt(text.encode("utf-8"))
		return token.decode("utf-8")


	def genPassword(self, length: int, digits: bool, others: bool, upper: bool, lower: bool, forbidden: str) -> str:
		chars    = 0
		alphabet = str(None)

		if(digits):
			chars    += 1
			alphabet += string.digits
		if(others):
			chars    += 1
			alphabet += string.punctuation
		if(upper) :
			chars    += 1
			alphabet += string.ascii_uppercase
		if(lower) :
			chars    += 1
			alphabet += string.ascii_lowercase

		if((alphabet is str(None)) or (chars > length)):
			 return str("")

		while True:
			password = ''.join(secrets.choice(alphabet) for i in range(length))
			if(digits): 
				if(not any(char.isdigit() for char in password)): continue
			if(others): 
				if(not any(char in string.punctuation for char in password)): continue
			if(upper) : 
				if(not any(char.isupper() for char in password)): continue
			if(lower): 
				if(not any(char.islower() for char in password)): continue
			if(forbidden != ""):
				if(forbidden in password): continue
			break

		return str(password)

	def isSafe(self, text: str) -> tuple[bool, str]:
		isSecure  = True
		message = ""

		if(not any(char.isdigit() for char in text)):
			isSecure = False
			message += "Digit missing|"
		if(not any(char in string.punctuation for char in text)):
			isSecure = False
			message += "Punctuation missing|"
		if(not any(char.isupper() for char in text)):
			isSecure = False
			message += "Uppercase letter missing|"
		if(not any(char.islower() for char in text)):
			isSecure = False
			message += "Lowercase letter missing|"
		if(len(text) < 8):
			isSecure = False
			message += "Password under 8 characters long|"

		#Search password in the haveibeenpwned database
		#TODO --- Not finished, complete mess! ---
		sha1 = hashlib.sha1()
		sha1.update(text.encode("utf-8"))
		sha1 = sha1.hexdigest()
		sha1 = str(sha1)
		response = requests.get(f"https://api.pwnedpasswords.com/range/{sha1[:5]}")
		if(response.status_code == 200):
			if(sha1[:5] in response.text):
				isSecure = False
				message += "Password is well known"
		print(response.status_code)
		print(sha1)
		print(response.text)
		#-----------------------------------------
		return (isSecure, message)



### TODO DEVELOPMENT AREA TO BE REMOVED ###
if __name__ == "__main__":
	print("--- Dev test of cryptor ---")

	cryptor = Cryptor()

	password = "Test123"
	print("Password: " + password)

	hashedPassword = cryptor.hashPassword(password, True)
	print("Hashed password: " + hashedPassword)

	otherPassword = "Test123a"
	print("Other password: " + otherPassword)

	isCorrect = cryptor.isCorrectPassword(otherPassword, hashedPassword)
	print("Is other password = hash? " + str(isCorrect))

	text = "Hallo, ich bins!"
	print("Text: " + text)

	encryptedText = cryptor.encryptText(text)
	print("Encrypted text: " + encryptedText)

	decryptedText = cryptor.decryptText(encryptedText)
	print("Decrypted text: " + decryptedText)

	newPassword = cryptor.genPassword(4, True, True, True, True, "Test")
	print("New password: " +  newPassword)

	isSafe = cryptor.isSafe("123")
	print("Is new password safe? " + str(isSafe[0]))
	print("\tReason(s): " + str(isSafe[1]))

	print("---------------------------")
###########################################


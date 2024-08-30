#!/bin/python3
"""
File: cryptor.py
Desc: Implements a simple interface for cryptography. En- and decrypts text with a masterkey.
      Hashes a password to a masterkey. Checks if a password is the masterkey. Generates and 
      checks passwords. 
"""

import sys
import hashlib
import secrets
import base64
import string
import requests
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Cryptor:
    """Class for crypting and hashing"""

    def __init__(self) -> None:
        self.__fernet: Fernet

    def __setMasterKey(self, key: str) -> None:
        salt = "IamSalty_asThIs!Pr0jEcT".encode("utf-8")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        masterKey = base64.urlsafe_b64encode(kdf.derive(key.encode("utf-8")))
        self.__fernet = Fernet(masterKey)

    def __wrongUsage(self) -> None:
        print("[Cryptor] ERROR: Wrong usage of Cryptor! Wrong order of method calls! No master key set!")
        sys.exit(1)

    def hashKey(self, key: str, externalCall: bool) -> str:
        hashedKey = hashlib.sha3_512(key.encode("utf-8"))
        if externalCall:
            self.__setMasterKey(key)
        return hashedKey.hexdigest()

    def isCorrectKey(self, key: str, hashedKey :str) -> bool:
        """Checks if a given password is the same as the hashed masterkey"""
        isCorrect = False
        if self.hashKey(key, False) == hashedKey:
            isCorrect = True
            self.__setMasterKey(key)
        return isCorrect

    def encryptText(self, text: str) -> str:
        """Encrypts a given text with the master key"""
        if self.__fernet is None:
            self.__wrongUsage()
	#None has no attribute "encrypt" -> None is checked above
        token = self.__fernet.encrypt(text.encode("utf-8")) #type: ignore
        return str(token.decode("utf-8"))

    def decryptText(self, text: str) -> str:
        """Decrypts a given text with the master key"""
        if self.__fernet is None:
            self.__wrongUsage()
	#None has no attribute "decrypt" -> None is checked above
        token = self.__fernet.decrypt(text.encode("utf-8")) #type: ignore
        return str(token.decode("utf-8"))

    def genPassword(self, length: int, digits: bool, others: bool, upper: bool, lower: bool, forbidden: str) -> str:
        """Generates a password with several options"""
        chars    = 0
        alphabet = ""

        if digits:
            chars    += 1
            alphabet += string.digits
        if others:
            chars    += 1
            alphabet += string.punctuation
        if upper :
            chars    += 1
            alphabet += string.ascii_uppercase
        if lower :
            chars    += 1
            alphabet += string.ascii_lowercase

        if (not alphabet) or (chars > length):
            return str("")

        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(length))
            if digits:
                if not any(char.isdigit() for char in password):
                    continue
            if others:
                if not any(char in string.punctuation for char in password):
                    continue
            if upper :
                if not any(char.isupper() for char in password):
                    continue
            if lower:
                if not any(char.islower() for char in password):
                    continue
            if forbidden != "":
                if forbidden in password:
                    continue
            break

        return str(password)

    def isSafe(self, text: str) -> tuple[bool, str]:
        """Checks if a given password is safe. Provides a additional description string"""
        isSecure  = True
        message = ""

        if not any(char.isdigit() for char in text):
            isSecure = False
            message += "Digit missing|"
        if not any(char in string.punctuation for char in text):
            isSecure = False
            message += "Punctuation missing|"
        if not any(char.isupper() for char in text):
            isSecure = False
            message += "Uppercase letter missing|"
        if not any(char.islower() for char in text):
            isSecure = False
            message += "Lowercase letter missing|"
        if len(text) < 8:
            isSecure = False
            message += "Password under 8 characters long|"

        #Search password in the haveibeenpwned database
        url = "https://api.pwnedpasswords.com/range/"
        sha1 = str(hashlib.sha1(text.encode("utf-8")).hexdigest()).upper()

        try:
            response = requests.get(url + sha1[:5], timeout=5)
            if response.status_code == 200:
                for line in response.text.splitlines():
                    if sha1[5:] in line:
                        isSecure = False
                        message += "Password is well known|"
            else:
                print(f"[Cryptor] WARNING: Can not reach \"{url}\"! Status code: {response.status_code}")
        #The API call is not important -> All exceptions are catched and the user is informed
        except Exception: #pylint: disable=broad-exception-caught
            message += "Check with API \"" + url + "\" failed - Maybe there is no internet connection"

        message = message[:-1].replace("|", ", ")
        return (isSecure, message)

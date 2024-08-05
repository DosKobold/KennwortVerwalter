#!/bin/python3
"""
File: cryptor.py
Desc: Implements a simple interface for the Datahandler. En- and decrypts text with a masterkey.
      Hashes a password to a masterkey. Checks if a password is the mastekey. Generates and checks
      passwords. 
"""

import os
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

    __fernet = None

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
        return token.decode("utf-8")

    def decryptText(self, text: str) -> str:
        """Decrypts a given text with the master key"""
        if self.__fernet is None:
            self.__wrongUsage()
	#None has no attribute "decrypt" -> None is checked above
        token = self.__fernet.decrypt(text.encode("utf-8")) #type: ignore
        return token.decode("utf-8")

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
            response = requests.get(url + sha1[:5])
            if response.status_code == 200:
                for line in response.text.splitlines():
                    if sha1[5:] in line:
                        isSecure = False
                        message += "Password is well known|"
            else:
                print(f"[Cryptor] WARNING: Can not reach \"{url}\"! Status code: {response.status_code}")
        except Exception:
            message += "Check with API \"" + url + "\" failed - Maybe there is no internet connection"

        message = message[:-1].replace("|", ", ")
        return (isSecure, message)



### TODO DEVELOPMENT AREA TO BE REMOVED ###
#if __name__ == "__main__":
 #   print("--- Dev test of cryptor ---")

 #   cryptor = Cryptor()

 #   PASSWORD = "Test123"
 #   print("Password: " + PASSWORD)

 #   HASHED_PASSWORD = cryptor.hashKey(PASSWORD, True)
 #   print("Hashed password: " + HASHED_PASSWORD)

 #   OTHER_PASSWORD = "Test123a"
 #   print("Other password: " + OTHER_PASSWORD)

 #   IS_CORRECT = cryptor.isCorrectKey(OTHER_PASSWORD, HASHED_PASSWORD)
 #   print("Is other password = hash? " + str(IS_CORRECT))

 #   TEXT = "Hallo, ich bins!\n Wer bist du?"
 #   print("Text: " + TEXT)

 #   ENCRYPTED_TEXT = cryptor.encryptText(TEXT)
 #   print("Encrypted text: " + ENCRYPTED_TEXT)

 #   DECRYPTED_TEXT = cryptor.decryptText(ENCRYPTED_TEXT)
 #   print("Decrypted text: " + DECRYPTED_TEXT)

 #   NEW_PASSWORD = cryptor.genPassword(300, False, False, False, False, "")
 #   print("New password: " +  NEW_PASSWORD)

 #   IS_SAFE = cryptor.isSafe(NEW_PASSWORD)
 #   print("Is new password safe? " + str(IS_SAFE[0]))
 #   print("\tReason(s): " + str(IS_SAFE[1]))

 #   print("---------------------------")
###########################################

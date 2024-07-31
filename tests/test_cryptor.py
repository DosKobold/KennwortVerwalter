#pylint: disable=C
import unittest
import cryptor
import string

class TestCryptor(unittest.TestCase):

	cryptor = cryptor.Cryptor()

	HASHES = {"Test123":"68644f3dd172089ae9a650e582ae4759df2ed943291b70729abbc96bca2521ac34f2fad8971c50210e173bd506f3c8e4260f932fd99c3b59c1884fd816cb24ee", "nNjhZut677-.!aEjdFse9Af7":"247c90a852c565dee172bef76aad733c16363be5d3176cf7c31e9199b7c7089ba9db70b7454ef12d8d51e9e6c5a5b88005ec80c98da5956c9a1201a1716e4d44","äüö*¹⁹,µ":"5e38d37379c0eca35a78dde39af037e7c829fc9732844cc76d3ba041173700cf24af4df50143739c6d4b8de15ab9752b79f199a4be8a05e6789cba8f60af440c"}

	TEXTS = ["Nudelsalat90.,-+äöü","fsefnsoiAW+ääö#ü457","#+ä+<>|,lmfi1827389"]

	def test_hashKey(self):
		for password in self.HASHES.keys():
			self.assertEqual(self.cryptor.hashKey(password, True), self.HASHES[password])
		#self.assertNotEqual(self.cryptor.__fernet, None)

	def test_isCorrectKey(self):
		for password in self.HASHES.keys():
			self.assertTrue(self.cryptor.isCorrectKey(password, self.HASHES[password]))

	def test_encryptText_decryptText(self):
		self.cryptor.isCorrectKey("Test123", "68644f3dd172089ae9a650e582ae4759df2ed943291b70729abbc96bca2521ac34f2fad8971c50210e173bd506f3c8e4260f932fd99c3b59c1884fd816cb24ee")
		for text in self.TEXTS:
			encryptedText = self.cryptor.encryptText(text)
			decryptedText = self.cryptor.decryptText(encryptedText)
			self.assertEqual(text, decryptedText)

	def test_genPassword(self):
		def passwordContainsCorrect(length: int, digits: bool, others: bool, upper: bool, lower: bool, forbidden: str, password: str) -> bool:
			isCorrect = True
			if len(password) != length:
				isCorrect = False
			if (digits) and (not any(char.isdigit() for char in password)):
				isCorrect = False
			elif (not digits) and (any(char.isdigit() for char in password)):
				isCorrect = False
			if (others) and (not any(char in string.punctuation for char in password)):
				isCorrect = False
			elif (not others) and (any(char in string.punctuation for char in password)):
				isCorrect = False
			if (upper) and (not any(char.isupper() for char in password)):
				isCorrect = False
			elif (not upper) and (any(char.isupper() for char in password)):
				isCorrect = False
			if (lower) and (not any(char.islower() for char in password)):
				isCorrect = False
			elif (not lower) and (any(char.islower() for char in password)):
				isCorrect = False
			if (forbidden != "") and (forbidden in password):
				isCorrect = False
			return isCorrect

		for i in range(100):
			print("Run out of 100: " + str(i))
			password = self.cryptor.genPassword(300, True, True, True, True, "E")
			self.assertTrue(passwordContainsCorrect(300, True, True, True, True, "E", password))

			password = self.cryptor.genPassword(100, True, False, False, True, "g")
			self.assertTrue(passwordContainsCorrect(100, True, False, False, True, "g", password))

			password = self.cryptor.genPassword(100, False, True, False, False, "Ä")
			self.assertTrue(passwordContainsCorrect(100, False, True, False, False, "Ä", password))
			
			password = self.cryptor.genPassword(300, False, False, False, False, "")
			self.assertEqual(password, "")

			password = self.cryptor.genPassword(3, True, True, True, True, "")
			self.assertEqual(password, "")

	def test_isSafe(self):
		self.assertFalse(self.cryptor.isSafe("123456789")[0])
		self.assertFalse(self.cryptor.isSafe("ABCDEFGHI")[0])
		self.assertFalse(self.cryptor.isSafe("abcdefghi")[0])
		self.assertFalse(self.cryptor.isSafe(".!-§$%&/(")[0])
		self.assertFalse(self.cryptor.isSafe("12345ABCDE")[0])
		self.assertFalse(self.cryptor.isSafe("12345abcde")[0])
		self.assertFalse(self.cryptor.isSafe("12345.!-$%")[0])
		self.assertFalse(self.cryptor.isSafe("123ABCabc")[0])
		self.assertFalse(self.cryptor.isSafe("1Aa.")[0])

		self.assertTrue(self.cryptor.isSafe("123ABCabc.!-")[0])

if __name__ == "__main__":
	unittest.main()

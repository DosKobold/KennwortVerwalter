#pylint: disable=C
import unittest
import dataHandler
import cryptor
import os

class TestCaseBase(unittest.TestCase):
	def assertIsFile(self, path):
		if not os.path.exists(path):
			raise AssertionError("File does not exist!")

class TestDataHandler(TestCaseBase):

	cryptor = cryptor.Cryptor()
	dataHandler = dataHandler.DataHandler(cryptor)

	FILE  = "tests/test_dataHandler_file.csv"
	USER1 = "testUser1"
	USER2 = "testUser2"
	KEY1  = "testKey1"
	KEY2  = "testKey2"
	CATEGORY1 = "testCategory1"
	CATEGORY2 = "testCategory2"

	TITLE1 = "testTitle1"
	NAME1 = "testName1"
	PASS1 = "testPass1"
	URL1 = "testUrl1"
	NOTICES1 = "testNotices1"
	TIMESTAMP1 = "testTimestamp1"

	TITLE2 = "testTitle2"
	NAME2 = "testName2"
	PASS2 = "testPass2"
	URL2 = "testUrl2"
	NOTICES2 = "testNotices2"
	TIMESTAMP2 = "testTimestamp2"

	ENTRY1 = {
		"name": NAME1,
		"password": PASS1,
		"url": URL1,
		"notices": NOTICES1,
		"timestamp": TIMESTAMP1
	}

	def test_01_createFile(self):
		self.dataHandler.createFile(self.FILE, self.USER1, self.cryptor.hashKey(self.KEY1, True))
		self.assertIsFile(self.FILE)

	def test_02_openFile(self):
		self.dataHandler.openFile(self.FILE)

	def test_03_addUser(self):
		self.dataHandler.addUser(self.USER2, self.cryptor.hashKey(self.KEY2, True))

	def test_04_getUsers(self):
		users = self.dataHandler.getUsers()
		self.assertIn(self.USER1, users)
		self.assertIn(self.USER2, users)

	def test_05_getKey(self):
		hashedKey1 = self.cryptor.hashKey(self.KEY1, False)
		savedKey1  = self.dataHandler.getKey(self.USER1)
		hashedKey2 = self.cryptor.hashKey(self.KEY2, False)
		savedKey2  = self.dataHandler.getKey(self.USER2)

		self.assertEqual(hashedKey1, savedKey1)
		self.assertEqual(hashedKey2, savedKey2)

	def test_06_startSession(self):
		self.cryptor.isCorrectKey(self.KEY1, self.dataHandler.getKey(self.USER1))
		self.dataHandler.startSession()

	def test_07_addCategory(self):
		self.dataHandler.addCategory(self.CATEGORY1)
		self.dataHandler.addCategory(self.CATEGORY2)

	def test_08_getCategories(self):
		self.assertIn(self.CATEGORY1, self.dataHandler.getCategories())
		self.assertIn(self.CATEGORY2, self.dataHandler.getCategories())

	def test_09_remCategory(self):
		self.dataHandler.remCategory(self.CATEGORY2)
		self.assertIn(self.CATEGORY1, self.dataHandler.getCategories())
		self.assertNotIn(self.CATEGORY2, self.dataHandler.getCategories())

	def test_10_addEntry(self):
		self.dataHandler.addEntry(self.CATEGORY1, self.TITLE1, self.NAME1, self.PASS1, self.URL1, self.NOTICES1, self.TIMESTAMP1)
		self.dataHandler.addEntry(self.CATEGORY1, self.TITLE2, self.NAME2, self.PASS2, self.URL2, self.NOTICES2, self.TIMESTAMP2)
		
	def test_11_getEntries(self):
		self.assertIn(self.TITLE1, self.dataHandler.getEntries(self.CATEGORY1))
		self.assertIn(self.TITLE2, self.dataHandler.getEntries(self.CATEGORY1))

	def test_12_searchEntry(self):
		self.assertIn(self.TITLE1, self.dataHandler.searchEntry(self.CATEGORY1)[self.CATEGORY1])
		self.assertIn(self.TITLE1, self.dataHandler.searchEntry(self.TITLE1)[self.CATEGORY1])
		self.assertIn(self.TITLE1, self.dataHandler.searchEntry(self.NAME1)[self.CATEGORY1])
		self.assertIn(self.TITLE1, self.dataHandler.searchEntry(self.PASS1)[self.CATEGORY1])
		self.assertIn(self.TITLE1, self.dataHandler.searchEntry(self.URL1)[self.CATEGORY1])
		self.assertIn(self.TITLE1, self.dataHandler.searchEntry(self.NOTICES1)[self.CATEGORY1])
		self.assertIn(self.TITLE1, self.dataHandler.searchEntry(self.TIMESTAMP1)[self.CATEGORY1])

	def test_13_remEntry(self):
		self.dataHandler.remEntry(self.CATEGORY1, self.TITLE2)
		self.assertIn(self.TITLE1, self.dataHandler.getEntries(self.CATEGORY1))
		self.assertNotIn(self.TITLE2, self.dataHandler.getEntries(self.CATEGORY1))

	def test_14_getEntry(self):
		self.assertEqual(self.ENTRY1, self.dataHandler.getEntry(self.CATEGORY1, self.TITLE1))

	def test_15_changeEntry(self):
		self.dataHandler.changeEntry(self.CATEGORY1, self.TITLE1, "password", self.PASS2)
		self.assertNotEqual(self.ENTRY1, self.dataHandler.getEntry(self.CATEGORY1, self.TITLE1))
		self.dataHandler.changeEntry(self.CATEGORY1, self.TITLE1, "password", self.PASS1)
		self.assertEqual(self.ENTRY1, self.dataHandler.getEntry(self.CATEGORY1, self.TITLE1))

	def test_16_addOldPassword(self):
		self.dataHandler.addOldPassword(self.PASS1)

	def test_17_getOldPasswords(self):
		self.assertIn(self.PASS1, self.dataHandler.getOldPasswords())
		for i in range(10):
			self.dataHandler.addOldPassword(self.PASS2)
		self.assertNotIn(self.PASS1, self.dataHandler.getOldPasswords())

	def test_18_closeSession(self):
		self.dataHandler.closeSession()

	def test_19_remUser(self):
		self.dataHandler.openFile(self.FILE)
		self.cryptor.isCorrectKey(self.KEY1, self.dataHandler.getKey(self.USER1))
		self.dataHandler.startSession()
		self.dataHandler.remUser()
		self.dataHandler.openFile(self.FILE)
		self.assertNotIn(self.USER1, self.dataHandler.getUsers())
		
if __name__ == "__main__":
	unittest.main()

#!/usr/bin/python3
"""
File: main.py
Desc: Bridge between frontend and backend
"""

import cryptor
import dataHandler

if __name__ == "__main__":
    print("main")

    ### EXAMPLE FOR FRONTED DEVELOPERS ###
    #frontend = frontend.Frontend()
    #frontend.loginScreen(dataHandler.getUsers(): str) -> tuple(user:str, password: str)
    #if password correct:
    #frontend.mainScreen(dataHandler.getCategories() -> list[str]) -> None
    #if frontend.getKey() == "enter":
        #frontend.entryView(dataHandler.getEntry(frontend.getChoosen() -> str)) -> None
        #if frontend.getKey() == "N":
            #dataHandler.addEntry(frontend.getChoosen())


    ### TODO DEVELOPMENT AREA TO BE REMOVED ###
    print("--- Dev test of backend interaction ---")

    cryptor = cryptor.Cryptor()
    dataHandler = dataHandler.DataHandler(cryptor)
    
    #FIRST RUN
    dataHandler.createFile("autoCreated.kwv", "paul", cryptor.hashKey("test123", True))
    dataHandler.openFile("autoCreated.kwv") #IMPORTANT CALL
    print(dataHandler.getUsers())
    #dataHandler.addUser("Klaus", cryptor.hashKey("test246", True))

    if cryptor.isCorrectKey("test123", dataHandler.getKey("paul")): #IF CLAUSE AND GETKEY ARE IMPORTANT CALLS
        dataHandler.startSession() #Data will be read from the file (openFile) and from user with the key (getKey) #IMPORTANT CALL
        print(dataHandler.getCategories())
        print(dataHandler.getEntries("EgCategory"))
        print(dataHandler.getOldPasswords())
        dataHandler.addOldPassword("hund78")
        dataHandler.addEntry("EgCategory", "Youtube", "benHD89", "hund78", "youtube.com", "Youtube is klasse", "2024-07-28")
        dataHandler.changeEntry("EgCategory", "Youtube", "name", "geänderter name")
        dataHandler.closeSession() #Data will be encrypted and written to disk #IMPORTANT CALL

    #SECOND RUN
    dataHandler.openFile("autoCreated.kwv") #IMPORTANT CALL
    print(dataHandler.getUsers())

    if cryptor.isCorrectKey("test123", dataHandler.getKey("paul")): #IF CLAUSE AND GETKEY ARE IMPORTANT CALLS
        dataHandler.startSession() #Data will be read from the file (openFile) and from user with the key (getKey) #IMPORTANT CALL
        print(dataHandler.getCategories())
        print(dataHandler.getEntries("EgCategory"))
        print(dataHandler.getOldPasswords())
        dataHandler.closeSession() #Data will be encrypted and written to disk #IMPORTANT CALL
        
    print("---------------------------------------")
    ###########################################

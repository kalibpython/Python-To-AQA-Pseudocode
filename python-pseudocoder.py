
#Python-to-AQA-psudocode converter
#By Andrew Mulholland aka gbaman

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.



#Enter the file name of the python file you want to convert below
#You should use its full file path
pythonFile = "test.py"


import sqlite3
import sys
import os
import os.path
import time

current_time = time.asctime(time.localtime(time.time()))


class files_s:
    def __init__(self):

        print(10 * "=" + "Initialize logFiles" + "=" * 10)
        self.rexists = os.path.isfile(".rec.txt")
        self.lexists = os.path.isfile(".log.txt")
        if self.rexists:

            self.recFile = open(".rec.txt", "r")  # this should always open in readmode
            # if data is to be written to the file then it shoul be appended to the last line
            # this is to ensure that the contents of the file isnt overwritten once the class is
            # instantiated
        else:
            print("[+] Creating records file ")
            self.recFile = open(".rec.txt", "w+")
        # version 2 would be for handling logs
        if self.lexists:

            self.logFiles = open(".log.txt", "r")
        else:
            print("[+] Creating logs file")
            self.logFiles = open(".log.txt", "w+")

    def read_records(self):
        for line in self.recFile:
            text = line.strip()
            commandList = text.split("#")
            command = commandList[0]
            casesLIST = commandList[-1]
            casesLIST = casesLIST.split(" ")

            if command == "RECORD":
                # RECORD#1000#1#TIME#8,000#124#12,000#
                i_d = int(commandList[1])
                version = commandList[2]
                time = commandList[3]
                total_cases = commandList[4]
                total_deaths = commandList[5]
                total_visitors = commandList[6]
                print(f"=" * 10 + "COVID RECORD " + f"verison:{version}" + "=" * 10)
                print(f"The id number:       {i_d}")
                print(f"record version:      {version}")
                print(f"The time:            {time}")
                print(f"total cases:         {total_cases}")
                print(f"total deaths:        {total_deaths}")
                print(f"total visitors:      {total_visitors}")
                print(10 * "-" + "Cases per parish:" + "-" * 10)
                for i in range(len(casesLIST)):
                    print(f"{casesLIST[i]}")

            elif command == "endfill":
                continue
                # covidrecords.close()

    def view_logs(self):

        for line in self.logFiles:
            text = line.strip()
            commandList = text.split(",")
            command = commandList[0]

            if command == "LOG":
                time = commandList[6]  # deals with TIME
                i_d = int(commandList[2])
                usage = int(commandList[4])
                print("=" * 10 + "LOG" + "=" * 10)

                print(f"The id number:       {i_d}")
                print(f"program usage count: {usage}")
                print(f"The time:            {time}")

            elif command == "CHANGES":
                firstname = commandList[2]
                lastname = commandList[4]
                i_d = int(commandList[6])

                print("=" * 10 + "CHANGE" + "=" * 10)
                print(f"Firstname is:        {firstname}")
                print(f"Lastname is:         {lastname}")
                print(f"ID is:               {i_d}")
            elif command == "endfill":
                print("End of file ")
        self.logFiles.close()

    def write_records(self, recordQry, cppList):
        # this function can be seen as the edit records function due to its implementation
        # this function should never overwrite a record
        # this should only add a new record while incrementing the version and saving
        # the admin id which was used to create that record
        # rewrite this finction based on the write logs function
        # thi should have 2 versions
        # version 2 would accomodate editing records
        # version 2 suggests that there should be a correlation between
        # cases per parish to total number of cases
        # i.e total number of cases should be calculated by adding all cases per parish
        # cases per parish would have to be retrieved in a list
        # cases per parish should be calculated before sent in the list
        recFiles = open(".rec.txt", "r")
        for line in recFiles:
            text = line.strip()
            commandList = text.split(",")
            command = commandList[0]
            if command == "endfill":
                end = True

            if end:
                print("the end is true")
                recFiles = open(".rec.txt", "a+")
                recFiles.writelines(recordQry + cppList + "\n")
                recFiles.close()
            else:
                recFiles.close()

        print("writelogs ")

    def write_logs(self, log_qry):

        logFiles = open(".log.txt", "r")
        for line in logFiles:
            text = line.strip()
            commandList = text.split(",")
            command = commandList[0]
            if command == "endfill":
                end = True

            if end:
                print("the end is true")
                logFiles = open(".log.txt", "a+")
                logFiles.writelines(log_qry + "\n")
                logFiles.close()
            else:
                logFiles.close()


class database_s(files_s):
    def __init__(self):
        self.connnect = sqlite3.connect("CoIMaDS.db")  # extablishes connection to database
        # print(f"Established connection at: {self.connnect}")
        self.cursor = self.connnect.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS user (id_num PRIMARY KEY,
                                                                firstname TEXT,
                                                                lastname TEXT,
                                                                date_of_birth TEXT,
                                                                address TEXT,
                                                                parish TEXT,
                                                                gender TEXT,
                                                                date_of_arival TEXT,
                                                                lengh_of_stay int,
                                                                precondition TEXT,
                                                                covid_status TEXT,
                                                                date_of_last_labtest TEXT,
                                                                violator_status TEXT)
                            """)
        # lengh of stay needs to be evaluated with checks
        # all date attriutes should be evaluated with checks
        # id is used to represent trn or ven respectively

    # this class deals with the database
    def add_user(self, args, ident):
        self.args = args
        self.ident = ident  # ident test
        try:
            if self.args == 1:
                # self.ident = input("Enter id: ") #ident test
                firstname = input("Enter fistname: ")
                lastname = input("Enter lastname: ")
                date_of_birth = input("Enter date of birth: ")
                address = input("Enter address: ")
                parish = input("Enter parish: ")
                gender = input("Enter gender: ")
                date_of_arrival = input("Enter date of arival status: ")
                length_of_stay = int(input("Enter length of stay: "))  # if trn user then this should be empty
                precondition = input("Enter medical precondition: ")
                covid_status = input("Enter covid status: ")
                date_of_last_labtest = input("Enter date of recent labtest: ")
                violator_status = input("Enter violator status: ")

                update_qry = """UPDATE user SET id_num=?,firstname=?,lastname=?,date_of_birth=?,address=?,parish=?,gender=?,date_of_arrival=?,length_of_stay=?,precondition=?,covid_status=?,date_of_last_labtest=?,violator_status=? WHERE id_num=?  """
                data = (self.ident, firstname, lastname, date_of_birth, address, parish, gender, date_of_arrival,
                        length_of_stay, precondition, covid_status, date_of_last_labtest, violator_status,
                        self.ident)  # last value is the idnum for the WHERE clause
                self.cursor.execute(update_qry, data)
                #################################
                # possible add functionality to add tablenames to a flat file before
                # they are sent to the database i.e firstname wille be appended to the file
                # because the user has to add something to firstname

                self.connnect.commit()
                self.cursor.close()  # closed curser
                self.connnect.close()  # closes database connection
                print("[+] New user was added to the database")

            elif self.args == 2:  # admin level
                # version 2 or the adduser functions takes the id from user input///
                # this verison should only be used when all data is to be entered at once
                # reguardless of if the user already initiated the program
                id_num = input("Enter the id: ")
                firstname = input("Enter fistname: ")  # all other values should be added
                self.cursor.execute("""INSERT INTO user (id_num,
                                                        firstname,
                                                        lastname,
                                                        date_of_birth,
                                                        address,
                                                        parish,
                                                        gender,
                                                        date_of_arrival,
                                                        length_of_stay,
                                                        precondition,
                                                        covid_status,
                                                        date_of_last_labtest,
                                                        violator_status) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"""
                                    , (id_num, firstname, lastname, date_of_birth, address, parish, gender,
                                       date_of_arrival, length_of_stay, precondition, covid_status,
                                       date_of_last_labtest, violator_status))
                #################################
                self.connnect.commit()
                self.cursor.close()  # closed curser
                self.connnect.close()  # closes database connection
                print("[+] New user was added to the database")



        except Exception as ex:
            print(f"[!] Could not add user to the database: {ex}")

    def search(self):
        # id is used as unique identifier to search for each user in the database
        # other methods of search can also be implemented such as
        # show all users with names john brown etc
        # this can be implemented with views or where statements
        # self.args = args
        # if self.args == 1:
        # search function needs development
        print("[+] you have selected the search option ")
        # add logic to search by ex. search by firstname or date of entry etc
        id_num = input("Enter the id to search: ")
        self.cursor.execute("SELECT * FROM user WHERE id_num=?", (id_num,))
        results = self.cursor.fetchone()  # returnes values from database quary

        if results:
            print("[+] User found")  # evaluate this line to return names
            results_list = []
            for i in range(len(results)):  # this range is dependent on how much data is to be returned
                results_list.append(results[i])

            show_user(results_list, args=3)  # show user 3 returns first name and id only
            # add logic to return to homescreen
        else:
            print("[!] User not found")
            self.cursor.close()  # closes cursor if user not found
            self.connnect.close()  # closes database connection if user not found
            # add logic to return to homescreen

    def delete_user(self):
        # this is the delete user function
        print("[+] you have selected the Delete option ")
        # add logic to search by ex. search by firstname or date of entry etc
        id_num = input("Enter the id: ")
        self.cursor.execute("SELECT * FROM user WHERE id_num=?", (id_num,))
        results = self.cursor.fetchone()  # returnes values from database quary

        if results:
            # evaluate this line to return names
            print("[+] User found!")
            results_list = []
            for i in range(len(results)):  # this range is dependent on how much data is to be returned
                results_list.append(results[i])

            show_user(results_list, args=3)  # this returnes data of the user which was found
            # add logic to return to homescreen

            d = input("[*] would you like to delete this user? y or n: ")
            try:  # try catch needs to be evaluated
                if d == "y" or "yes":
                    # execute the delete user quary
                    self.cursor.execute("DELETE FROM user WHERE id_num=?", (id_num,))
                    print("[*] User Removed!")
                    self.connnect.commit()
                    self.cursor.close()  # closed curser
                    self.connnect.close()
                    #################################
                # possible add functionality to add tablenames to a flat file before
                # they are sent to the database i.e firstname wille be appended to the file
                # because the user has to add something to firstname

                # add logic to return to homescreen i.e call the usage function again
                elif d == "n" or "no":
                    self.cursor.close()
                    self.connnect.close()
                    # add logic to return to homescreen
            except:
                print("[!] incorrect input")  #### needs evaluation

        else:
            print("[!] User not found")
            self.cursor.close()  # closes cursor if user not found
            self.connnect.close()
            # closes database connection if user not found
            # add logic to return to homescreen

    def edit_user(self, args, ident):
        # this is the edit user function or rather the update user function
        # these functions need different versions to enforce acces levels in the progran
        # each version of the function is implemented using args which are numbers passed
        # to each version which initializes it
        # this function will have an append verion where it is able to append data to the database
        self.args = args
        self.ident = ident
        #################################
        # functionality to update
        #  firstname,lastname,precondition,violator_status,covid_status
        #
        # add logic to search by ex. search by firstname or date of entry etc
        if args == 1:
            t = database_s()
            t.add_user(args=1, ident=ident)  # this edits everythong about an existing user


        elif args == 2:

            id_num = input("Enter the id: ")
            self.cursor.execute("SELECT * FROM user WHERE id_num=?", (id_num,))
            result = self.cursor.fetchone()  # returnes values from database quary
            if result:
                print("[*] User found")
                results_list = []
                for i in range(len(result)):  # this range is dependent on how much data is to be returned
                    results_list.append(result[i])
                show_user(list=results_list, args=4)  # returnes the users information

                opt = input("Would you like to update this users data? y or n")
                if opt == "y" or "yes":
                    firstname = input("Enter the firstname: ")
                    lastname = input("Enter the lastname: ")
                    precondition = input("Enter the precondition: ")
                    violator_status = input("Enter the violator status: ")
                    covid_status = input("Enter the covid status: ")
                    update_qry = """UPDATE user SET firstname=?,lastname=?,precondition=?,violator_status=?,covid_status=? WHERE id_num=?  """
                    data = (firstname, lastname, precondition, violator_status, covid_status, id_num)
                    self.cursor.execute(update_qry, data)
                    self.connnect.commit()
                    self.cursor.close()  # closed curser
                    self.connnect.close()  # closes database connection
                    print("[+] user updated")

                elif opt == "n" or "no":
                    pass


            else:
                print("[-] User not found")


        elif args == 3:
            pass

        return
        # rec handling was here


def records_handling(args, ident):  # possible add functionality to pass list with total deaths and visitors
    # if not develop logic to add them
    if args == 1:
        print("add log ")
        logsList = []
        # usage will alwsys be equal to one however it will be used to add up total usage count
        logsList.append(ident)
        logsList.append(current_time)
        ####
        log_qry = f"LOG,ID,{logsList[0]},TIME,{logsList[1]}\nendfill"
        f = files_s()  # this is the files class
        f.write_logs(log_qry)  # this is the write logs function from the logs class
    elif args == 2:
        print("add record")
        recList = []  # this list should deal with all the data
        # strt = "record1,1000,time"
        id_num = str(ident)
        version = 1  # might remove
        total_deaths = 134  # should have functionality
        total_visitors = 8000  # should have functionality
        cppList = []
        dpp = []
        parish = ["Kingston", "St.Andrew", "St.Catherine", "Clarendon", "Manchester", "St.Elizabeth", "Westmoreland",
                  "Hanover", "St.James", "Trelawny", "St.Ann", "St.Mary", "Portland", "St.Thomas"]
        print("Enter the number of cases per parish: ")
        for i in range(len(parish)):
            d = int(input(f" {parish[i]} "))
            dpp.append(d)
            cppList.append(parish[i] + ":" + str(d))

        total_cases = sum(dpp)
        recList.append(id_num)
        recList.append(version)
        recList.append(current_time)
        recList.append(total_cases)
        recList.append(total_deaths)
        recList.append(total_visitors)
        # identity
        ##RECORD#1000#1#TIME#8,000#124#12,000#
        recordQry = f"RECORD#{recList[1]}#{recList[2]}#{recList[3]}#{recList[4]}#{recList[5]}#{recList[6]}"
        # records quary which should come after the beginfill
        f = files_s()
        f.write_records(recordQry=recordQry, cppList=cppList)


# this would be where the program runs
# develop a login function to initiate this

def usage(args, ident):
    # usage function need multiple versions for different levels of access and
    # usage args 1 would be for administrator level access i.e has all the options available
    # usage args 2 would be semi=administrator level access i.e has 2 or at least 3 options available
    # usage args 3 would be low privalaged user level access i.e has only the search user option etc
    # this is version 1
    if args == 1:

        database_s()
        print("=" * 20)
        print("Select (1) to add user Select (2) to search for user (3) to delete user ///(4) to edit user")
        selected = int(input(":"))
        if selected == 1:
            t = database_s()
            t.add_user(args=1, ident=ident)  # this will call the function if the user already exists
            # logic to call add user function should be developed
            # add user version 2 is admin level
        elif selected == 2:
            t = database_s()
            t.search()
        elif selected == 3:
            t = database_s()
            t.delete_user()
        elif selected == 4:
            t = database_s()
            t.edit_user(args=1, ident=ident)  # edit user needs ident for version 1

    # add logic to save all instances or usages of the program
    # this file should save id used to enter and return the date and time the user logged on,
    # this wold increment by an id of all logs i.e (logs) = logs + 1 "after use"

    # add else clause for exit functionality


def show_user(list, args):
    if args == 1:
        # show user 1 would return all data of the user
        # 0,1,2,3,4,5,6,7,8,9,10,11
        """
        0 id
        1 firstname
        2 lastname
        3 date of birth
        4 address
        5 parish
        6 gender
        7 date of arrival
        8 length of stay
        9 precondition
        10 covid status
        11 date of last labtest
        12 violator status
        """
        id_num = 0
        firstname, lastname, date_of_birth, address, parish, gender, date_of_arrival, length_of_stay, precondition, covid_status, date_of_last_labtest, violator_status = ""

        id_num = str(list[0])
        firstname = str(list[1])
        lastname = str(list[2])
        date_of_birth = str(list[3])
        address = str(list[4])
        parish = str(list[5])
        gender = str(list[6])
        date_of_arrival = str(list[7])
        length_of_stay = str(list[8])
        precondition = str(list[9])
        covid_status = str(list[10])
        date_of_last_labtest = str(list[11])
        violator_status = str(list[12])

        print("=" * 10)
        print(f"I.D:       {id_num}")
        print(f"Firstname: {firstname}")
        print(f"Lastname:  {lastname}")
        print(f"Date of birth:  {date_of_birth}")
        print(f"Address:  {address}")
        print(f"Parish:  {parish}")
        print(f"Gender:  {gender}")
        print(f"Date of Arrival:  {date_of_arrival}")
        print(f"Length of stay:  {length_of_stay}")
        print(f"Precondition:  {precondition}")
        print(f"Covid status:  {covid_status}")
        print(f"Date of recent labtest:  {date_of_last_labtest}")
        print(f"Violator status:  {violator_status}")
        print("=" * 10)
        # incomplete i.e to add further aspects of the user ex lastname,date of birth etc
    elif args == 2:
        # show user 2 would return the first name only as a single line variable
        firstname = ""
        firstname = str(list[1])
        # print(f"Firstname: {firstname}")
        # this could return the last name as well
        return firstname
    elif args == 3:
        # show user 3 would only return the first name and id
        id_num = 0
        firstname = ""
        id_num = str(list[0])
        firstname = str(list[1])
        print("=" * 10)
        print(f"I.D:       {id_num}")
        print(f"Firstname: {firstname}")
        print("=" * 10)
    elif args == 4:  ##incomplete
        id_num = 0
        firstname, lastname, precondition, violator_status, covid_status = ""
        """
        0 id
        1 firstname
        2 lastname
        3 date of birth
        4 address
        5 parish
        6 gender
        7 date of arrival
        8 length of stay
        9 precondition
        10 covid status
        11 date of last labtest
        12 violator status
        """
        id_num = str(list[0])
        firstname = str(list[1])
        lastname = str(list[2])
        precondition = str(list[9])
        violator_status = str(list[12])
        covid_status = str(list[10])
        ##########
        print("=" * 10)
        print(f"I.D:            {id_num}")
        print(f"Firstname:      {firstname}")
        print(f"Lastname:       {lastname}")
        print(f"Precondition:   {precondition}")
        print(f"Violator status:{violator_status}")
        print(f"Covid status:   {covid_status}")
        print("=" * 10)


def menu():
    # this is the main menu of the program
    database_s()  # this initializes the database once the program starts
    select = int(input("(1)T.R.N (2) V.E.N "))
    # this code ensures the user selects 1 or 2 to get started
    # if 3 is entered, the program exits #this is the case for testing
    # add update to logs file as trn user true for example
    try:
        if select == 1:
            dbcon = sqlite3.connect("CoIMaDS.db")
            cursor = dbcon.cursor()
            trn = input("Enter t.r.n number: ")
            try:
                cursor.execute("SELECT * FROM user WHERE id_num=?", (trn,))
                results = cursor.fetchone()  # returnes values from database quary

                if results:
                    records_handling(args=1,
                                     ident=trn)  # facilitate ident as a list which tells if the user is a trn user
                    results_list = []
                    for i in range(len(results)):  # this range is dependent on how much data is to be returned
                        results_list.append(results[i])

                    print(f"[+] Welcome back " + show_user(results_list, args=2))  # evaluate this line to return names
                    dbcon.commit()
                    usage(args=1, ident=trn)

                else:
                    # print("[!] User not found")
                    cursor.execute("""INSERT INTO user ( id_num) VALUES (?)
                                     """, (trn,))  # quary not complete to add values ?
                    dbcon.commit()
                    print("You will be asked to use this trn as an id to search,edit,and add user to the system")
                    usage(args=1, ident=trn)

            except Exception as ex:
                print(ex)  # needs to be evaluated
                # cursor.close()
                if ex:
                    usage(args=1, ident=trn)  # if the exception is a unique id error then continue
                    records_handling(args=1,
                                     ident=trn)  # facilitate ident as a list which tells if the user is a trn user
                # continue the code
        elif select == 2:
            dbcon = sqlite3.connect("CoIMaDS.db")
            cursor = dbcon.cursor()
            ven = input("Enter v.e.n number: ")
            try:
                cursor.execute("SELECT * FROM user WHERE id_num=?", (ven,))
                results = cursor.fetchone()  # returnes values from database quary

                if results:
                    records_handling(args=1,
                                     ident=trn)  # facilitate ident as a list which tells if the user is a trn user
                    results_list = []
                    for i in range(len(results)):  # this range is dependent on how much data is to be returned
                        results_list.append(results[i])

                    print(f"[+] Welcome back " + show_user(results_list, args=2))  # evaluate this line to return names
                    dbcon.commit()
                    usage(args=1, ident=ven)

                else:
                    # print("[!] User not found")
                    cursor.execute("""INSERT INTO user ( id_num) VALUES (?)
                                     """, (ven,))  # quary not complete to add values ?
                    dbcon.commit()
                    print("You will be asked to use this trn as an id to search,edit,and add user to the system")
                    usage(args=1, ident=ven)

            except Exception as ex:
                print(ex)  # needs to be evaluated
                # cursor.close()
                if ex:
                    usage(args=1, ident=ven)  # if the exception is a unique id error then continue
                    records_handling(args=1,
                                     ident=ven)  # facilitate ident as a list which tells if the user is a trn user
                # continue the code

    except:  # user entered exit
        sys.exit(1)  # exit function assuming user entered something else


############80% complete
menu()  # lol


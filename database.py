# Student Number: F230551
# Date: 11/11/2022
# Version 11
# database.py file containing all the operations to do with the database
import sqlite3 #Importing the library that will operate the database
import numpy as np #Numpy operations used in code require this library
import pandas as pd #Some execution is making use of panda execution

class Database():
    '''
        Database class containing all operations on the database:
        - Creating Tables
        - Dropping Tables
        - Inserting Data
        - Running select queries which return data
        - Running update/insert queries which execute the statement
    '''
    def __init__(self):
        '''
        Initiialisation of the database connection and the cursor which will be referenced throughout the program
        '''
        connection = sqlite3.connect("Library.db") #Creates the connection to the library db
        self.connection = connection #Creating a variable to be used throughout the program
        self.cursor = self.connection.cursor() #Creating the cursor for statement excution

    def Create_Table(self,SqlStatements=[],No_Of_Tables=1):
        '''
        Function that creates tables for my db
        :param SqlStatements: List of sql queries the program should execute
        :param No_Of_Tables: Integer value for the amount of tables to be created
        :return: Table successfully created
        '''
        for i in range(No_Of_Tables): #Iterating through the list of queries
            try: #Try Except argument to catch sql errors
                self.cursor.execute(SqlStatements[i]) #Executing the query in the list

            except sqlite3.Error as error: #Except catches the sqlite errors produced
                print("Error: ", error) #Show the Problem caught

            finally: #Always execute the code below even after an error is caught
                print("Table {} Successfully created".format(i+1)) #Inform that a table has been created

    def Drop_Table(self,SqlStatements=[],No_Of_Tables=1):
        '''
        Dropping tables created for an initialisation restart
        :param SqlStatements: Drop statements to execute
        :param No_Of_Tables: Number of queries to execute
        :return: Table successfully dropped
        '''
        #Code has same functionality as creating tables but for dropping them
        for i in range(No_Of_Tables):
            try:
                self.cursor.execute(SqlStatements[i])
            except sqlite3.Error as error:
                print("Error: ", error)
            finally:
                print("Table {} Successfully dropped".format(i+1))

    def Insert_Data(self):
        '''
        Inserting the data into the tables generated
        :return: Data Successfully added after execution
        '''
        Book_Info_File = pd.read_csv("Book_Info.txt") #Import the data of the books to begin manipulation
        Book_Info_File = Book_Info_File.rename(columns={'ID':'Book_ID','Purchase Price £':'Purchase_Price_£'
                                                        ,'Purchase Date':'Purchase_Date'}) #Change the column names

        Loan_Reservation_History_File = pd.read_csv("Loan_Reservation_History.txt") #Import the Loan res data
        Loan_Reservation_History_File = Loan_Reservation_History_File.rename(columns={'Book_ID':'BID'}) #Change the column name

        try: #Try the following code except sqlite errors
            #Merging the book_info file with the loan reservation history file to compute calculations
            Availability_from_Loan = pd.merge(Book_Info_File,Loan_Reservation_History_File,left_on='Book_ID',right_on='BID')

            Availability_from_Loan['Loan_Availability'] = np.nan #Creating a column in the merged data that is null
            #Checking the checkout date and return date to see if the book is available
            Availability_from_Loan.loc[
                (Availability_from_Loan.Return_Date == '---') & (Availability_from_Loan.Checkout_Date != '---'), 'Loan_Availability'] = "Not Available"
            #Checking the return date is not null which states the book is available
            Availability_from_Loan.loc[
                (Availability_from_Loan.Return_Date != '---'), 'Loan_Availability'] = "Available"

            # Creating a column in the book info file to the values generated for availability
            Book_Info_File['Loan_Availability'] = Availability_from_Loan['Loan_Availability']
            # If a row is empty then the book is available so set to available
            Book_Info_File.loc[Book_Info_File['Loan_Availability'].isnull(), 'Loan_Availability'] = "Available"

            #Select the rows of the books table and drop duplicates then append values to the db table
            Book_Rows = Book_Info_File[['Book_ID','Title','Loan_Availability']].drop_duplicates()
            Book_Rows.to_sql("Books",self.connection, if_exists='append',index=False)

            #Select the relevant columns, drop duplicates and append to the db table genres
            Genre_Rows = Book_Info_File[['Genre']].drop_duplicates()
            Genre_Rows.to_sql("Genres",self.connection, if_exists='append',index=False)

            #Select the relevant columns then drop duplicates and finally append to the db table authors
            Author_Rows = Book_Info_File[['Author']].drop_duplicates()
            Author_Rows.to_sql("Authors",self.connection, if_exists='append',index=False)

            #Create a duplicate data file for calculations later
            DupData = Book_Info_File.drop(columns="Loan_Availability")
            DupData.to_sql("DupData", self.connection, if_exists='append', index=False)

            #Rename the column to match the column name in the db table
            Book_Info_File = Book_Info_File.rename(columns={'Book_ID': 'BPID'})

            #Select the relevant rows
            Purchase_Rows = Book_Info_File[['BPID','Purchase_Price_£','Purchase_Date']]
            #Using the DupData table pull the genre_id where the genres match and same applies for authors
            GID = pd.read_sql('''SELECT Genres.Genre_ID from Dupdata 
                                                JOIN Genres ON DupData.Genre = Genres.Genre''', self.connection)
            AID = pd.read_sql('''SELECT Authors.Author_ID from Dupdata 
                                                JOIN Authors ON DupData.Author = Authors.Author''', self.connection)
            #Set the information found to new rows in the purchase_rows dataframe
            Purchase_Rows['GID'] = GID
            Purchase_Rows['AID'] = AID
            #Append the values to the db table
            Purchase_Rows.to_sql("Purchases",self.connection, if_exists='append',index=False)

            #Replace the "---" with np.nan which is null in python then append the values to the file
            Reservation_Rows = Loan_Reservation_History_File.replace("---",np.nan)
            Reservation_Rows.to_sql("Reservations",self.connection, if_exists='append',index=False)

            self.connection.commit()#Save all the changes made from creating the tables to inserting the data into them

        except sqlite3.Error as error:
            print(error)

        finally:
            print("Data Successfully Added")

    def RunSQL_Return(self,SQLStatement=""):
        '''
        Function runs the statement
        :param SQLStatement: Statement that needs to be run
        :return: A dataframe of the data provided
        '''
        try:
            # Executing the statement using pandas by passing the statement and the db conncetion
            result = pd.read_sql(SQLStatement, self.connection)

        except sqlite3.Error as Error:
            print("Error: ", Error)

        finally:
            self.connection.commit()

        return result

    def RunSQL_Update(self,SQLStatement=""):
        '''
        Running statements such as update and insert
        :param SQLStatement: Statement to be run
        :return: nothing is returned but connection is commited to save changes.
        '''
        try:
            self.cursor.execute(SQLStatement)#Executing the statement

        except sqlite3.Error as Error:
            print("Error: ", Error)

        finally:
            self.connection.commit()

class Initialise_DB(Database):
    '''
        Inheritance of Database to initialise the db on command
    '''
    def __init__(self):
        '''
            Initialisation of the database
        '''
        super().__init__() #Creating a initialisation of the database class
        self.Start_DB() #Initiates the database initialisation

    def Start_DB(self):
        Create_Book_Table = '''CREATE TABLE IF NOT EXISTS Books (Book_ID integer PRIMARY KEY NOT NULL,
                                                                    Title text NOT NULL,
                                                                    Loan_Availability text DEFAULT 'Available' NOT NULL);'''

        Create_Genre_Table = '''CREATE TABLE IF NOT EXISTS Genres (Genre_ID integer PRIMARY KEY NOT NULL,
                                                                    Genre text NOT NULL);'''

        Create_Author_Table = '''CREATE TABLE IF NOT EXISTS Authors (Author_ID integer PRIMARY KEY NOT NULL,
                                                                        Author text NOT NULL);'''

        Create_Purchases_Table = '''CREATE TABLE IF NOT EXISTS Purchases (BPID integer NOT NULL,
                                                                            GID integer NOT NULL,
                                                                            AID integer NOT NULL,
                                                                            Purchase_Price_£ integer NOT NULL,
                                                                            Purchase_Date text NOT NULL,
                                                                            FOREIGN KEY (BPID) REFERENCES Books(Book_ID)
                                                                            FOREIGN KEY (GID) REFERENCES Genres(Genre_ID)
                                                                            FOREIGN KEY (AID) REFERENCES Authors(Author_ID));'''

        Create_Reservation_Table = '''CREATE TABLE IF NOT EXISTS Reservations (Transaction_ID integer NOT NULL,
                                                                                BID integer NOT NULL,
                                                                                Reservation_Date text,
                                                                                Checkout_Date text,
                                                                                Return_Date text,
                                                                                Member_ID integer NOT NULL,
                                                                                PRIMARY KEY (Transaction_ID),
                                                                                FOREIGN KEY (BID) REFERENCES Books(Book_ID));'''

        Create_DupData_Table = '''CREATE TABLE IF NOT EXISTS DupData (Book_ID integer,
                                                                    Genre text,
                                                                    Title text,
                                                                    Author text,
                                                                    Purchase_Price_£ integer,
                                                                    Purchase_Date text);'''

        Drop_Book_Table = """DROP TABLE IF EXISTS Books;"""
        Drop_Genre_Table = """DROP TABLE IF EXISTS Genres;"""
        Drop_Author_Table = """DROP TABLE IF EXISTS Authors;"""
        Drop_Purchase_Table = """DROP TABLE IF EXISTS Purchases;"""
        Drop_Reservation_Table = """DROP TABLE IF EXISTS Reservations;"""
        Drop_DupData_Table = """DROP TABLE IF EXISTS DupData;"""

        cstates = [Create_Book_Table,Create_Genre_Table,
                   Create_Author_Table,Create_Purchases_Table,
                   Create_Reservation_Table,Create_DupData_Table] #List of all the create table queries generated above
        dstates = [Drop_Book_Table,Drop_Genre_Table,
                   Drop_Author_Table,Drop_Purchase_Table,
                   Drop_Reservation_Table] #List of the drop table queries generated above

        self.Drop_Table(dstates,5) #Start by dropping the existing tables
        self.Create_Table(cstates,6) #Recreate the tables
        self.Insert_Data() #Insert data into the tables created
        self.Drop_Table([Drop_DupData_Table]) #Drop the duplicate data table
        self.cursor.close() #Close the cursor
        self.connection.close() #Close the connection

####TESTING####
def Test1():
    Database_Test = Database()
    SQLStatement = """SELECT B.Book_ID,B.Title,G.Genre,A.Author,B.Loan_Availability from (((((Purchases P JOIN Books B ON B.Book_ID = P.BPID)
                                            JOIN Genres G ON G.Genre_ID = P.GID)
                                            JOIN Authors A ON A.Author_ID = P.AID)
                                            JOIN Reservations R ON R.BID = P.BPID))
                                            WHERE TITLE LIKE "{}%";  """.format("Harry")
    Res = Database_Test.RunSQL_Return(SQLStatement)
    print(Res)

def Test2():

    Database_Test = Database()
    # Row should be added to the database table reservations
    SQLStatement = """INSERT INTO Reservations (BID,Checkout_Date,Member_ID) VALUES ({},"{}",{});""".format(3,"10/01/2016",1002)
    Database_Test.RunSQL_Update(SQLStatement)

def Test3():
    Database_Test = Database()
    # Row should be removed from the database
    SQLStatement = """DELETE FROM Reservations WHERE BID = 3 and Member_ID = 1002;"""
    Database_Test.RunSQL_Update(SQLStatement)

if __name__ == "__main__":
    Test1()#Select from database
    Test2()#Insert into database
    Test3()#Delete from database
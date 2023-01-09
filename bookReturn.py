# Student Number: F230551
# Date: 11/11/2022
# Version 7
# bookReturn.py file containing all the operations to do with returning books to the library
import database #Importing the database file
from datetime import date #Importing date function

class BookReturn():
    '''
    Class containing functions that return a book
    '''
    def __init__(self):
        '''
        initialise by creating the database object
        '''
        conn = database.Database()
        self.dr = conn

    def Return(self,Book_ID=0):
        '''
        Returning a book back to the library
        :param Book_ID: Book that needs to be returned
        :return: Message regarding the return
        '''
        td = date.today()#Find todays date
        Date = td.strftime("%d/%m/%Y")# Format todays date into wanted format dd/mm/yyyy
        ret = self.dr.RunSQL_Return("SELECT * FROM Books;")#Select all the books from the book file
        Book_ID = int(Book_ID) #Convert Book ID into integer

        if Book_ID in ret['Book_ID'].values:#Check if book id is valid
            # Run Sql statements to find the availability and reservation status
            Available = self.dr.RunSQL_Return("SELECT * FROM Books WHERE Book_ID == {};".format(Book_ID))
            Reservation = self.dr.RunSQL_Return("""SELECT * FROM Reservations WHERE BID == {} 
                                                            AND Reservation_Date is not NULL;
                                                """.format(Book_ID))
            if None in Reservation["Reservation_Date"].values:#Check book is not reserved for message
                # checking availability of book if not available then continue otherwise fall into else
                if "Not Available" in Available["Loan_Availability"].values:
                    SQLStatement = """UPDATE Reservations SET Return_Date = "{}"
                                        WHERE BID == {}
                                        AND Checkout_Date IS NOT NULL 
                                        AND Return_Date IS NULL; """.format(Date,Book_ID)

                    SQLStatement2 = """UPDATE Books SET Loan_Availability = "Available" 
                                        WHERE Book_ID == {}""".format(Book_ID)

                    # Running the SQLStatements generated above which update the return date and loan_availability
                    self.dr.RunSQL_Update(SQLStatement)
                    self.dr.RunSQL_Update(SQLStatement2)

                    return "Successful Return" # Returning message that transaction successful

                else:
                    return "Book is already available"

            else:
                SQLStatement = """UPDATE Reservations SET Return_Date = "{}"
                                                        WHERE BID == {}
                                                        AND Checkout_Date IS NOT NULL 
                                                        AND Return_Date IS NULL; """.format(Date, Book_ID)

                SQLStatement2 = """UPDATE Books SET Loan_Availability = "Available" 
                                                        WHERE Book_ID == {}""".format(Book_ID)
                self.dr.RunSQL_Update(SQLStatement)
                self.dr.RunSQL_Update(SQLStatement2)

                #selecting the reserved book information
                Reserved = self.dr.RunSQL_Return("""SELECT * FROM Reservations WHERE BID == {} 
                                                                            AND Checkout_Date is NULL
                                                                            AND Return_Date is NULL
                                                                            AND Reservation_Date is not NULL;
                                                                            """.format(Book_ID))
                Reserved_Member = Reserved["Member_ID"].to_list()#Grabbing the Member ID column and converting into list
                if Reserved_Member != []:#Checking that the list is not empty
                    return "Successful Return, Reservation has been made by Member {}".format(Reserved_Member[0])
                else:
                    return "Successful Return"

        else:
            return "Book ID is not Valid"

    def Not_Available_Books(self):
        """
        Function selecting the unavailable books
        :return: Unavailable books
        """
        Result = self.dr.RunSQL_Return("""SELECT B.Book_ID,B.Title,G.Genre,A.Author,B.Loan_Availability from 
                                ((((Purchases P JOIN Books B ON B.Book_ID = P.BPID) 
                                                JOIN Genres G ON G.Genre_ID = P.GID) 
                                                JOIN Authors A ON A.Author_ID = P.AID))
                                                WHERE B.Loan_Availability == "Not Available"  """)
        return Result

def Test1():
    print("""Not Available Expected Output:
       Book_ID                                     Title    Genre           Author Loan_Availability
0        2  Harry Potter and the Philosopher's Stone  Fantasy     J.K. Rowling     Not Available
1        9                                  Twilight  Romance  Stephenie Meyer     Not Available
    """)
    result = ReturnTest.Not_Available_Books()
    print("Not Available Actual Output:\n",result.to_string())

def Test2():
    print("""Non-Existent Book ID Expected Output:
Book ID is not Valid
    """)
    result = ReturnTest.Return(53)
    print("Non-Existent Book ID Actual Output:\n",result)

def Test3():
    print("""Returned and Reserved by another member Expected Output:
Successful Return, Reservation has been made by Member 6319
    """)
    result = ReturnTest.Return(5)
    print("Returned and Reserved by another member Actual Output:\n",result)

if __name__ == "__main__":
    ReturnTest = BookReturn()
    Test1()
    Test2()
    Test3()
# Student Number: F230551
# Date: 11/11/2022
# Version 11
# bookCheckout.py file containing all the operations to do with checking out books from the library
import database
from datetime import date

class BookCheckout():
    '''
    Class containing functionality for checking out and reserving books
    '''
    def __init__(self):
        '''
        Initialises the database, sets the flag to defualt false and creates a parameter for the class "date"
        '''
        conn = database.Database()
        self.dc = conn
        flag = False
        self.flag = flag
        #Same functionality as shown in bookReturn.py
        td = date.today()
        Date = td.strftime("%d/%m/%Y")
        self.date = Date

    def Checkout(self,Book_ID,Member_ID):

        res = self.dc.RunSQL_Return("SELECT Book_ID FROM Books;")

        Book_ID = int(Book_ID)
        Member_ID = int(Member_ID)

        if Book_ID in res['Book_ID'].values:#Check if the book id is valid
            #Run sql statements to determine the availability, if the same person has
            # checked out and if there is any existing reservations
            Available = self.dc.RunSQL_Return("SELECT * FROM Books WHERE Book_ID == {};".format(Book_ID))
            Existing_Checkout = self.dc.RunSQL_Return(
                """SELECT * FROM Reservations WHERE BID = {} AND Member_ID = {} 
                                                             AND Checkout_Date is NOT NULL
                                                             AND Return_Date is NULL""".format(Book_ID, Member_ID))


            Existing_Reservation = self.dc.RunSQL_Return("""SELECT * FROM Reservations WHERE BID = {} 
                                                                AND Reservation_Date is NOT NULL
                                                                AND Checkout_Date is NULL
                                                                AND Return_Date is NULL""".format(Book_ID,Member_ID))

            if Book_ID not in Existing_Checkout["BID"].values:#Checks that the person checking out isnt chekcing out the same book
                if 1000 <= Member_ID <= 9999:#Checks that the id is within the range
                    if ("Available" in Available["Loan_Availability"].values): #Checking the availability of a book
                        if Book_ID in Existing_Reservation["BID"].values:#Checking if the book ID is a existing reservations
                            if Member_ID in Existing_Reservation["Member_ID"].values: #Checking if the member id matches with the book id
                                SQLStatement = """UPDATE Reservations SET Checkout_Date = "{}"
                                                            WHERE BID == {} 
                                                            AND Member_ID == {};""".format(self.date, Book_ID,Member_ID)

                                SQLStatement_Available = """UPDATE Books SET Loan_Availability = "Not Available" 
                                                                                WHERE Book_ID = "{}"; """.format(Book_ID)
                                #Run the sql statements generated above
                                self.dc.RunSQL_Update(SQLStatement)
                                self.dc.RunSQL_Update(SQLStatement_Available)
                                #Return a message saying the reserved member checked out the book
                                return "Successful Checkout, Member {} who reserved has checked out".format(Member_ID), self.flag

                            else:#Otherwise inform the librarian that the book is reserved
                                Member_Reserve = self.dc.RunSQL_Return("""SELECT Member_ID FROM Reservations WHERE BID = {}
                                                                            AND Reservation_Date is NOT NULL
                                                                            AND Checkout_Date is NULL
                                                                            AND Return_Date is NULL""".format(Book_ID))
                                Reserved_Member = Member_Reserve["Member_ID"].to_list()#from the data above convert into a list
                                return "Book is reserved by Member {}".format(Reserved_Member[0]), self.flag

                        else:#Otherwise allow checkout of the book if no existing reservation made
                            SQLStatement = """INSERT INTO Reservations (BID, Checkout_Date ,Member_ID) 
                                                    VALUES ({},"{}",{}); """.format(Book_ID, self.date, Member_ID)

                            SQLStatement_Available = """UPDATE Books SET Loan_Availability = "Not Available" 
                                                                        WHERE Book_ID = "{}"; """.format(Book_ID)

                            self.dc.RunSQL_Update(SQLStatement)
                            self.dc.RunSQL_Update(SQLStatement_Available)
                            return "Successful Checkout", self.flag

                    elif Book_ID not in Existing_Reservation["BID"].values:# Checking if book id in existing reservations
                        self.flag = True #Set the flag to true
                        return "Book is not available, Reservation can be made", self.flag #Return reservation availability

                    else:#otherwise display the book is not available and is reserved
                        return "Existing Reservation, Can not Reserve", self.flag

                else:
                    return "Member id is not Valid", self.flag

            else:
                return "Existing Checkout made, Can not reserve", self.flag

        else:
            return "Book does not exist", self.flag

    def Reserve(self,Book_ID,Member_ID):
        """
        Function enabling the reservation of a book
        :param Book_ID: Book that will be reserved
        :param Member_ID: Member reserving the book
        :return: Message regarding the reservation
        """
        Book_ID = int(Book_ID)#Converting into integer
        Member_ID = int(Member_ID)#Converting into integer
        #Running sql statements to pull all reservations in variable Reserved and Reservations made for the book in
        # variable Reservation
        Reservation = self.dc.RunSQL_Return(
            """SELECT Reservation_Date FROM Reservations WHERE BID == {} 
                                                AND Checkout_Date IS NULL 
                                                AND Return_Date IS NULL;""".format(Book_ID))

        Reserved = self.dc.RunSQL_Return(
            "SELECT * FROM Reservations WHERE BID == {};".format(Book_ID))

        if None not in Reservation["Reservation_Date"].values:#Checking reservation is not existent
            # Ensuring book can be reserved if the chekout and return dates are respectively null
            if None not in Reserved["Checkout_Date"].values and None in Reserved["Return_Date"].values:
                SQLStatement = """INSERT INTO Reservations (BID,Reservation_Date,Member_ID) 
                                                    VALUES ({},"{}",{})""".format(Book_ID, self.date, Member_ID)

                self.dc.RunSQL_Update(SQLStatement)
                return "Book has been reserved", self.flag

            else:
                return "Reservation can not be made", self.flag
        else:
            return "Existing Reservation, Can not reserve", self.flag

    def Available_Books(self):
        """
        Function that selects the available books
        :return: Available books
        """
        Result = self.dc.RunSQL_Return("""SELECT B.Book_ID,B.Title,G.Genre,A.Author,B.Loan_Availability from 
                                ((((Purchases P JOIN Books B ON B.Book_ID = P.BPID) 
                                                JOIN Genres G ON G.Genre_ID = P.GID) 
                                                JOIN Authors A ON A.Author_ID = P.AID))
                                                WHERE B.Loan_Availability == "Available"  """)
        return Result

def Test1():
    print("""Book Reserved Expected Output:
Book is reserved by member 6319
    """)
    result = CheckoutTest.Checkout(5,1234)
    print("Book Reserved Actual Output:\n",result[0])

def Test2():
    print("""Reserved Member Checkout Expected Output:
Successful Checkout, Member 6319 who reserved has checked out
    """)
    result = CheckoutTest.Checkout(5, 6319)
    print("Reserved Member Checkout Actual Output:\n",result[0])

def Test3():
    print("""Successful Checkout Expected Output:
Successful Checkout
    """)
    result = CheckoutTest.Checkout(11, 4567)
    print("Successful Checkout Actual Output:\n",result[0])

if __name__ == "__main__":
    CheckoutTest = BookCheckout()
    Test1()
    Test2()
    Test3()
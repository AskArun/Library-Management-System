# Student Number: F230551
# Date: 11/11/2022
# Version 5
# bookSearch.py file containing all the operations to do with searching the database for books
import database

def Reset_DB():
    '''
    Initialise the DB button calls this function from the menu
    :return: None
    '''
    database.Initialise_DB()#Calling the class in the database function that will initialise the database again

class BookSearch():
    '''
    Class contains functionality for book search
    '''
    def __init__(self):
        '''
        Initialising the database object and setting to self.d
        '''
        conn = database.Database()
        self.d = conn

    def Search(self,Data=""):
        '''
        Function that runs the search functionality in the GUI by
        passing a query to the database and returning the result
        :param Data: Input from the user to insert into query
        :return: Dataframe of selected values named "res"
        '''
        # Select statement for selecting books which have a similar
        # title, genre or author to the data passed to the function
        SQLStatement = """SELECT B.Book_ID,B.Title,G.Genre,A.Author,P.Purchase_Price_£,P.Purchase_Date,B.Loan_Availability from 
                                ((((Purchases P JOIN Books B ON B.Book_ID = P.BPID) 
                                                JOIN Genres G ON G.Genre_ID = P.GID) 
                                                JOIN Authors A ON A.Author_ID = P.AID))
                                                WHERE TITLE LIKE "%{}%" 
                                                OR GENRE LIKE "%{}%" 
                                                OR AUTHOR LIKE "%{}%"; """.format(Data,Data,Data)

        res = self.d.RunSQL_Return(SQLStatement)#Runs the statement and saves the result in the variable res
        return res

def Test1():

    print("""Title Search Test Expected Outcome:
       Book_ID                                     Title    Genre        Author  Purchase_Price_£ Purchase_Date Loan_Availability
0        2  Harry Potter and the Philosopher's Stone  Fantasy  J.K. Rowling                11    12/12/2012     Not Available
1        3  Harry Potter and the Philosopher's Stone  Fantasy  J.K. Rowling                11    01/01/2014         Available
2        4  Harry Potter and the Philosopher's Stone  Fantasy  J.K. Rowling                11    01/01/2014         Available
3        5  Harry Potter and the Philosopher's Stone  Fantasy  J.K. Rowling                11    12/12/2012         Available
4        6  Harry Potter and the Philosopher's Stone  Fantasy  J.K. Rowling                11    12/12/2012         Available
5        7  Harry Potter and the Philosopher's Stone  Fantasy  J.K. Rowling                11    26/09/2020         Available
6        8  Harry Potter and the Philosopher's Stone  Fantasy  J.K. Rowling                11    01/01/2014         Available
    """)
    result = SearchTest.Search("Harry Potter")
    print("Title Search Test Actual Outcome:\n",result.to_string())

def Test2():
    print("""\n#########################################################################################################
Genre Search Test Expected Outcome:
        Book_ID                               Title    Genre           Author  Purchase_Price_£ Purchase_Date Loan_Availability
0        19              The Fault in Our Stars  Fiction       John Green                12    26/09/2020         Available
1        20              The Fault in Our Stars  Fiction       John Green                12    26/09/2020         Available
2        21              The Fault in Our Stars  Fiction       John Green                12    26/09/2020         Available
3        22              The Fault in Our Stars  Fiction       John Green                12    29/09/2020         Available
4        23  The Hobbit or There and Back Again  Fiction   J.R.R. Tolkien                 8    19/10/2014         Available
5        24  The Hobbit or There and Back Again  Fiction   J.R.R. Tolkien                 8    19/10/2014         Available
6        34                 Pride and Prejudice  Fiction      Jane Austen                19    28/08/2017         Available
7        35                    The Kite Runner   Fiction  Khaled Hosseini                 5    12/12/2012         Available
8        36                    The Kite Runner   Fiction  Khaled Hosseini                 5    12/12/2012         Available
9        37                    The Kite Runner   Fiction  Khaled Hosseini                 5    19/10/2014         Available
10       38                    The Kite Runner   Fiction  Khaled Hosseini                 5    12/12/2012         Available
    """)
    result = SearchTest.Search("Fiction")
    print("Genre Search Test Actual Outcome:\n",result.to_string())

def Test3():
    print("""\n#########################################################################################################
Author Search Test Expected Outcome:
   Book_ID                   Title    Genre      Author  Purchase_Price_£ Purchase_Date Loan_Availability
0       19  The Fault in Our Stars  Fiction  John Green                12    26/09/2020         Available
1       20  The Fault in Our Stars  Fiction  John Green                12    26/09/2020         Available
2       21  The Fault in Our Stars  Fiction  John Green                12    26/09/2020         Available
3       22  The Fault in Our Stars  Fiction  John Green                12    29/09/2020         Available
    """)
    result = SearchTest.Search("John Green")
    print("Author Search Test Actual Outcome:\n",result.to_string())

if __name__ == "__main__":
    SearchTest = BookSearch()
    Test1()#Testing the search functionality for title
    Test2()#Testing the search functionality for genre
    Test3()#Testing the search functionality for author
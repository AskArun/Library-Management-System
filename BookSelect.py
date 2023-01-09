# Student Number: F230551
# Date: 11/11/2022
# Version 5
# BookSelect.py file containing all the operations to do with recommending books to purchase for the library
import pandas as pd

import database
import matplotlib.pyplot as plt  # Importing matplotlib to create the graphs of the most popular titles and genres
# The imports below are used to make the dot code produce a database schema of my tables
from graphviz import Source
import tempfile

class BookSelect():
    """
    handles all the recommendation part of the system
    """
    def __init__(self):
        """
        Initialise the database object
        """
        conn = database.Database()
        self.ds = conn

    def Popular_Titles(self):
        """
        Selects all the popular titles the total price for each title and a count of the book ids
        :return: The data grouped by Title and ordered by total price selected
        """
        SQLStatement = """SELECT COUNT(B.Book_ID) AS "Count",
                                B.Title,SUM(P.Purchase_Price_£) AS "Price_Total", P.Purchase_Price_£ AS "Price" from 
                                                                (((((Purchases P JOIN Books B ON B.Book_ID = P.BPID) 
                                                                JOIN Genres G ON G.Genre_ID = P.GID) 
                                                                JOIN Authors A ON A.Author_ID = P.AID)
                                                                JOIN Reservations R ON R.BID = B.Book_ID))
                                                                GROUP BY TITLE ORDER BY SUM(P.Purchase_Price_£) DESC;  """
        result = self.ds.RunSQL_Return(SQLStatement)

        return result

    def Popular_Genres(self):
        """
        Selects the Genre, total price and count of book ids
        :return: The data grouped by the Genre and ordered by the total price selected
        """
        SQLStatement = """SELECT COUNT(B.Book_ID) as "Count",
                                G.Genre,SUM(P.Purchase_Price_£) AS "Price_Total", P.Purchase_Price_£ AS "Price" from 
                                                        (((((Purchases P JOIN Books B ON B.Book_ID = P.BPID) 
                                                        JOIN Genres G ON G.Genre_ID = P.GID) 
                                                        JOIN Authors A ON A.Author_ID = P.AID)
                                                        JOIN Reservations R ON R.BID = B.Book_ID))
                                                        GROUP BY GENRE ORDER BY SUM(P.Purchase_Price_£) DESC; """
        result = self.ds.RunSQL_Return(SQLStatement)

        return result

    def Recommend(self,budget=0):
        """
        Recommending the books to purchase and how many copies
        :param budget: How much budget the librarian has entered that the library has
        :return: 2 dataframes of recommneded titles and genres with the amount to purchase as well
        """
        Popular_Titles = self.Popular_Titles()# Calling the Popular titles function to retrieve the most occuring titles
        Popular_Genres = self.Popular_Genres()# Calling the Popular genres function to retrieve the most occuring genres

        #Two empty lists for computation of recommendation to be added
        list_of_recommendations_titles = []
        list_of_recommendations_genres = []

        for i in range(len(Popular_Titles)): #Iterates through the data from the popular titles function
            if budget > Popular_Titles['Price_Total'][i]: # Checks to see if the budget is enough for the title
                # If it is enough calculate the number of books that can be bought for that title
                Number_of_Purchases_Titles = int(round(budget // Popular_Titles['Price'][i], 0))
                #Append the title and the amount suggested to the recommended titles list
                list_of_recommendations_titles.append([Popular_Titles['Title'][i],Number_of_Purchases_Titles])

        for i in range(len(Popular_Genres)): #Iterates through the most popular genres
            if budget > Popular_Genres['Price_Total'][i]: #Checks if the budget is enough for purchase
                #Calculates how many books can be purchased for that genre
                Number_of_Purchases_Genres = int(round(budget // Popular_Genres['Price'][i]))
                #Appends the genre and the amount to purchase to the recommended genres list
                list_of_recommendations_genres.append([Popular_Genres['Genre'][i],Number_of_Purchases_Genres])

        #Converting the lists into dataframes for easier data manipulation later
        Recommend_Titles = pd.DataFrame(list_of_recommendations_titles,columns=["Title","Amount of Purchase"])
        Recommend_Genres = pd.DataFrame(list_of_recommendations_genres,columns=["Genre","Amount of Purchase"])

        return Recommend_Titles,Recommend_Genres

class Show_Plot(BookSelect):
    """
    Show the graphs of the most popular genres and inherit from the BookSelect method
    """
    def __init__(self):
        """
        Initialise the program by first initialising the database object in the inherited class.
        Then create a variable that can be used throughout the program for the figure
        """
        super().__init__()
        fig = plt.figure(figsize=(9,4))#Set the figure size and create the figure
        self.fig = fig
    def Graph_Popular_Titles(self):
        """
        Selects data grouped by title and ordered by count(book id)
        :return: data selected from the sql statement
        """
        SQLStatement = """SELECT COUNT(B.Book_ID) AS "Count",B.Title from 
                                                                (((((Purchases P JOIN Books B ON B.Book_ID = P.BPID) 
                                                                JOIN Genres G ON G.Genre_ID = P.GID) 
                                                                JOIN Authors A ON A.Author_ID = P.AID)
                                                                JOIN Reservations R ON R.BID = B.Book_ID))
                                                                GROUP BY TITLE ORDER BY COUNT(B.Book_ID) DESC;  """
        result = self.ds.RunSQL_Return(SQLStatement)

        return result

    def Graph_Popular_Genres(self):
        """
        Selects the data grouped by genre and ordered by count(book id)
        :return: Data selected from the query
        """
        SQLStatement = """SELECT COUNT(B.Book_ID) as "Count",Genre from 
                                                        (((((Purchases P JOIN Books B ON B.Book_ID = P.BPID) 
                                                        JOIN Genres G ON G.Genre_ID = P.GID) 
                                                        JOIN Authors A ON A.Author_ID = P.AID)
                                                        JOIN Reservations R ON R.BID = B.Book_ID))
                                                        GROUP BY GENRE ORDER BY COUNT(B.Book_ID) DESC; """
        result = self.ds.RunSQL_Return(SQLStatement)
        return result

    def Show_Graphs(self):
        """
        Creates the subplots and adjusts some parameters
        :return: figure of both subplots
        """
        #Call to the respective title and genre fucntions to find the most popular books
        result_title = self.Graph_Popular_Titles()
        result_genre = self.Graph_Popular_Genres()

        ax1 = self.fig.add_subplot(121) #creates an axis and subplot on that axis in position 1
        Labels_Titles = result_title['Title'].head().to_list() #Converts the pulled data title into a list
        Data_Titles = result_title['Count'].head().to_list() #Converts the pulled data count into a list
        ax1.barh(Labels_Titles,Data_Titles,align="center") #Creation of the horizontal bar plot using the data above
        ax1.set_title("Most Popular Titles")#Sets a title for the graph
        ax1.tick_params(axis='y', labelsize=7)#Changes the labelsize of the graphs

        #Conversion of the genre and count columns to lists
        Labels_Genres = result_genre['Genre'].head().to_list()
        Data_Genres = result_genre['Count'].head().to_list()
        ax2 = self.fig.add_subplot(122)#Placing the subplot in position 2 and creating another axis
        ax2.barh(Labels_Genres, Data_Genres, align="center")#Creation of horizontal bar plot for genres
        ax2.set_title("Most Popular Genres")
        ax2.tick_params(axis='y', labelsize=7)

        return self.fig

    def Show_Data_Model(self):
        """
        Produce a data model schema that would have been shown on the GUI
        :return: None
        """
        dot_code = """
        graph {
        layout=neato
        node [shape=box]; Books; Genres; Authors; Purchases; Reservations;
        node [shape=ellipse]; Book_ID; Title; Genre_ID; Genre; Author_ID; Author; Purchase_Price_£; Purchase_Date; Reservation_Date; Checkout_Date; Return_Date; Member_ID; Transaction_ID; Loan_Availability;
        
        Book_ID -- Books;
        Title -- Books;
        Loan_Availability -- Books;
        
        Genre_ID -- Genres;
        Genre -- Genres;
        
        Author_ID -- Authors;
        Author -- Authors;
        
        Book_ID -- Purchases;
        Genre_ID -- Purchases;
        Author_ID -- Purchases;
        Purchase_Price_£ -- Purchases;
        Purchase_Date -- Purchases;
        
        Book_ID -- Reservations;
        Reservation_Date -- Reservations;
        Checkout_Date -- Reservations;
        Return_Date -- Reservations;
        Member_ID -- Reservations;
        
        Reservations -- Books;
        Purchases -- Books;
        Purchases -- Genres;
        Purchases -- Authors;
        }
        """
        src = Source(dot_code,format="png")
        Temp = tempfile.mktemp()
        src.render(Temp, view=True)#Error on this line

        x = plt.imread(Temp + ".png")
        x.shape
        plt.imshow(x)
        plt.axis('off')
        plt.show()

def Test1():
    print("""Recommendation for budget of £200 Titles Expected Output:
                                     Title  Amount of Purchase
0               To Kill a Mockingbird                   5
1                    Angels & Demons                   28
2                 Pride and Prejudice                  10
3                    The Kite Runner                   40
4                    The Hunger Games                  20
5                Nineteen Eighty-Four                  22
6  The Hobbit or There and Back Again                  25
7                    The Great Gatsby                  40

Recommendation for budget of £200 Genres Expected Output:
        Genre  Amount of Purchase
0   Thriller                  28
1  Dystopian                  20
    """)
    result,result2 = SelectTest.Recommend(200)
    print("\nRecommendation for budget of £200 Titles Actual Output:\n",result)
    print("Recommendation for budget of £200 Genres Actual Output:\n",result2)

def Test2():
    print("""Expected Output: Subplots showing the most popular book titles and genres""")
    fig = Show_Plot().Show_Graphs()
    plt.show()

def Test3():
    print("""Expected Output: Data schema of Library.db""")
    Show_Plot().Show_Data_Model()

if __name__ == "__main__":
    SelectTest = BookSelect()
    Test1()  # Test the Recommendation algorithm for £200 budget
    Test2()  # Show the graphs of most popular titles and genres
    Test3()  # Shows the database schema

# Student Number: F230551
# Date: 11/11/2022
# Version 11
# menu.py file containing all the operations to do with the development of the GUI
#Importing libraries that will be used throughout the program
from tkinter import *
from tkinter import ttk
import tkinter.font as font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#importing the files created for particular functionality
import bookSearch #Searching for books
import bookCheckout #Checking out or reserving books out of the library
import bookReturn #Returning books to the library
import BookSelect #Recommending books to purchase and how many as well producing plots to be seen

class Menu():
    '''
    Class contains functionality for searching, returning, checking out and recommending books on the gui
    '''
    def __init__(self):
        """
        Initialising the GUI variables and Home page
        """
        root = Tk() #Creating the root window
        Tracing_Variable = StringVar()#Setting the variable to stringvar to allow for tracing
        self.Tracing_Variable = Tracing_Variable
        self.root = root
        self.root.configure(background="#C2C8C6")#Changing the background colour of the screen

        self.Tracing_Variable.trace_variable("w", self.Search_Book)  # Tracing the stringvar variable "Tracing_Variable"

        #Creating all the buttons that are used throughout the program
        SearchButton = Button(self.root, text="Search", command=self.Search,bg="#DCD7C9")
        CheckoutButton = Button(self.root, text="Checkout", command=self.Checkout,bg="#DCD7C9")
        ReturnButton = Button(self.root, text="Return", command=self.Return,bg="#DCD7C9")
        SelectBookButton = Button(self.root, text="Purchase Books", command=self.Select,bg="#DCD7C9")
        InitialiseDB_Button = Button(self.root, text="Initialise DB", command=self.Initialise_DB,bg="#DCD7C9")
        Check_Button = Button(self.root, text="Checkout", command=self.Checkout_Book,bg="#DCD7C9")
        Reserve_Button = Button(self.root, text="Reserve", command=self.Reserve_Book,bg="#DCD7C9")
        Ret_Button = Button(self.root, text="Return", command=self.Return_Book,bg="#DCD7C9")
        Show_Popular = Button(self.root, text="Show Popular Graphs", command=self.Show_Popular_Books,bg="#DCD7C9")
        Select_Book = Button(self.root, text="Show Popular Books/Genres", command=self.Select_Book,bg="#DCD7C9")
        Back_To_Homepage = Button(self.root, text="Back to Home", command=self.Home,bg="#DCD7C9")

        #Setting the font size of the buttons
        FontSize = font.Font(size=11)
        self.FontSize = FontSize
        Back_To_Homepage['font'] = self.FontSize
        SearchButton['font'] = self.FontSize
        CheckoutButton['font'] = self.FontSize
        ReturnButton['font'] = self.FontSize
        InitialiseDB_Button['font'] = self.FontSize
        Check_Button['font'] = self.FontSize
        Reserve_Button['font'] = self.FontSize
        Ret_Button['font'] = self.FontSize
        Show_Popular['font'] = self.FontSize
        SelectBookButton['font'] = self.FontSize
        Select_Book['font'] = self.FontSize

        #Creating the variables apart of the class
        self.CheckButton = Check_Button
        self.ReserveButton = Reserve_Button
        self.RetButton = Ret_Button
        self.searchbutton = SearchButton
        self.checkoutbutton = CheckoutButton
        self.returnbutton = ReturnButton
        self.InitialiseDBButton = InitialiseDB_Button
        self.ShowPopular = Show_Popular
        self.SelectButton = SelectBookButton
        self.select = Select_Book
        self.submit = Back_To_Homepage

        #Creating, configuring and setting the class variables for all the reused labels
        # self.root is the frame or window the text is wanted
        # text="example" is the text that is wanted to be displayed
        # bg = background colour of the label
        self.resultLabel = Label(self.root, text="",bg="#C2C8C6")
        Home_Label = Label(self.root, text="WELCOME TO THE LIBRARY",bg="#C2C8C6")
        Home_Label.configure(font=("bold", 18))
        Checkout_Label = Label(self.root, text="Checkout Books from the Library",bg="#C2C8C6")
        Checkout_Label.configure(font=("bold", 18))
        self.CheckoutLabel = Checkout_Label
        Book_Label = Label(self.root, text="Enter a Book ID:",bg="#C2C8C6")
        self.BookLabel = Book_Label
        Member_Label = Label(self.root, text="Enter a Member ID:",bg="#C2C8C6")
        self.MemberLabel = Member_Label
        self.Home_Page = Home_Label
        Return_Label = Label(self.root, text="Return Books to the Library",bg="#C2C8C6")
        Return_Label.configure(font=("bold", 18))
        self.ReturnLabel = Return_Label
        Search_Label = Label(self.root, text="Search for Books in the Library",bg="#C2C8C6")
        Search_Label.configure(font=("bold", 18))
        self.SearchLabel = Search_Label
        Search_Entry_Label = Label(self.root, text="Start typing a book title, genre or author to search",bg="#C2C8C6")
        Search_Entry_Label.configure(font=("bold",11))
        self.SearchEntryLabel = Search_Entry_Label
        Popular_Label = Label(self.root, text="Popular Books and Genres in the Library",bg="#C2C8C6")
        Popular_Label.configure(font=("bold", 18))
        self.PopularLabel = Popular_Label
        Select_Frame_Label = Label(self.root, text="Recommendations for books to purchase dependent on Title and Genre",bg="#C2C8C6")
        Select_Frame_Label.configure(font=("bold", 18))
        self.SelectFrameLabel = Select_Frame_Label
        Select_Label = Label(self.root, text="Enter a Budget for the library:",bg="#C2C8C6")
        self.SelectLabel = Select_Label

        #Creating the common entry fields of the program
        Search_Entry = Entry(self.root, textvariable=self.Tracing_Variable)#Search field for the dynamic search
        Book_Entry_Field = Entry(self.root)
        Member_Entry_Field = Entry(self.root)
        Budget_Entry_Field = Entry(self.root)
        self.BookEntry = Book_Entry_Field
        self.MemberEntry = Member_Entry_Field
        self.SearchEntry = Search_Entry
        self.BudgetEntryField = Budget_Entry_Field

        # Creating the frames
        Search_Frame = Frame(self.root, width=900, height=500)
        Checkout_Frame = Frame(self.root, width=900, height=500)
        Return_Frame = Frame(self.root, width=900, height=500)
        Select_Frame = Frame(self.root, width=900, height=500)
        Popular_Books = Frame(self.root, width=1200, height=500)
        Home_Frame = Frame(self.root)
        self.SearchFrame = Search_Frame
        self.CheckoutFrame = Checkout_Frame
        self.ReturnFrame = Return_Frame
        self.HomeFrame = Home_Frame
        self.PopularBooksFrame = Popular_Books
        self.SelectFrame = Select_Frame

        """
        Creating 5 trees for different frames and inserting intitial data 
        - tree
        - tree1
        - tree2
        - tree3
        - tree4
        """
        #Setting the columns of the treeview the frame it will
        # sit in and defining to show the headings the height of headings
        tree = ttk.Treeview(self.SearchFrame, column=("Book_ID", "Genre", "Title",
                                          "Author", "Purchase_Price_£",
                                          "Purchase_Date", "Loan_Availability"), show='headings', height=10)
        self.tree = tree
        self.tree.column("Book_ID", anchor=CENTER, width=100)#Creating a column with width 100
        self.tree.heading("Book_ID", text="ID")# Renaming the column to ID
        self.tree.column("Title", anchor=CENTER, width=100)
        self.tree.heading("Title", text="Title")
        self.tree.column("Genre", anchor=CENTER, width=100)
        self.tree.heading("Genre", text="Genre")
        self.tree.column("Author", anchor=CENTER, width=100)
        self.tree.heading("Author", text="Author")
        self.tree.column("Purchase_Price_£", anchor=CENTER, width=100)
        self.tree.heading("Purchase_Price_£", text="Purchase_Price_£")
        self.tree.column("Purchase_Date", anchor=CENTER, width=100)
        self.tree.heading("Purchase_Date", text="Purchase_Date")
        self.tree.column("Loan_Availability", anchor=CENTER, width=100)
        self.tree.heading("Loan_Availability", text="Loan_Availability")

        tree1 = ttk.Treeview(self.CheckoutFrame, column=("Book_ID", "Genre", "Title",
                                                      "Author", "Loan_Availability"), show='headings', height=10)
        self.tree1 = tree1
        self.tree1.column("Book_ID", anchor=CENTER, width=100)
        self.tree1.heading("Book_ID", text="ID")
        self.tree1.column("Title", anchor=CENTER, width=100)
        self.tree1.heading("Title", text="Title")
        self.tree1.column("Genre", anchor=CENTER, width=100)
        self.tree1.heading("Genre", text="Genre")
        self.tree1.column("Author", anchor=CENTER, width=100)
        self.tree1.heading("Author", text="Author")
        self.tree1.column("Loan_Availability", anchor=CENTER, width=100)
        self.tree1.heading("Loan_Availability", text="Loan_Availability")
        res = bookCheckout.BookCheckout().Available_Books()
        for x in range(len(res)): #Iterating threw the dataframe
            df_row = res.iloc[x, :].to_list()#Pulling the row from the frame
            self.tree1.insert("", END, values=df_row)#Inserting the row into the treeview

        tree2 = ttk.Treeview(self.ReturnFrame, column=("Book_ID", "Genre", "Title",
                                                      "Author", "Loan_Availability"), show='headings', height=10)
        self.tree2 = tree2
        self.tree2.column("Book_ID", anchor=CENTER, width=100)
        self.tree2.heading("Book_ID", text="ID")
        self.tree2.column("Title", anchor=CENTER, width=100)
        self.tree2.heading("Title", text="Title")
        self.tree2.column("Genre", anchor=CENTER, width=100)
        self.tree2.heading("Genre", text="Genre")
        self.tree2.column("Author", anchor=CENTER, width=100)
        self.tree2.heading("Author", text="Author")
        self.tree2.column("Loan_Availability", anchor=CENTER, width=100)
        self.tree2.heading("Loan_Availability", text="Loan_Availability")
        res = bookReturn.BookReturn().Not_Available_Books()
        for x in range(len(res)):
            df_row = res.iloc[x, :].to_list()
            self.tree2.insert("", END, values=df_row)

        tree3 = ttk.Treeview(self.SelectFrame, column=("Title", "Amount of Purchase"), show='headings', height=10)
        self.tree3 = tree3
        self.tree3.column("Title", anchor=CENTER, width=225)
        self.tree3.heading("Title", text="Title")
        self.tree3.column("Amount of Purchase", anchor=CENTER, width=225)
        self.tree3.heading("Amount of Purchase", text="Purchase Amount")

        tree4 = ttk.Treeview(self.SelectFrame, column=("Genre", "Amount of Purchase"), show='headings', height=10)
        self.tree4 = tree4
        self.tree4.column("Genre", anchor=CENTER, width=225)
        self.tree4.heading("Genre", text="Genre")
        self.tree4.column("Amount of Purchase", anchor=CENTER, width=225)
        self.tree4.heading("Amount of Purchase", text="Purchase Amount")


        #Creating a plot by calling the function in the book select file then creating a canvas for that image to be
        # displayed on the window
        fig = BookSelect.Show_Plot().Show_Graphs()  # Retreiving th efigure from the function that produced it
        canvas = FigureCanvasTkAgg(fig, self.PopularBooksFrame)  # Creating a canvas for the fig on the frame
        self.canvas = canvas

        self.Home()  # Calling the home frame to be initialised
        self.root.geometry("950x525")  # Adjusting the window size when generated which fits my screen
        root.mainloop()

    #The clear all functions are required to dynamically reset the treeview
    def clear_all(self):
        for item in self.tree.get_children():#iterating through the rows in the treeview
            self.tree.delete(item)#deleting the relevant row

    def clear_all_checkout(self):
        for item in self.tree1.get_children():
            self.tree1.delete(item)

    def clear_all_return(self):
        for item in self.tree2.get_children():
            self.tree2.delete(item)

    def clear_all_titles(self):
        for item in self.tree3.get_children():
            self.tree3.delete(item)

    def clear_all_genres(self):
        for item in self.tree4.get_children():
            self.tree4.delete(item)

    def Home(self):
        """
        Home page of the Library system containing all the buttons for certain functionalities
        :return: None
        """
        #The block of code below forgets any widgets/frames from previous frames that were created
        self.SearchEntry.pack_forget()
        self.submit.pack_forget()
        self.tree.pack_forget()
        self.CheckoutLabel.pack_forget()
        self.BookLabel.pack_forget()
        self.MemberLabel.pack_forget()
        self.BookEntry.pack_forget()
        self.MemberEntry.pack_forget()
        self.CheckButton.pack_forget()
        self.RetButton.pack_forget()
        self.ReturnLabel.pack_forget()
        self.resultLabel.pack_forget()
        self.ReserveButton.pack_forget()
        self.SearchFrame.pack_forget()
        self.CheckoutFrame.pack_forget()
        self.ReturnFrame.pack_forget()
        self.SearchLabel.pack_forget()
        self.SearchEntryLabel.pack_forget()
        self.PopularBooksFrame.pack_forget()
        self.PopularLabel.pack_forget()
        self.SelectButton.pack_forget()
        self.SelectFrameLabel.pack_forget()
        self.SelectLabel.pack_forget()
        self.BudgetEntryField.pack_forget()
        self.SelectFrame.pack_forget()
        self.select.pack_forget()

        #Initialisation of the buttons for the main functionalities
        self.Home_Page.pack(pady=5)
        self.searchbutton.pack(pady=5)
        self.checkoutbutton.pack(pady=5)
        self.returnbutton.pack(pady=5)
        self.SelectButton.pack(pady=5)
        self.ShowPopular.pack(pady=5)
        self.InitialiseDBButton.pack(pady=5)

    def Search_Book(self,var, index, mode):
        """
        Updating the tree view everytime the variable is updated.
        :param var: Variable for callback
        :param index: Index if variable is a list
        :param mode: The mode of operation: read, write, update
        :return: None
        """
        Space = self.Tracing_Variable.get().isspace()#Checking if the user has typed spaces
        self.clear_all()
        if self.Tracing_Variable.get() != "":#Checking if the input field is blank or not
            if not Space:#Checking if there is any spaces typed instead of letters/numbers
                # Passing the data to the search function in the search file and storing the returned information in res
                res = bookSearch.BookSearch().Search(self.Tracing_Variable.get())
                for x in range(len(res)):#Iterating through the number of rows returned
                    df_row = res.iloc[x,:].to_list()#pulling the row and converting to a list
                    self.tree.insert("", END, values=df_row)#inserting the row into the treeview
            else:#If input is spaces return an error message
                self.resultLabel = Label(self.root, text="Not a valid Input", bg="#C2C8C6")#Label to be displayed to screen
                self.resultLabel.configure(font=("bold", 11))#Configuring the size of the label text
                self.resultLabel.after(2000, self.resultLabel.forget)
                self.resultLabel.pack()#Packing the label so that it can be displayed.

    def Search(self):
        """
        Search function that creates the frame and elements on the page
        :return:
        """
        #Forgets all the items on the home page
        self.Home_Page.pack_forget()
        self.searchbutton.pack_forget()
        self.checkoutbutton.pack_forget()
        self.returnbutton.pack_forget()
        self.InitialiseDBButton.pack_forget()
        self.ShowPopular.pack_forget()
        self.SelectButton.pack_forget()

        #Packing all the items of the frame in the relevant order
        self.SearchLabel.pack()
        self.SearchEntryLabel.pack()
        self.SearchEntry.pack(pady=10)#padding the cell with 10 on each y direction
        self.SearchFrame.pack()
        self.tree.pack(expand=True, fill=BOTH) #Filling the search frame for a good view
        self.submit.pack(pady=10)

    def Checkout_Book(self):
        """
        Function for processing the checkout
        :return: None
        """
        Bvar = self.BookEntry.get()#Retrieving the book id data inputted
        Mvar = self.MemberEntry.get()#Retrieving the member id data inputted

        self.ReserveButton.pack_forget()#forgetting the reserve button if not falling in reservation needed
        if Bvar != "":#checking for user input
            if Mvar != "":#checking for user input
                result, flag = bookCheckout.BookCheckout().Checkout(Bvar, Mvar)#Retrieving and unpacking the result and flag from the checkout
                if flag: #Checking if a reservation needs to be made
                    self.ReserveButton.pack(pady=5)
                self.clear_all_checkout()#Clearing the treeview
                res = bookCheckout.BookCheckout().Available_Books()
                for x in range(len(res)):#Dynamically inserting the data from the dataframe "res" for available books
                    df_row = res.iloc[x, :].to_list()
                    self.tree1.insert("", END, values=df_row)
                self.resultLabel = Label(self.root, text=result,bg="#C2C8C6")#Displaying the message received for the function calculation above
                self.resultLabel.configure(font=("bold", 11))
                self.resultLabel.after(2000, self.resultLabel.forget)
            else:#Displays message regarding the error
                self.resultLabel = Label(self.root, text="Please enter a Member ID",bg="#C2C8C6")
                self.resultLabel.configure(font=("bold", 11))
                self.resultLabel.after(2000, self.resultLabel.forget)#forgetting the result label to prevent duplicate messages stacking
        else:
            self.resultLabel = Label(self.root, text="Please enter a Book ID",bg="#C2C8C6")
            self.resultLabel.configure(font=("bold", 11))
            self.resultLabel.after(2000, self.resultLabel.forget)

        self.resultLabel.pack()

    def Reserve_Book(self):
        """
        Function for processing the reservation of a book
        :return: None
        """
        Bvar = self.BookEntry.get()
        Mvar = self.MemberEntry.get()
        result, flag = bookCheckout.BookCheckout().Reserve(Bvar, Mvar)#Reserving a book and unpacking the flag and result
        self.resultLabel = Label(self.root, text=result,bg="#C2C8C6")
        self.resultLabel.configure(font=("bold", 11))
        self.resultLabel.after(2000, self.resultLabel.forget)
        self.resultLabel.pack()

    def Checkout(self):
        """
        Function handling most of the elements on the interface including position and location
        :return: None
        """
        self.Home_Page.pack_forget()
        self.searchbutton.pack_forget()
        self.checkoutbutton.pack_forget()
        self.returnbutton.pack_forget()
        self.InitialiseDBButton.pack_forget()
        self.ShowPopular.pack_forget()
        self.SelectButton.pack_forget()

        self.clear_all_checkout()
        res = bookCheckout.BookCheckout().Available_Books()
        for x in range(len(res)):
            df_row = res.iloc[x, :].to_list()
            self.tree1.insert("", END, values=df_row)

        #Placing all the relevant buttons, treeviews and labels in the correct order and location
        Book_ID = self.BookEntry
        Member_ID = self.MemberEntry
        self.CheckoutLabel.pack()
        self.BookLabel.pack()
        Book_ID.pack()
        self.MemberLabel.pack()
        Member_ID.pack()
        self.CheckButton.pack(pady=5)
        self.CheckoutFrame.pack()
        self.tree1.pack()
        self.submit.pack(pady=5)


    def Return_Book(self):
        """
        Function handling the return of a book
        :return: None
        """
        Bvar = self.BookEntry.get()

        if Bvar != "":
            result = bookReturn.BookReturn().Return(Bvar)#Returing the book and unpacking the information received
            self.clear_all_return()
            res = bookReturn.BookReturn().Not_Available_Books()
            for x in range(len(res)):#Dynamically inserting the not available books
                df_row = res.iloc[x, :].to_list()
                self.tree2.insert("", END, values=df_row)
            self.resultLabel = Label(self.root, text=result,bg="#C2C8C6")
            self.resultLabel.configure(font=("bold", 11))
            self.resultLabel.after(2000, self.resultLabel.forget)

        else:
            self.resultLabel = Label(self.root, text="No Input Entered",bg="#C2C8C6")
            self.resultLabel.configure(font=("bold", 11))
            self.resultLabel.after(2000, self.resultLabel.forget)
        self.resultLabel.pack()


    def Return(self):
        """
        Function handling the interface for the return of books to the library
        :return: None
        """
        self.Home_Page.pack_forget()
        self.searchbutton.pack_forget()
        self.checkoutbutton.pack_forget()
        self.returnbutton.pack_forget()
        self.InitialiseDBButton.pack_forget()
        self.ShowPopular.pack_forget()
        self.SelectButton.pack_forget()
        self.clear_all()

        self.clear_all_return()
        res = bookReturn.BookReturn().Not_Available_Books()
        for x in range(len(res)):#Dynamically inserting the not available books
            df_row = res.iloc[x, :].to_list()
            self.tree2.insert("", END, values=df_row)

        #Placing all the elements in the correct position
        Book_ID = self.BookEntry
        self.ReturnLabel.pack()
        self.BookLabel.pack()
        Book_ID.pack()
        self.RetButton.pack(pady=5)
        self.ReturnFrame.pack()
        self.tree2.pack()
        self.submit.pack(pady=5)

    def Select_Book(self):
        """
        Recommendation for the number of books to purchase for popular titles or genres
        :return: None
        """
        Budget = self.BudgetEntryField.get()
        self.clear_all_titles()
        self.clear_all_genres()
        if Budget != "":
            #Retrieving recommended titles and genres and the amount to buy accordingly
            Recommended_Titles, Recommended_Genres = BookSelect.BookSelect().Recommend(int(Budget))
            for x in range(len(Recommended_Titles)):#Iterate through the recommended titles dataframe
                df_row = Recommended_Titles.iloc[x, :].to_list()
                self.tree3.insert("", END, values=df_row)#Insert the row into the tree
            for x in range(len(Recommended_Genres)):#Iterate through the recommended genres dataframe
                df_row = Recommended_Genres.iloc[x, :].to_list()
                self.tree4.insert("", END, values=df_row)#Insert the row into the tree

        else:
            self.resultLabel = Label(self.root, text="Not a valid Input", bg="#C2C8C6")#Error message if there is no input
            self.resultLabel.configure(font=("bold",11))
            self.resultLabel.after(2000, self.resultLabel.forget)
            self.resultLabel.pack()

    def Select(self):
        """
        Function handling the interface of the Recommendation for books
        :return:
        """
        self.Home_Page.pack_forget()
        self.searchbutton.pack_forget()
        self.checkoutbutton.pack_forget()
        self.returnbutton.pack_forget()
        self.InitialiseDBButton.pack_forget()
        self.ShowPopular.pack_forget()
        self.SelectButton.pack_forget()

        #Placing all the items in the correct place
        self.SelectFrameLabel.pack()
        self.SelectLabel.pack()
        self.BudgetEntryField.pack(pady=5)
        self.select.pack(pady=5)
        self.SelectFrame.pack()
        self.tree3.pack(side=LEFT)
        self.tree4.pack(side=RIGHT)
        self.submit.pack(pady=10)

    def Show_Popular_Books(self):
        """
        Function showing the graphs for the most popular books and genres
        :return: None
        """
        self.Home_Page.pack_forget()
        self.searchbutton.pack_forget()
        self.checkoutbutton.pack_forget()
        self.returnbutton.pack_forget()
        self.InitialiseDBButton.pack_forget()
        self.ShowPopular.pack_forget()
        self.SelectButton.pack_forget()

        #Placing the items in the correct place
        self.PopularLabel.pack()
        self.PopularBooksFrame.pack(pady=10)
        self.canvas.get_tk_widget().pack()
        self.submit.pack(pady=10)

    def Initialise_DB(self):
        """
        Initialising the db to reset
        :return: None
        """
        bookSearch.Reset_DB()#Calling the relevant function to reset the database
        #Displaying a message once the db has been reset which disappears after 1200ms
        self.resultLabel = Label(self.root,text="Database Reset",bg="#C2C8C6")
        self.resultLabel.after(1200, self.resultLabel.forget)
        self.resultLabel.pack()



if __name__ == "__main__":#Only runs the code if the file is run and not called from another file
    Menu()

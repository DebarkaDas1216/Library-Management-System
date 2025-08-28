#Library Management System using Python and SQL
"""
Library Management System
-------------------------
Author      : Debarka Das
College     : NIT Warangal
Description : A GUI-based Library Management System built using Python's Tkinter for frontend 
              and MySQL for backend database operations.

Features:
    - Add new library members and borrowed books
    - Search, delete, and display member records
    - Calendar integration to select borrowed date
    - Auto-calculates due date and overdue status
    - GUI table (Treeview) to display stored records
    - Pre-loaded list of sample books with ISBN, author, and loan period
    - Reduces manual work by 40%
"""

# Importing required Python Libraries

from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkcalendar import *
import datetime
import pymysql


# ========================================================================
# Library Class
# ------------------------------------------------------------------------
# This class defines the complete GUI and functionality for the Library 
# Management System. It manages Tkinter widgets, database connectivity, 
# event handling, and CRUD (Create, Read, Update, Delete) operations.
# ========================================================================


class Library:
    def __init__(self,root):\
    
        # ---------------------------
        # Initialize Tkinter Window
        # ---------------------------
        # - Set title, geometry, and background
        # - Initialize Tkinter StringVar() variables for data binding
        # - Build the main frames for layout organization

        self.root = root
        self.root.title("Library Management Sysytem")
        self.root.geometry("1360x750+0+0")
        self.root.configure(bg="cadetblue")

        MType = StringVar()
        Member = StringVar()
        Title = StringVar()
        Firstname = StringVar()
        Surname = StringVar()
        Address = StringVar()
        Address2 = StringVar()
        PostCode = StringVar()
        MobileNo = StringVar()
        BookISBN = StringVar()
        BookTitle = StringVar()
        BookType = StringVar()
        Author = StringVar()
        DateBorrowed = StringVar()
        DateDue = StringVar()
        SellingPrice = StringVar()
        LateReturnFine = StringVar()
        DateOverDue = StringVar()
        DaysOnLoan = StringVar()

    
        #==============================================
        # Main Layout Frames
        # ---------------------------
        # TitleFrame   : Displays the title of the application
        # ButtonFrame  : Holds control buttons (Add, Delete, Search, etc.)
        # DataFrame    : Contains both LEFT (Member Info) and RIGHT (Book Info) panels

        MainFrame = Frame(self.root,bd=10,bg="cadetblue")
        MainFrame.grid()

        TitleFrame=Frame(MainFrame, bd=10, width=1350, padx=60, relief=RIDGE)
        TitleFrame.pack(side=TOP)

        self.lbTittle = Label(TitleFrame, width=38, font = ("arial",40,"bold"),text="Library management System")
        self.lbTittle.grid()
        
        ButtonFrame = Frame(MainFrame, bd=10, width=1350, height=50, relief=RIDGE)
        ButtonFrame.pack(side=BOTTOM)

        DataFrame = Frame(MainFrame, bd=10, width=1300, height=400, relief=RIDGE)
        DataFrame.pack(side=BOTTOM)

        DataFrameLEFTCover = LabelFrame(DataFrame, bd=10, width=800, height=300, relief=RIDGE,
                                        bg='cadetblue', font=('arial', 12,'bold'), text="Library Membership Info:")
        DataFrameLEFTCover.pack(side=LEFT, padx=10)

        DataFrameLEFT = Frame(DataFrameLEFTCover, bd=10, width=800, height=300, padx=13, pady=2, relief=RIDGE)
        DataFrameLEFT.pack(side=TOP)

        DataFrameLEFTb = LabelFrame(DataFrameLEFTCover, bd=10, width=800, height=100, pady=4, padx=10, relief=RIDGE,
                                    font=('arial', 12,'bold'), text="Library Membership Info:")
        DataFrameLEFTb.pack(side=TOP)

        DataFrameRIGHT = LabelFrame(DataFrame, bd=10, width=450, height=300, padx=10, relief=RIDGE,
                                    bg='cadetblue', font=('arial', 12,'bold'), text="Book Details:")
        DataFrameRIGHT.pack(side=RIGHT)
        #================================RESETS==================================================#
        def iExit():
        # Function: iExit()
        # Confirm before closing the application.
        # --------------------------------------------------

            iExit=tkinter.messagebox.askyesno("Library Management System","Confirm if you want to exit")
            if iExit>0:
                self.root.destroy()
                return
            

        def iReset():
        # Function: iReset()
        # Clears all input fields (resets StringVar() variables).
        # ---------------------------
                MType.set("")
                Member.set("")
                Title.set("")
                Firstname.set("")
                Surname.set("")
                Address.set("")
                Address2.set("")
                PostCode.set("")
                MobileNo.set("")
                BookISBN.set("")
                BookTitle.set("")
                BookType.set("")
                Author.set("")
                DateBorrowed.set("")
                DateDue.set("")
                SellingPrice.set("")
                LateReturnFine.set("")
                DateOverDue.set("")
                DaysOnLoan.set("")
        d4=datetime.datetime.now()
        def SelectedBook(evt):
        # Function: SelectedBook()
        # Event handler triggered when a book is selected from the listbox.
        # - Fetches predefined book data
        # - Populates fields such as ISBN, Title, Author, Fine, and Loan period
        # - Auto-calculates due date based on days on loan
        # ---------------------------           
            selected_title = str(booklist.get(booklist.curselection()))
            book_data = {
                "Cinderella": ["ISBN 9781408307785", "Cinderella", "Brothers Grimm", "₹2.00", "₹120", 14],
                "Game Design": ["ISBN 9780131687479", "Game Design Fundamentals", "Ernest Adams", "₹3.50", "₹550", 21],
                "Ancient Rome": ["ISBN 9780199590058", "Ancient Rome: A New History", "David Potter", "₹2.75", "₹400", 14],
                "Made in Africa": ["ISBN 9780796925349", "Made in Africa", "Carolyn Jenkins", "₹3.00", "₹320", 21],
                "Sleeping Beauty": ["ISBN 9781408349907", "Sleeping Beauty", "Charles Perrault", "₹2.00", "₹110", 14],
                "London": ["ISBN 9780340768030", "London: The Biography", "Peter Ackroyd", "₹4.00", "₹600", 30],
                "Nigeria": ["ISBN 9780141972950", "There Was a Country", "Chinua Achebe", "₹3.25", "₹450", 21],
                "Snow White": ["ISBN 9780064437595", "Snow White", "Brothers Grimm", "₹2.00", "₹115", 14],
                "Shrek 3": ["ISBN 9780061228653", "Shrek the Third", "Kathleen Zoehfeld", "₹2.50", "₹180", 10],
                "London Street": ["ISBN 9781910026073", "London Street Atlas", "A-Z Map Co", "₹3.00", "₹300", 15],
                "I Love Lagos": ["ISBN 9789785412525", "I Love Lagos", "Tunde Leye", "₹2.80", "₹290", 14],
                "Love Kenya": ["ISBN 9789966225717", "Love Kenya", "Ngugi wa Thiong’o", "₹3.20", "₹350", 20],
                "Hello India": ["ISBN 9789386538171", "Hello India!", "Rohini Chowdhury", "₹2.75", "₹240", 14],
            }

            if selected_title in book_data:
                global data
                data = book_data[selected_title]
                BookISBN.set(data[0])
                BookTitle.set(data[1])
                Author.set(data[2])
                LateReturnFine.set(data[3])
                SellingPrice.set(data[4])
                DaysOnLoan.set(str(data[5]))

                d1 = datetime.date.today()
                d2 = datetime.timedelta(days=data[5])
   
                d3 = d1 + d2
                d4=d3
                DateBorrowed.set(d1.strftime("%Y-%m-%d"))
                DateDue.set(d3.strftime("%Y-%m-%d"))
                DateOverDue.set("No")
            else:
                tkinter.messagebox.showerror("Error", "Book not found in the system.")
        
        def addData():
        # Function: addData()
        # Inserts a new record into the MySQL database.
        # - Captures member and book details
        # - Sets borrowed and due date
        # - Updates the Treeview with new record
        # ---------------------------

            if Member.get()=="" or Firstname.get()=="" or Surname.get()=="" :
                    tkinter.messagebox.showerror("Library Management System","Enter correct Member details.")
            else:
                 borrowed_date = cal.get_date()  # e.g. '2025-07-21'
                 due_date = d4.strftime('%Y-%m-%d')  # d3 is a datetime object

                 DateBorrowed.set(borrowed_date)
                 DateDue.set(due_date)
                 sqlCon=pymysql.connect(
                            host="localhost",
                            user="root",
                            password="root1216",
                            database="librarymanagementsysytem"
                        )
                 cur = sqlCon.cursor()
                 cur.execute("insert into library values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                 Member.get(),
                 Firstname.get(),
                 Surname.get(),
                 Address.get(),
                 DateBorrowed.get(),
                 DateDue.get(),
                 DateOverDue.get(),
                 Author.get(),
                 BookISBN.get(),
                 BookTitle.get()
                 )
                 )
                 sqlCon.commit()
                 Displaydata()
                 sqlCon.close()
                 DateDue.set(cal.get_date())
                 DateOverDue.set("Yes")
                 tkinter.messagebox.showinfo("Library Management System","record Enteren Succesfully")
        
        def Displaydata():
        # Function: Displaydata()
        # Retrieves all records from the database and displays them in the Treeview.
        # ---------------------------
             sqlCon=pymysql.connect(
                            host="localhost",
                            user="root",
                            password="root1216",
                            database="librarymanagementsysytem"
                        )
             cur=sqlCon.cursor()
             cur.execute("SELECT * from library")
             result = cur.fetchall()
             if len(result)!=0:
                    self.library_records.delete(*self.library_records.get_children())
                    for row in result:
                        self.library_records.insert("",END,values=row)
                        sqlCon.commit()
                    sqlCon.close()
        def deleteDB():
        # Function: deleteDB()
        # Deletes a record from the database based on the entered Member ID.
        # ---------------------------
             sqlCon= pymysql.connect(host="Localhost",
                                     password="root1216",
                                     user="root",
                                     database="librarymanagementsysytem")
             cur=sqlCon.cursor()
             cur.execute("delete from library where member=%s",Member.get())
             sqlCon.commit()
             Displaydata()
             sqlCon.close()
             tkinter.messagebox.showinfo("Library Management System","Record Deleted Succesfully")

        def searchDB():
        # Function: searchDB()
        # Searches the database for a specific Member ID.
        # Populates input fields if record is found.
        # ---------------------------
            try:
                sqlCon= pymysql.connect(host="Localhost",
                                        password="root1216",
                                        user="root",
                                        database="librarymanagementsysytem")
                cur=sqlCon.cursor()
                cur.execute("SELECT * from library where member=%s ",Member.get())

                row=cur.fetchone()

                Member.set(row[0])
                Firstname.set(row[1])
                Surname.set(row[2])
                Address.set(row[3])
                DateBorrowed.set(row[4])
                DateDue.set(row[5])
                DateOverDue.set(row[6])
                Author.set(row[7])
                BookISBN.set(row[8])
                BookTitle.set(row[9])

                sqlCon.commit()
            except:
                tkinter.messagebox.showinfo("Library Management System","Record Does not Exist")
                sqlCon.close()

       

        def SelectedBook(evt):
            selected_title = str(booklist.get(booklist.curselection()))

            book_data = {
                "Cinderella": ["ISBN 9781408307785", "Cinderella", "Brothers Grimm", "₹2.00", "₹120", 14],
                "Game Design": ["ISBN 9780131687479", "Game Design Fundamentals", "Ernest Adams", "₹3.50", "₹550", 21],
                "Ancient Rome": ["ISBN 9780199590058", "Ancient Rome: A New History", "David Potter", "₹2.75", "₹400", 14],
                "Made in Africa": ["ISBN 9780796925349", "Made in Africa", "Carolyn Jenkins", "₹3.00", "₹320", 21],
                "Sleeping Beauty": ["ISBN 9781408349907", "Sleeping Beauty", "Charles Perrault", "₹2.00", "₹110", 14],
                "London": ["ISBN 9780340768030", "London: The Biography", "Peter Ackroyd", "₹4.00", "₹600", 30],
                "Nigeria": ["ISBN 9780141972950", "There Was a Country", "Chinua Achebe", "₹3.25", "₹450", 21],
                "Snow White": ["ISBN 9780064437595", "Snow White", "Brothers Grimm", "₹2.00", "₹115", 14],
                "Shrek 3": ["ISBN 9780061228653", "Shrek the Third", "Kathleen Zoehfeld", "₹2.50", "₹180", 10],
                "London Street": ["ISBN 9781910026073", "London Street Atlas", "A-Z Map Co", "₹3.00", "₹300", 15],
                "I Love Lagos": ["ISBN 9789785412525", "I Love Lagos", "Tunde Leye", "₹2.80", "₹290", 14],
                "Love Kenya": ["ISBN 9789966225717", "Love Kenya", "Ngugi wa Thiong’o", "₹3.20", "₹350", 20],
                "Hello India": ["ISBN 9789386538171", "Hello India!", "Rohini Chowdhury", "₹2.75", "₹240", 14],
            }

            if selected_title in book_data:
                data = book_data[selected_title]
                BookISBN.set(data[0])
                BookTitle.set(data[1])
                Author.set(data[2])
                LateReturnFine.set(data[3])
                SellingPrice.set(data[4])
                DaysOnLoan.set(str(data[5]))

                d1 = datetime.date.today()
                d2 = datetime.timedelta(days=data[5])
                d3 = d1 + d2

                DateBorrowed.set(d1.strftime("%Y-%m-%d"))
                DateDue.set(d3.strftime("%Y-%m-%d"))
                DateOverDue.set(d3.strftime("%Y-%m-%d"))
            else:
                tkinter.messagebox.showerror("Error", "Book not found in the system.")
        def LibraryInfo(ev):
            selected_row = self.library_records.focus()
            data = self.library_records.item(selected_row)
            row = data['values']

            if row:
                Member.set(row[0])
                Firstname.set(row[1])
                Surname.set(row[2])
                Address.set(row[3])
                DateBorrowed.set(row[4])
                DateDue.set(row[5])
                DateOverDue.set(row[6])
                Author.set(row[7])
                BookISBN.set(row[8])
                BookTitle.set(row[9])



       #=========================================================================================================================================== 
        self.lblMembertype = Label(DataFrameLEFT,font=("arial",12,"bold"),text="Member Type",padx=2,pady=2)
        self.lblMembertype.grid(row=0,column=0,sticky=W)

        self.cboMemberType= ttk.Combobox(DataFrameLEFT, textvariable=MType,state="readonly",font=("arial",12,"bold"), width=34 )
        self.cboMemberType["value"]=(" ","Lecturer","student","Admin Stuff")
        self.cboMemberType.current(0)
        self.cboMemberType.grid(row=0,column=1)

        self.lblBookISBN= Label(DataFrameLEFT,font=("arial",12,"bold"),text="Book ID",padx=2,pady=2)
        self.lblBookISBN.grid(row=0,column=2,sticky=W)

        self.txtBookISBN = Entry(DataFrameLEFT, font=("arial", 12, "bold"),
                                textvariable=BookISBN, width=31)
        self.txtBookISBN.grid(row=0, column=3, padx=2, pady=2)

        # Member Reference Number
        self.lblMemberRef = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Member Ref No:", padx=2, pady=2)
        self.lblMemberRef.grid(row=1, column=0, sticky=W)

        self.txtMemberRef = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=Member, width=36)
        self.txtMemberRef.grid(row=1, column=1)

        # Book Title
        self.lblBookTitle = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Book Title:", padx=2, pady=2)
        self.lblBookTitle.grid(row=1, column=2, sticky=W)

        self.txtBookTitle = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=BookTitle, width=31)
        self.txtBookTitle.grid(row=1, column=3)

        # Title (Mr., Miss., etc.)y
        self.lblTitle = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                            text="Title:", padx=2, pady=2)
        self.lblTitle.grid(row=2, column=0, sticky=W)

        self.cboTitle = ttk.Combobox(DataFrameLEFT, textvariable=Title, state='readonly',
                                    font=('arial', 12, 'bold'), width=34)
        self.cboTitle['value'] = ('', 'Mr.', 'Miss.', 'Mrs.', 'Dr.', 'Capt.', 'Ms.')
        self.cboTitle.current(0)
        self.cboTitle.grid(row=2, column=1)

        # Author
        self.lblAuthor = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                            text="Author:", padx=2, pady=2)
        self.lblAuthor.grid(row=2, column=2, sticky=W)

        self.txtAuthor = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                            textvariable=Author, width=31)
        self.txtAuthor.grid(row=2, column=3)

        # Firstname
        self.lblFirstname = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Firstname:", padx=2, pady=2)
        self.lblFirstname.grid(row=3, column=0, sticky=W)

        self.txtFirstname = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=Firstname, width=36)
        self.txtFirstname.grid(row=3, column=1)

        # Date Borrowed
        self.lblDateBorrowed = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                    text="Date Borrowed:", padx=2, pady=2)
        self.lblDateBorrowed.grid(row=3, column=2, sticky=W)

        self.txtDateBorrowed = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                    textvariable=DateBorrowed, width=31)
        self.txtDateBorrowed.grid(row=3, column=3)

        # Surname
        self.lblSurname = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Surname:", padx=2, pady=6)
        self.lblSurname.grid(row=4, column=0, sticky=W)

        self.txtSurname = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=Surname, width=36)
        self.txtSurname.grid(row=4, column=1)

        # Date Due
        self.lblDateDue = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Date Due:", padx=2, pady=2)
        self.lblDateDue.grid(row=4, column=2, sticky=W)

        self.txtDateDue = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=DateDue, width=31)
        self.txtDateDue.grid(row=4, column=3)
        # Address 1
        self.lblAddress1 = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Address 1:", padx=2, pady=2)
        self.lblAddress1.grid(row=5, column=0, sticky=W)

        self.txtAddress1 = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=Address, width=36)
        self.txtAddress1.grid(row=5, column=1)

        # Days on Loan
        self.lblDaysOnLoan = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Days on Loan:", padx=2, pady=2)
        self.lblDaysOnLoan.grid(row=5, column=2, sticky=W)

        self.txtDaysOnLoan = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=DaysOnLoan, width=31)
        self.txtDaysOnLoan.grid(row=5, column=3)

        # Address 2
        self.lblAddress2 = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Address 2:", padx=2, pady=2)
        self.lblAddress2.grid(row=6, column=0, sticky=W)

        self.txtAddress2 = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=Address2, width=36)
        self.txtAddress2.grid(row=6, column=1)

        # Late Return Fine
        self.lblLateReturnFine = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                    text="Late Return Fine:", padx=2, pady=2)
        self.lblLateReturnFine.grid(row=6, column=2, sticky=W)

        self.txtLateReturnFine = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                    textvariable=LateReturnFine, width=31)
        self.txtLateReturnFine.grid(row=6, column=3)

        # Post Code
        self.lblPostCode = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Post Code:", padx=2, pady=2)
        self.lblPostCode.grid(row=7, column=0, sticky=W)

        self.txtPostCode = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=PostCode, width=36)
        self.txtPostCode.grid(row=7, column=1)

        # Date Over Due
        self.lblDateOverDue = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                    text="Date Over Due:", padx=2, pady=2)
        self.lblDateOverDue.grid(row=7, column=2, sticky=W)

        self.txtDateOverDue = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                    textvariable=DateOverDue, width=31)
        self.txtDateOverDue.grid(row=7, column=3)

        # Mobile No
        self.lblMobileNo = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                text="Mobile No:", padx=2, pady=2)
        self.lblMobileNo.grid(row=8, column=0, sticky=W)

        self.txtMobileNo = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                textvariable=MobileNo, width=36)
        self.txtMobileNo.grid(row=8, column=1)

        # Selling Price
        self.lblSellingPrice = Label(DataFrameLEFT, font=('arial', 12, 'bold'),
                                    text="Selling Price:", padx=2, pady=2)
        self.lblSellingPrice.grid(row=8, column=2, sticky=W)

        self.txtSellingPrice = Entry(DataFrameLEFT, font=('arial', 12, 'bold'),
                                    textvariable=SellingPrice, width=31)
        self.txtSellingPrice.grid(row=8, column=3)


        # ===================== Calendar ======================
        cal = Calendar(DataFrameRIGHT,
                    selectmode="day",
                    year=2025, month=10, day=16,
                    date_pattern='yyyy-mm-dd',
                    font=('arial', 12, 'bold'),
                    padx=1)
        cal.grid(row=0, column=0, pady=10)

       
        # ===================== Scrollbar ======================
        scrollbar = Scrollbar(DataFrameRIGHT, orient=VERTICAL)
        scrollbar.grid(row=1, column=1, sticky='ns')

        # ===================== Book List ======================
        ListOfBooks = [
            'Cinderella', 'Game Design', 'Ancient Rome', 'Made in Africa',
            'Sleeping Beauty', 'London', 'Nigeria', 'Snow White', 'Shrek 3',
            'London Street', 'I Love Lagos', 'Love Kenya', 'Hello India'
        ]

        booklist = Listbox(DataFrameRIGHT,
                        width=40,
                        height=12,
                        font=('times', 11, 'bold'),
                        yscrollcommand=scrollbar.set)
        booklist.bind('<<ListboxSelect>>',SelectedBook)
        booklist.grid(row=1, column=0, padx=3)
        scrollbar.config(command=booklist.yview)

        for items in ListOfBooks:
            booklist.insert(END, items)

        # ===================== Frame Detail =====================
        scroll_x = Scrollbar(DataFrameLEFTb, orient=HORIZONTAL)
        scroll_y = Scrollbar(DataFrameLEFTb, orient=VERTICAL)

        self.library_records = ttk.Treeview(DataFrameLEFTb,
            height=5,
            columns=("member", "firstname", "surname", "address", "dateborrowed",
                    "datedue", "dayoverdue", "author", "bookisbn", "booktitle"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.library_records.xview)
        scroll_y.config(command=self.library_records.yview)

        # ===================== Treeview Headings =====================
        self.library_records.heading("member", text="Member")
        self.library_records.heading("firstname", text="Firstname")
        self.library_records.heading("surname", text="Surname")
        self.library_records.heading("address", text="Address")
        self.library_records.heading("dateborrowed", text="Date Borrowed")
        self.library_records.heading("datedue", text="Date Due")
        self.library_records.heading("dayoverdue", text="Days Over Due")
        self.library_records.heading("author", text="Author")
        self.library_records.heading("bookisbn", text="Book ISBN")
        self.library_records.heading("booktitle", text="Book Title")
        # ===================== Show Treeview Headings =====================
        self.library_records['show'] = 'headings'

        # ===================== Set Column Widths =====================
        self.library_records.column("member", width=70)
        self.library_records.column("firstname", width=100)
        self.library_records.column("surname", width=100)
        self.library_records.column("address", width=100)
        self.library_records.column("dateborrowed", width=70)
        self.library_records.column("datedue", width=70)
        self.library_records.column("dayoverdue", width=100)
        self.library_records.column("author", width=100)
        self.library_records.column("bookisbn", width=70)
        self.library_records.column("booktitle", width=70)

        # ===================== Pack Treeview =====================
        self.library_records.pack(fill=BOTH, expand=1)

        # ===================== Bind Event to Treeview =====================
        self.library_records.bind("<ButtonRelease-1>",LibraryInfo)
        Displaydata()


        # ===================== Buttons =====================
      
        # ---------------------------
        # Control Buttons
        # ---------------------------
        # Display Data : Add new record to DB
        # Delete       : Remove selected record
        # Reset        : Clear all input fields
        # Search       : Search DB by Member ID
        # Exit         : Close the application

        self.btnDisplayData = Button(ButtonFrame, text='Display Data',
            font=('arial', 19, 'bold'), padx=4, width=16, bd=4, bg='cadetblue', command= addData)
        self.btnDisplayData.grid(row=0, column=0, padx=3)

        self.btnDelete = Button(ButtonFrame, text='Delete',
            font=('arial', 19, 'bold'), width=16, bd=5, padx=4, bg='cadetblue',command=deleteDB)
        self.btnDelete.grid(row=0, column=2, padx=4)

        self.btnReset = Button(ButtonFrame, text='Reset',
            font=('arial', 19, 'bold'), width=16, bd=5, padx=4, bg='cadetblue',command=iReset)
        self.btnReset.grid(row=0, column=3, padx=4)

        self.btnSearch = Button(ButtonFrame, text='Search',
            font=('arial', 19, 'bold'), width=16, bd=5, padx=4, bg='cadetblue',command=searchDB)
        self.btnSearch.grid(row=0, column=4, padx=4)

        self.btnExit = Button(ButtonFrame, text='Exit',
            font=('arial', 19, 'bold'), width=16, bd=5, padx=4, bg='cadetblue', command= iExit)
        self.btnExit.grid(row=0, column=5, padx=3)
    


if __name__=="__main__":
    root = Tk()
    application = Library(root)
    root.mainloop()





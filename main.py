import logging
import os

logging.basicConfig(filename="transactionsLog.log", filemode='a', format="%(asctime)s - %(message)s",
                    level=logging.DEBUG)

from datetime import datetime, timedelta
from random import randint
from tkinter import *
from tkinter import messagebox, Label, Entry, StringVar, ttk
from tkinter import Tk, Label, Button
from tkinter import PhotoImage
import csv
import re
import hashlib
import tkinter
import sqlite3

conn = sqlite3.connect('KSUGolfCart1.db')
c = conn.cursor()

# Adding admin info
userID = 123456
Fname = "Admain"
Lname = "User"
Password = "1234567890"
PhoneNumber = '0555555555'
Email = 'admin12345@ksu.edu.sa'
user = "Admin"
sql = """INSERT INTO userInfo VALUES('{}','{}','{}','{}','{}','{}','{}')
                """.format(userID, Fname, Lname, Password, PhoneNumber, Email, user)
#c.execute(sql)
conn.commit()


# Create the Tabels
conn = sqlite3.connect('KSUGolfCart1.db')
c = conn.cursor()
c.execute(''' Create table IF NOT EXISTS userInfo(
userID      Char(10) Primary Key    ,
FName     CHAR (30)    ,
LName     CHAR (30)    ,
Password        CHAR (30)  ,
Email         CHAR (30)    ,
PhoneNumber  CHAR(15),
userType
 ); ''')

c.execute(''' Create table IF NOT EXISTS admainInfo(
CartID      Char(10) Primary Key    ,
collage     CHAR (30)   

 ); ''')

c.execute(''' Create table IF NOT EXISTS reservation(
reservID Char(5) Primary Key,
userId      CHAR(10),
cartID      CHAR(10) ,
startTime DATETIME,
endTime DATETIME,
FOREIGN KEY(userID) REFERENCES userInfo(userID) ,
FOREIGN KEY(cartID) REFERENCES admainInfo(CartID)
 ); ''')

conn.close()


class GUI:
    file_path = "counter.txt"

    def __init__(self):
        self.main_window = Tk()
        self.main_window.configure(bg='light blue')
        self.main_window.title("Welcome To Golf Cart!")

        # university logo
        self.university_logo = PhotoImage(file="logoksu2.png")
        self.resized=self.university_logo.subsample(10,10)
        self.logo_label = Label(self.main_window, image=self.resized, bg='light blue')
        self.logo_label.pack(side='top', anchor="ne", padx=10,pady = 5)

        self.label1 = Label(self.main_window, text="To start Click The Button:", font=('Times New Roman',12),bg='light blue')
        self.signup_choose = Button(self.main_window, text="Sign Up", command=self.sign_up)

        self.label1.pack()
        self.signup_choose.pack()
        self.signup_choose.pack(side='bottom')
        self.reservation_id_counter = self.load_counter()
        self.displayed_reserve_ids = set()

        tkinter.mainloop()


    def load_counter(self):
        # Load the counter value from the file, or start from 0 if the file doesn't exist
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return int(file.read().strip())
        else:
            return 0

    def sign_up(self):
        self.main_window.destroy()
        self.sign_up_window = tkinter.Tk()

        #logo
        self.university_logo = PhotoImage(file="logoksu2.png")
        self.resized = self.university_logo.subsample(10, 10)
        self.logo_label = Label(self.sign_up_window, image=self.resized, bg='light blue')
        self.logo_label.grid(row=0,column=2,sticky='NE', padx=10, pady=5)

        self.sign_up_window.configure(bg='light blue')
        self.sign_up_window.title("sign up!")

        Label(self.sign_up_window, text="First name:",bg='light blue').grid(row=5, column=0, padx=10, pady=5)
        self.Fname_var = StringVar()
        self.Fname_entry = Entry(self.sign_up_window, textvariable=self.Fname_var)
        self.Fname_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(self.sign_up_window, text="Last name:",bg='light blue').grid(row=6, column=0, padx=10, pady=5)
        self.Lname_var = StringVar()
        self.Lname_entry = Entry(self.sign_up_window, textvariable=self.Lname_var)
        self.Lname_entry.grid(row=6, column=1, padx=10, pady=5)


        Label(self.sign_up_window, text="The ID :",bg='light blue').grid(row=3, column=0, padx=10, pady=5)
        self.userID_var = StringVar()
        self.userID_entry = Entry(self.sign_up_window, textvariable=self.userID_var)
        self.userID_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(self.sign_up_window, text="Password:",bg='light blue').grid(row=4, column=0, padx=10, pady=5)
        self.Pass_var = StringVar()
        self.Pass_entry = Entry(self.sign_up_window, show="*", textvariable=self.Pass_var)
        self.Pass_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(self.sign_up_window, text="Email Address:",bg='light blue').grid(row=7, column=0, padx=10, pady=5)
        self.email_var = StringVar()
        self.email_entry = Entry(self.sign_up_window, textvariable=self.email_var)
        self.email_entry.grid(row=7, column=1, padx=10, pady=5)


        Label(self.sign_up_window, text="Phone number:",bg='light blue').grid(row=8, column=0, padx=10, pady=5)
        self.number_var = StringVar()
        self.number_entry = Entry(self.sign_up_window, textvariable=self.number_var)
        self.number_entry.grid(row=8, column=1, padx=10, pady=5)

        self.uservar = tkinter.StringVar()
        # Combo box for user class
        tkinter.Label(self.sign_up_window, text="User class:",bg='light blue').grid(row=1, column=0, padx=10, pady=5)
        user_class_options = ["Student", "Faculty", "Employee"]
        self.user_class_combobox = ttk.Combobox(self.sign_up_window, textvariable=self.uservar,values=user_class_options)
        self.user_class_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.B1 = tkinter.Button(self.sign_up_window, text="Login", command=self.login)
        self.B1.grid(row=9, column=0, padx=10, pady=5)
        self.B2 = tkinter.Button(self.sign_up_window, text="Submit", command=self.CheckSignUP)
        self.B2.grid(row=9, column=1, padx=10, pady=5)


        self.sign_up_window.mainloop()


    def CheckSignUP(self):

        try:
            conn = sqlite3.connect("KSUGolfCart1.db")
            c = conn.cursor()

            # check phone
            phone = self.number_entry.get()
            if not phone:
                messagebox.showinfo("Error", "You must enter your Phonenumber")
                return

            reg2 = "^(05)[0-9]{8}$"
            y = re.search(re.compile(reg2), phone)
            if not y:
                messagebox.showinfo("Invalid Phone Number", "Phone Number must Start with: \'05\' and 9 digit")
                return

            # check email
            email = self.email_entry.get()
            reg = "^([a-zA-Z0-9\._-]+){8}(@ksu\.edu\.sa)$"
            x = re.search(re.compile(reg), email)
            if not x:
                messagebox.showinfo("invalid Email", "Email should be  xxxxxxxx@ksu.edu.sa ")
                return

            # Check FName & Lname:
            Fname = self.Fname_entry.get()
            Lname = self.Lname_entry.get()

            if not Fname or not Lname:
                messagebox.showinfo("Error", "You must enter First and Last Name")
                return

            # Check ID:
            id = self.userID_entry.get()

            reg = "[0-9]"
            pat = re.compile(reg)
            x = re.search(pat, id)
            userType = self.user_class_combobox.get()

            if not x:
                messagebox.showerror("Error", "ID must be digit ")
                return

            elif userType == 'Student':
                if len(id) != 10:
                    messagebox.showerror("Error", "ID must be 10 digits")
                    return

            elif userType == 'Faculty' or userType == "Employee":
                if len(id) != 6:
                    messagebox.showerror("Error", " ID must be 6 digits")
                    return

            # Check Password:
            Pass = self.Pass_entry.get()
            reg = "^[A-Za-z0-9]{6,100}$"
            pat = re.compile(reg)
            x = re.search(pat, Pass)

            if not x:
                messagebox.showinfo("Error", "Password must be at least 6 characters")
                return

            else:
                check = c.execute(f"SELECT userID FROM userInfo WHERE userID = {id}")
                if len(check.fetchall()) == 0:
                    hashPass = hashlib.sha256(Pass.encode()).hexdigest()
                    sql = """INSERT INTO userInfo VALUES('{}','{}','{}','{}','{}','{}','{}' )
                                    """.format(id, Fname, Lname, hashPass, email, phone, userType)
                    c.execute(sql)

                    conn.commit()
                    messagebox.showinfo("Registration Done", "Congratulation You information has been saved")


                else:
                    messagebox.showinfo("ID already exist", "The enterd id is exist please try with another ID")

                conn.close()
        except sqlite3.Error:
            messagebox.showinfo("Error!", "Try Again Please")

    def login(self):
        self.sign_up_window.destroy()
        self.login_window = tkinter.Tk()
        self.login_window.configure(bg='light blue')
        self.login_window.title("Login")

        #  university logo
        self.university_logo = PhotoImage(file="logoksu2.png")
        self.resized = self.university_logo.subsample(10, 10)
        self.logo_label = Label(self.login_window, image=self.resized, bg='light blue')
        self.logo_label.grid(row=0, column=4, sticky='NE', padx=10, pady=5)

        login_button = Button(self.login_window, text="Login", command=self.perform_login)
        login_button.grid(row=3, column=3)

        Label(self.login_window, text="ID:",bg='light blue').grid(row=1, column=2, padx=10, pady=5)
        self.login_id_var = StringVar()
        self.login_id_entry = Entry(self.login_window, textvariable=self.login_id_var)
        self.login_id_entry.grid(row=1, column=3, padx=10, pady=5)

        Label(self.login_window, text="Password:",bg='light blue').grid(row=2, column=2, padx=10, pady=5)
        self.login_password_var = StringVar()
        self.login_password_entry = Entry(self.login_window, show="*", textvariable=self.login_password_var)
        self.login_password_entry.grid(row=2, column=3, padx=10, pady=5)

    def resign_up(self):
        self.sign_up_window = tkinter.Tk()

        # logo
        self.university_logo = PhotoImage(file="logoksu2.png")
        self.resized = self.university_logo.subsample(10, 10)
        self.logo_label = Label(self.sign_up_window, image=self.resized, bg='light blue')
        self.logo_label.grid(row=0, column=2, sticky='NE', padx=10, pady=5)

        self.sign_up_window.configure(bg='light blue')
        self.sign_up_window.title("sign up!")

        Label(self.sign_up_window, text="First name:", bg='light blue').grid(row=5, column=0, padx=10, pady=5)
        self.Fname_var = StringVar()
        self.Fname_entry = Entry(self.sign_up_window, textvariable=self.Fname_var)
        self.Fname_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(self.sign_up_window, text="Last name:", bg='light blue').grid(row=6, column=0, padx=10, pady=5)
        self.Lname_var = StringVar()
        self.Lname_entry = Entry(self.sign_up_window, textvariable=self.Lname_var)
        self.Lname_entry.grid(row=6, column=1, padx=10, pady=5)

        Label(self.sign_up_window, text="The ID :", bg='light blue').grid(row=3, column=0, padx=10, pady=5)
        self.userID_var = StringVar()
        self.userID_entry = Entry(self.sign_up_window, textvariable=self.userID_var)
        self.userID_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(self.sign_up_window, text="Password:", bg='light blue').grid(row=4, column=0, padx=10, pady=5)
        self.Pass_var = StringVar()
        self.Pass_entry = Entry(self.sign_up_window, show="*", textvariable=self.Pass_var)
        self.Pass_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(self.sign_up_window, text="Email Address:", bg='light blue').grid(row=7, column=0, padx=10, pady=5)
        self.email_var = StringVar()
        self.email_entry = Entry(self.sign_up_window, textvariable=self.email_var)
        self.email_entry.grid(row=7, column=1, padx=10, pady=5)

        Label(self.sign_up_window, text="Phone number:", bg='light blue').grid(row=8, column=0, padx=10, pady=5)
        self.number_var = StringVar()
        self.number_entry = Entry(self.sign_up_window, textvariable=self.number_var)
        self.number_entry.grid(row=8, column=1, padx=10, pady=5)

        self.uservar = tkinter.StringVar()

        # Combo box for user class
        tkinter.Label(self.sign_up_window, text="User class:", bg='light blue').grid(row=1, column=0, padx=10, pady=5)
        user_class_options = ["Student", "Faculty", "Employee"]
        self.user_class_combobox = ttk.Combobox(self.sign_up_window, textvariable=self.uservar,
                                                values=user_class_options)
        self.user_class_combobox.grid(row=1, column=1, padx=10, pady=5)

        self.B1 = tkinter.Button(self.sign_up_window, text="Login", command=self.login)
        self.B1.grid(row=9, column=0, padx=10, pady=5)
        self.B2 = tkinter.Button(self.sign_up_window, text="Submit", command=self.CheckSignUP)
        self.B2.grid(row=9, column=1, padx=10, pady=5)

        self.sign_up_window.mainloop()
    def perform_login(self):

        try:
            conn = sqlite3.connect("KSUGolfCart1.db")
            c = conn.cursor()

            # retrive the password and id
            Pass = self.login_password_entry.get()
            iduser = self.login_id_entry.get()

            # Hash the Password:
            hashPass = hashlib.sha256(Pass.encode()).hexdigest()

            # 1- User did not enter ID or Password:
            if not Pass or not iduser:
                messagebox.showinfo("Error", "You must enter ID and Password! ")
                return

            # 2-User didn't enter numbers:
            reg = "^[0-9]+$"
            x = re.search(re.compile(reg), iduser)
            if not x:
                messagebox.showerror("Error", "ID must be digit ")
                return

            # 3-User entered less than 6 digits for the password:
            if len(Pass) < 6:
                messagebox.showerror("Error", "Password must be at least 6 digits")
                return

            # 4-User entered an incorrect number of digits for ID:
            if len(iduser) not in (10, 6):
                messagebox.showerror("Error", "ID must be 10 digits for students and 6 for faculty or employee")
                return

            # 5- check ID availability
            checkID = c.execute(f"SELECT userID FROM userInfo WHERE userID='{iduser}'").fetchone()
            if not checkID:
                messagebox.showerror("Error", "ID not found!")
                return

            # 6-IF it is the admin:
            adminPass = '1234567890'
            hashPassAdmin = hashlib.sha256(adminPass.encode()).hexdigest()

            if hashPass == hashPassAdmin and iduser == '123456':
                self.Admin_window()
                return

            # 7-check password validity
            checkPass = c.execute(f"SELECT Password FROM userInfo WHERE userID='{iduser}'").fetchone()
            if checkPass[0] != hashPass:
                messagebox.showerror("Error", "Wrong Password")
            else:
                self.userViwe(iduser)
        except sqlite3.Error:
            messagebox.showinfo("Error!", "Try Again Please")
        finally:
            conn.close()

    def Admin_window(self):
        self.login_window.destroy()
        self.admin_window = tkinter.Tk()
        self.admin_window.title("Admin")
        self.university_logo = PhotoImage(file="logoksu2.png")
        self.resized = self.university_logo.subsample(10, 10)
        self.logo_label = Label(self.admin_window, image=self.resized, bg='light blue')
        self.logo_label.pack(side='top', anchor="ne", padx=10,pady = 5)
        self.admin_window.configure(bg='light blue')

        # Enter Golf Cart Number:
        self.Label1 = StringVar()
        Label(self.admin_window, text="Enter the Golf Cart plate Number: ",bg='light blue').pack()
        self.GolfEntry = Entry(self.admin_window, textvariable=self.Label1)
        self.GolfEntry.pack()

        # Enter College:
        self.Label2 = StringVar()
        Label(self.admin_window, text="Enter the College: ",bg='light blue').pack()
        self.CollegeEntry = Entry(self.admin_window, textvariable=self.Label2)
        self.CollegeEntry.pack()

        # Create Button:
        tkinter.Button(self.admin_window, text="Create", command=self.Confirm).pack(pady=3)

        # Backup Button:
        tkinter.Button(self.admin_window, text="Backup", command=self.Backup).pack(pady=3)

        # LogOut Button:
        tkinter.Button(self.admin_window, text="LogOut", command=self.Logout).pack(pady=3)

        tkinter.mainloop()

    def Confirm(self):
        try:
            conn = sqlite3.connect('KSUGolfCart1.db')
            c = conn.cursor()
            GolfNumber = self.GolfEntry.get()
            if not GolfNumber:
                messagebox.showinfo("Missing input", "Enter Golf Cart Number")
                return
            College = self.CollegeEntry.get()
            if not College:
                messagebox.showinfo("Missing input", "Enter College!")
                return

            # Check if CartID already exists
            cart_id_exists = c.execute(f"SELECT CartID FROM admainInfo WHERE CartID='{GolfNumber}'").fetchone()
            if not cart_id_exists:
                sql = """INSERT INTO admainInfo VALUES('{}','{}') """.format(GolfNumber, College)
                c.execute(sql)
                conn.commit()

                messagebox.showinfo(title=" Added ", message="Information Added Succfuly")

            else:
                messagebox.showinfo("Error","Golf Cart ID already exists")
                return

            conn.close()
        except sqlite3.Error:
            messagebox.showinfo("Error!", "Try Again Please")

    def Logout(self):
        self.admin_window.destroy()
        self.resign_up()


    def Backup(self):
            try:
                conn = sqlite3.connect('KSUGolfCart1.db')
                c = conn.cursor()
                file = open("KSUGolfCart.csv", 'a+', newline='')
                w = csv.writer(file)

                # Write all user info in CSV file:
                w.writerow("User Information:")
                sql_userInfo = ('''select * from userInfo''')
                result = c.execute(sql_userInfo)
                for row in result:
                    w.writerow(row)

                # Write all Reservation info in CSV file:
                w.writerow("Reservation Information:")
                sql_reservation = ('''select * from reservation''')
                result1= c.execute(sql_reservation)
                for row in result1:
                    w.writerow(row)

                # Write all Reservation info in CSV file:
                w.writerow("Admin Information:")
                sql_admin = ('''select * from admainInfo''')
                result2=c.execute(sql_admin)
                for row in result2:
                    w.writerow(row)
                file.close()
                messagebox.showinfo("Backup", "Backup Successfuly")
            except Exception as e:
                messagebox.showinfo("Error!", f"Error during backup: {e}")

    def userViwe(self, id):
        self.login_window.destroy()
        self.userview = tkinter.Tk()
        self.userview.configure(bg='light blue')
        self.userview.geometry('700x400')
        self.userview.title("Reservations")

        #logo
        self.university_logo = PhotoImage(file="logoksu2.png")
        self.resized = self.university_logo.subsample(10, 10)
        self.logo_label = Label(self.userview, image=self.resized, bg='light blue')
        self.logo_label.pack(side='top', anchor="ne", padx=10, pady=5)


        # get the id
        self.ID = id

        # create a notebook
        self.tabControl = ttk.Notebook(self.userview)
        self.tabControl.pack(pady=10, expand=True)

        # create frames
        self.reserve_tap = ttk.Frame(self.tabControl, width=500, height=200)
        self.reserve_tap.pack()
        self.view_tap = ttk.Frame(self.tabControl, width=500, height=800)
        self.view_tap.pack()

        # add frames to notebook
        self.tabControl.add(self.reserve_tap, text="Reserve a Cart")
        self.tabControl.add(self.view_tap, text="View my Reservation ")

        # ------------------------------"Reserve a Cart" ------------------------------------------

        # treeview for list of all golf cart numbers and location
        conn = sqlite3.connect('KSUGolfCart1.db')
        self.TreePlate = ttk.Treeview(self.reserve_tap, columns=(1, 2), show='headings', height=6)
        self.TreePlate.heading(1, text="Cart ID")
        self.TreePlate.column(1, minwidth=20, width=60, anchor=CENTER, stretch=NO)
        self.TreePlate.heading(2, text="Collage")
        self.TreePlate.column(2, minwidth=20, width=140, anchor=CENTER, stretch=NO)

        cursor = conn.execute("SELECT * FROM admainInfo")
        count = 0
        for row in cursor:
            self.TreePlate.insert(parent="", index=count, text="", values=(row[0], row[1]))
            count += 1
        self.TreePlate.grid(row=0, column=1, pady=10)

        # labels for entry the dates
        self.start_time = tkinter.Label(self.reserve_tap, text="Start Time %Y-%m-%d %H:%M")
        self.start_time.grid(row=1, column=0, pady=10)
        self.start_entry = tkinter.Entry(self.reserve_tap)
        self.start_entry.grid(row=1, column=1, pady=10)

        self.end_time = tkinter.Label(self.reserve_tap, text="End Time %Y-%m-%d %H:%M")
        self.end_time.grid(row=2, column=0, pady=10)
        self.end_entry = tkinter.Entry(self.reserve_tap)
        self.end_entry.grid(row=2, column=1, pady=10)

        #buttons reserve/logout
        button_frame1 = tkinter.Frame(self.reserve_tap)
        button_frame1.grid(row=3, column=1)
        self.reserve_button = tkinter.Button(button_frame1, text="Reserve", command=self.reserved)
        self.reserve_button.grid(row=3, column=1,pady=10)
        self.logout_button = tkinter.Button(button_frame1, text="Logout", command=self.logout)
        self.logout_button.grid(row=3, column=2,pady=10)

        # --------------------------------View my Reservation ------------------------------------------------
        activeLabel = tkinter.Label(self.view_tap, text='The Active Reservations:', font=('Times New Roman', 12))
        activeLabel.grid(row=0,column=0)
        self.TreePlate1 = ttk.Treeview(self.view_tap, columns=(1, 2, 3, 4, 5), show='headings', height=6)
        self.TreePlate1.heading(1, text="reserve ID")
        self.TreePlate1.column(1, minwidth=20, width=60, anchor=CENTER, stretch=NO)
        self.TreePlate1.heading(2, text="User Id")
        self.TreePlate1.column(2, minwidth=20, width=80, anchor=CENTER, stretch=NO)
        self.TreePlate1.heading(3, text="Cart Id")
        self.TreePlate1.column(3, minwidth=20, width=60, anchor=CENTER, stretch=NO)
        self.TreePlate1.heading(4, text="Start Time")
        self.TreePlate1.column(4, minwidth=20, width=120, anchor=CENTER, stretch=NO)
        self.TreePlate1.heading(5, text="End Time")
        self.TreePlate1.column(5, minwidth=20, width=120, anchor=CENTER, stretch=NO)

        #show active:
        current_time = datetime.now()
        sqlt = conn.execute("SELECT * FROM reservation INNER JOIN userInfo ON reservation.userID = userInfo.userID WHERE reservation.userID = ? AND ? < startTime",
            (self.ID , current_time,))

        count = 0
        for row in sqlt:
            reservID=row[0]
            if reservID not in self.displayed_reserve_ids:
                self.TreePlate1.insert(parent="", index=count, text="", values=(row[0], row[1], row[2], row[3], row[4]))
                count += 1
        self.TreePlate1.grid(row=1, column=0, pady=5)

        # buttons view/logout
        button_frame = tkinter.Frame(self.view_tap)
        self.show_button = tkinter.Button(button_frame, text="View", command=self.Show)
        self.logout_button = tkinter.Button(button_frame, text="Logout", command=self.logout)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        self.show_button.grid(row=2, column=0, sticky='ew')
        self.logout_button.grid(row=2, column=1, sticky='ew')
        button_frame.grid(row=2, column=0, sticky="ew")

        self.tabControl.pack()
        self.userview.mainloop()


    def reserved(self):
        try:
            conn = sqlite3.connect('KSUGolfCart1.db')
            c = conn.cursor()

            # Take the Selection
            selection = self.TreePlate.selection()
            if not selection:
                messagebox.showerror("Error", "Please select From The Table")
                return

            selectedItem = self.TreePlate.selection()[0]
            cID = str(self.TreePlate.item(selectedItem)['values'][0])

            # get the user Entry
            startTime = str(self.start_entry.get())
            endTime = str(self.end_entry.get())
            if not startTime or not endTime:
                messagebox.showerror("Error", "Please Enter the Time")
                return

            else:
                # The Location
                c.execute(f"""SELECT collage From admainInfo WHERE CartID = {cID}""")
                locResult = c.fetchone()
                location = locResult[0]
                conn.commit()

                # the date&time
                st = datetime.strptime(startTime, "%Y-%m-%d %H:%M")
                et = datetime.strptime(endTime, "%Y-%m-%d %H:%M")
                checkUser = c.execute(f"""SELECT userType FROM userInfo WHERE userID = {self.ID} """)
                result = checkUser.fetchone()

                if et < st:
                    logging.error(
                        f"""ID is: ,{self.ID} ,Cart Number is:{cID}, The Start and End Time: {st},{et}, The Location: {location},
                                                                                              The EndTime must be After the StartTime""")
                    messagebox.showerror("Error",
                                         "The start time must be earlier than end time ")
                    return

                if result:
                    user_type = result[0]

                    # Check the reservation period
                    if user_type == 'Student':
                        if et - st > timedelta(minutes=30):
                            logging.error(
                                f"""ID is: ,{self.ID} ,Cart Number is:{cID}, The Start and End Time: {st},{et}, The Location: {location},
                                                                          The reservation period should not exceed 30 min for Student""")
                            messagebox.showerror("Error",
                                                 "The reservation period should not exceed 30 mins for students")
                            return

                    elif user_type == 'Employee':
                        if et - st > timedelta(hours=1):
                            logging.error(
                                f"""ID is: ,{self.ID} ,Cart Number is:{cID}, The Start and End Time: {st},{et}, The Location: {location},
                                                         The reservation period should not exceed 1 hour for Employee""")
                            messagebox.showerror("Error",
                                                 "The reservation period should not exceed 1 hour for Employee")
                            return

                    elif user_type == 'Faculty':
                        if et - st > timedelta(hours=1, minutes=30):
                            logging.error(
                                f"""ID is: ,{self.ID} ,Cart Number is:{cID}, The Start and End Time: {st},{et}, The Location: {location},
                                         The reservation period should not exceed 1:30 hour for Faculty""")
                            messagebox.showerror("Error",
                                                 "The reservation period should not exceed 1:30 hour for Faculty")
                            return

            # check the availability of the selected golf cart
            sql1 = """SELECT startTime ,endTime FROM reservation WHERE cartID =('{}') """.format(
                cID)
            c.execute(sql1)
            conn.commit()
            result = c.fetchall()

            for row in result:
                timeTuple = row
                existing_start_time = datetime.strptime(str(timeTuple[0]), "%Y-%m-%d %H:%M:%S")
                existing_end_time = datetime.strptime(str(timeTuple[1]), "%Y-%m-%d %H:%M:%S")

                if existing_start_time < et and existing_end_time > st:
                    logging.error(
                        f'ID is: {self.ID}, Cart Number is: {cID}, The Start and End Time: {st}, {et}, The Location: {location}, The cart is not available')
                    messagebox.showerror("ERROR", "The cart is not available")
                    return

            # insert the reservation
            reservID = self.generate_reservation_id()
            # save the counter
            with open(self.file_path, 'w') as file:
                file.write(str(self.reservation_id_counter))

            sql = """INSERT INTO reservation VALUES('{}','{}','{}','{}','{}')
                   """.format(reservID, self.ID, cID, st, et)
            c.execute(sql)
            conn.commit()
            logging.info(f'{self.ID} ,{cID},{st},{et},{location}, Reserved Successfully')
            messagebox.showinfo("Success", "Reserved Successfully")




            #active rev
            current_time = datetime.now()
            sqlt = conn.execute("SELECT * FROM reservation WHERE ? < startTime AND reservID = ?", (current_time , reservID))

            count = 0
            for row in sqlt:
                self.TreePlate1.insert(parent="", index=count, text="", values=(row[0], row[1], row[2], row[3], row[4]))
                count += 1

            conn.commit()
            conn.close()

        except ValueError:
            messagebox.showerror("Error", " Please Enter the Date and the Time as %Y-%m-%d %H:%M")
            return

        except sqlite3.Error:
            messagebox.showinfo("Error!", "Try Again Please")
            return

    def generate_reservation_id(self):

        # Increment the counter and return the new reservation ID
        self.reservation_id_counter += 1
        return str(self.reservation_id_counter)

    def Show(self):

        allLabel= tkinter.Label(self.view_tap,text='All the Reservations:',font=('Times New Roman',12))
        allLabel.grid(row=3,column=0)
        self.TreePlateAll = ttk.Treeview(self.view_tap, columns=(1, 2, 3, 4, 5), show='headings', height=6)
        self.TreePlateAll.heading(1, text="reserve ID")
        self.TreePlateAll.column(1, minwidth=20, width=60, anchor=CENTER, stretch=NO)
        self.TreePlateAll.heading(2, text="User Id")
        self.TreePlateAll.column(2, minwidth=20, width=80, anchor=CENTER, stretch=NO)
        self.TreePlateAll.heading(3, text="Cart Id")
        self.TreePlateAll.column(3, minwidth=20, width=60, anchor=CENTER, stretch=NO)
        self.TreePlateAll.heading(4, text="Start Time")
        self.TreePlateAll.column(4, minwidth=20, width=120, anchor=CENTER, stretch=NO)
        self.TreePlateAll.heading(5, text="End Time")
        self.TreePlateAll.column(5, minwidth=20, width=120, anchor=CENTER, stretch=NO)
        self.TreePlateAll.grid(row=4,column=0)

        conn = sqlite3.connect('KSUGolfCart1.db')
        c = conn.cursor()
        # Fetch all reservations for the current user
        all_reservations = c.execute(
            "SELECT * FROM reservation INNER JOIN userInfo ON reservation.userID = userInfo.userID WHERE reservation.userID = ?",
            (self.ID,)
        ).fetchall()

        # Display all reservations treeAll
        count = 0
        for row in all_reservations:
            self.TreePlateAll.insert(parent='', index=count, text='', values=(row[0], row[1], row[2], row[3], row[4]))
            count += 1

        conn.commit()
        conn.close()

    def logout(self):
        self.userview.destroy()
        self.resign_up()

# Instantiate the GUI class
gui = GUI()
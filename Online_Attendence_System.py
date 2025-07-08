from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox
import mysql.connector
from datetime import datetime
from datetime import date
from tkcalendar import DateEntry
import csv
from tkinter import filedialog

root = Tk()
root.title("Python Online Attendance System")

width = 1000
height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(False, False)

USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()
current_user=None

STUDENT = StringVar()
ROLL = StringVar()
var = IntVar()

def Database():
    global mydb, cursor
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="Online"
    )
    cursor = mydb.cursor()
    cursor.execute("create table if not exists member (mem_id int primary key auto_increment, username varchar(20),password varchar(20), firstname varchar(20), lastname varchar(20))")

    cursor.execute("create table if not exists students (stud_no int primary key auto_increment ,student varchar(20), roll varchar(20), var int,mem_id int, date date, foreign key (mem_id) REFERENCES member(mem_id))")

def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def Save():
    Database()
    cur = mydb.cursor()
    cur.execute("SELECT student, roll, var, date FROM students where mem_id=(Select mem_id from member Where username = %s)",(current_user,))
    rows = cur.fetchall()
    if not rows:
        tkMessageBox.showinfo("No Data","No attendance data found to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Student Name","Roll No.","Status","Date"])
            for row in rows:
                status = "Present" if row[2] == 1 else "Absent"
                try:
                    formatted_date = row[3].strftime("%Y-%m-%d")
                except ValueError:
                    formatted_date = row[3]
                writer.writerow([row[0], row[1], status, row[3]])
        tkMessageBox.showinfo("Success",f"Attendance data saved successfully to{file_path}.")
    cur.close()
    mydb.close()
def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)
    title = Label(LoginFrame, text="LOGIN FORM", fg="red", font=('arial',25), bd=18)
    title.grid(row=0)
    lbl_username = Label(LoginFrame, text="UserName:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="PassWord:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial',20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=5, columnspan=2, pady=20)

    lbl_register = Label(LoginFrame, text="CREATE ACCOUNT", fg="Blue", font=('arial', 18))
    lbl_register.grid(row=4, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)

def RegisterForm():
    global RegisterFrame,lbl_result2
    RegisterFrame = Frame(root)
    RegisterFrame.pack(side=TOP, pady=40)
    title = Label(RegisterFrame, text="REGISTRATION FORM", fg="red", font=('arial', 25), bd=18)
    title.grid(row=0)
    lbl_username = Label(RegisterFrame, text="UserName:", font=('arial', 18), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18)
    lbl_password.grid(row=2)
    lbl_firstname = Label(RegisterFrame, text="FirstName:", font=('arial', 18), bd=18)
    lbl_firstname.grid(row=3)
    lbl_lastname = Label(RegisterFrame, text="LastName:", font=('arial', 18), bd=18)
    lbl_lastname.grid(row=4)
    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)
    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=3, column=1)
    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=LASTNAME, width=15)
    lastname.grid(row=4, column=1)
    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=35, command=Register)
    btn_login.grid(row=6, columnspan=2, pady=20)

    lbl_login = Label(RegisterFrame, text="GO TO LOGIN FORM", fg="Blue", font=('arial', 15))
    lbl_login.grid(row=7, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

def attendanceForm():
    global attendanceFrame, lbl_result3, date_entry
    attendanceFrame = Frame(root)
    attendanceFrame.pack(side=TOP, pady=20)
    title2= Label(attendanceFrame, text="Online Attendance", fg="red", font=('arial', 18), bd=10)
    title2.grid(row=0)
    lbl_student = Label(attendanceFrame, text="StudentName:", font=('arial', 18), bd=10)
    lbl_student.grid(row=1)
    lbl_roll = Label(attendanceFrame, text="Roll no.:", font=('arial', 18), bd=10)
    lbl_roll.grid(row=2)

    lbl_result3 = Label(attendanceFrame, text="", font=('arial', 10))
    lbl_result3.grid(row=6, column=1)
    student = Entry(attendanceFrame, font=('arial', 18), textvariable=STUDENT, width=15)
    student.grid(row=1, column=1)
    roll = Entry(attendanceFrame, font=('arial', 18), textvariable=ROLL, width=15)
    roll.grid(row=2, column=1)

    present = Radiobutton(attendanceFrame, text="Present", padx=1, variable=var, value=1)
    present.grid(row=4, column=1)
    absent = Radiobutton(attendanceFrame, text="Absent", padx=5, variable=var, value=0)
    absent.grid(row=4, column=0)

    btn_submit = Button(attendanceFrame, text="SUBMIT", font=('arial', 10), width=35, command=Submit)
    btn_submit.grid(row=5, columnspan=2, pady=20)

    b2 = tk.Button(attendanceFrame, text="View All Data", font=('arial',10), width=35, command=View)
    b2.grid(row=7, columnspan=2, pady=20)

    b3 = Button(attendanceFrame, text="View Data by Date", font=('arial', 10), width=35, command=ViewDate)
    b3.grid(row=8, columnspan=2, pady=20)


def View():
    all_data_win = Toplevel(root)
    all_data_win.title("View All Attendance Data")
    all_data_win.geometry("1000x600")
    search = Label(all_data_win, text='Search student:')
    search.pack(pady=10)
    search_entry = Entry(all_data_win)
    search_entry.pack(pady=10)
    columns = ('student', 'roll', 'presents', 'absents', 'total')
    tree = ttk.Treeview(all_data_win, columns=columns, show='headings')
    tree.heading('student', text='Student Name')
    tree.heading('roll', text='Roll No.')
    tree.heading('presents', text='Presents')
    tree.heading('absents', text='Absents')
    tree.heading('total', text='Total No. of Attendance')
    tree.pack(fill=BOTH, expand=True)
    size = ttk.Sizegrip(all_data_win)
    size.pack(side=tk.RIGHT, anchor=tk.SE)

    Database()
    cur = mydb.cursor()
    cur.execute("SELECT mem_id FROM member where username = %s",(current_user,))
    mem_id = cursor.fetchone()[0]
    cursor.execute("SELECT student, roll, SUM(var = 1) as presents, SUM(var = 0) as absents, COUNt(*) as total from students where mem_id = %s group by student, roll", (mem_id,))
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))
    def search_stu():
        for item in tree.get_children():
            tree.delete(item)
        search_term = search_entry.get()
        Database()
        cur = mydb.cursor()
        query = "SELECT  student, roll, SUM(var = 1) as presents, SUM(var = 0) as absents, COUNT(*) as total FROM students WHERE student LIKE %s and mem_id = %s group by student, roll"
        try:
            cur.execute(query, (f"%{search_term}%",mem_id,))
            rows = cur.fetchall()
            for r in rows:
                tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4]))
        except mysql.connector.Error as err:
            print(f"Error:{err}")
        finally:
            cur.close()
            mydb.close()
    search_btn = Button(all_data_win, text="Search", command=search_stu)
    search_btn.pack(pady=10)
    close = Button(all_data_win, text="Close", command=all_data_win.destroy)
    close.pack(pady=10)

def ViewDate():
    date_data_win = Toplevel(root)
    date_data_win.title("View Attendance by Date ")
    date_data_win.geometry("1000x600")
    lbl_date = Label(date_data_win, text="Select Date:", font=('arial', 15))
    lbl_date.pack(pady=10)
    date_entry = DateEntry(date_data_win, width=10, font=('arial', 15), date_pattern='y-mm-dd')
    date_entry.pack(pady=5)
    search = Label(date_data_win, text='Search student:', font=('arial', 15))
    search.pack(pady=10)
    search_entry = Entry(date_data_win)
    search_entry.pack(pady=5)
    columns = ('student', 'roll', 'status', 'total')
    tree = ttk.Treeview(date_data_win, columns=columns, show='headings')
    tree.heading('student', text='Student Name')
    tree.heading('roll', text='Roll No.')
    tree.heading('status', text='Status')
    tree.heading('total', text='Total No. of Attendance')
    tree.pack(fill=BOTH, expand=True)
    size = ttk.Sizegrip(date_data_win)
    size.pack(side=tk.RIGHT, anchor=tk.SE)
    def ViewByDate():
        for item in tree.get_children():
            tree.delete(item)
        selected_date = date_entry.get()
        Database()
        cur = mydb.cursor()
        cur.execute("SELECT mem_id FROM member where username = %s", (current_user,))
        mem_id = cursor.fetchone()[0]
        cursor.execute(
            "SELECT student, roll, var, COUNT(*) as total from students where mem_id = %s and date=%s group by student, roll",
            (mem_id, selected_date,))
        rows = cur.fetchall()
        for row in rows:
            status = 'Present' if row[2] == 1 else 'Absent'
            tree.insert("", tk.END, values=(row[0], row[1], status, row[3]))
    def search_stu_date():
        for item in tree.get_children():
            tree.delete(item)
        search_term = search_entry.get()
        selected_date = date_entry.get()
        Database()
        cur = mydb.cursor()
        cur.execute("SELECT mem_id FROM member where username = %s", (current_user,))
        mem_id = cursor.fetchone()[0]
        query = "SELECT  student, roll, var, COUNT(*) as total from students where student like %s and mem_id = %s and date = %s group by student,roll"
        try:
            cur.execute(query, (f"%{search_term}%",mem_id,selected_date,))
            rows = cur.fetchall()
            for r in rows:
                status = 'Present' if r[2] == 1 else 'Absent'
                tree.insert("", tk.END, values=(r[0], r[1], status, r[3]))
        except mysql.connector.Error as err:
            print(f"Error:{err}")
        finally:
            cur.close()
            mydb.close()
    btn_view = Button(date_data_win, text="View Data", font=('arial',15), command=ViewByDate)
    btn_view.pack(pady=10)
    search_btn = Button(date_data_win, text="Search", font=('arial',15), command=search_stu_date)
    search_btn.pack(pady=10)
    close = Button(date_data_win, text="Close", font=('arial',15), command=date_data_win.destroy)
    close.pack(pady=10)
def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()

def ToggleToSubmit(event=None):
    LoginFrame.destroy()
    attendanceForm()

def Register():
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM member WHERE username = %s", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken try another", fg="red")
        else:
            cursor.execute("INSERT INTO member (username, password, firstname, lastname) VALUES(%s, %s, %s, %s)",
                           (USERNAME.get(), PASSWORD.get(), FIRSTNAME.get(), LASTNAME.get()))
            mydb.commit()
            USERNAME.set("")
            PASSWORD.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()


def Login():
    global current_user
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM member WHERE username = %s and password = %s", (USERNAME.get(), PASSWORD.get()))
        user = cursor.fetchone()

        if user is not None:
            current_user = USERNAME.get()
            ToggleToSubmit()
        else:
            lbl_result1.config(text="Invalid Username or Password", fg="red")
    cursor.close()

def Submit():
    Database()
    current_date = date.today()
    if STUDENT.get == "" or ROLL.get() == "" or var.get() == -1:
        lbl_result3.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT mem_id from member WHERE username = %s", (current_user,))
        mem_id = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM students WHERE student = %s AND mem_id = %s and date = %s", (STUDENT.get(), mem_id, current_date))
        if cursor.fetchone() is not None:
            lbl_result3.config(text="Attendance already recorded for today", fg="red")
        else:
            cursor.execute("INSERT INTO students (student, roll,var,mem_id,date) VALUES(%s,%s,%s,%s,%s)", (STUDENT.get(), ROLL.get(), var.get(), mem_id, current_date))
            mydb.commit()
            STUDENT.set("")
            ROLL.set("")
            var.set(-1)
            lbl_result3.config(text="Attendance Submitted!", fg="green")
            View()
        cursor.close()
        mydb.close()

LoginForm()

menubar = Menu(root)
file = Menu(menubar, tearoff=0)
file.add_command(label="Save", command=Save)
file.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=file)
root.config(menu=menubar)

if __name__ == '__main__':
    root.mainloop()



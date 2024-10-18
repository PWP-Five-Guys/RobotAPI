import sqlite3
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox
import webbrowser
from datetime import datetime

def update_login_log(msg):
    with open("login_record.log", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {msg}\n")

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("863x540+15+30")
        self.root.resizable(False, False)
        self.bg = ImageTk.PhotoImage(file="Login/Nature.jpg")
        self.bg_image = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        self.frame2 = Frame(self.root, bg="#C09E7D")
        self.frame2.place(x=307, y=138, width=280, height=265)
        self.frame = Frame(self.root, bg="#9AAEBE")
        self.frame.place(x=312, y=143, width=270, height=255)
        self.user_txt = Label(self.frame, text="Username", font=("eurostile.TTF", 15, "bold"), fg="black",
                              bg="#9AAEBE").place(x=15, y=15)
        self.user = Entry(self.frame, font=("eurostile.TTF", 15, "bold"), bg="#C4D8E8")
        # Make sure to place separately for proper get() usage
        self.user.place(x=15, y=45)
        self.password_txt = Label(self.frame, text="Password", font=("eurostile.TTF", 15, "bold"), fg="black",
                                  bg="#9AAEBE").place(x=15, y=78)
        self.password = Entry(self.frame, show='*', font=("eurostile.TTF", 15, "bold"), bg="#C4D8E8")
        self.password.place(x=15, y=108)
        self.login = Button(self.frame, command=self.check_input, text="Login", bd=0,
                            font=("eurostile.TTF", 30, "bold"), bg="#C4D8E8", fg="#444A19").place(x=15, y=153)
        self.access = False
        self.register = Button(self.frame, command=self.register, text="Register", bd=0,
                               font=("eurostile.TTF", 30, "bold"), bg="#C4D8E8", fg="#444A19").place(x=115, y=153)
        self.del_acc = Button(self.frame, command=self.delete_account, text="Delete Account", bd=0,
                              font=("eurostile.TTF", 30, "bold"), bg="#C4D8E8", fg="#444A19").place(x=15, y=208)
        self.profile_user = self.user.get()
        self.user3 = None
        self.password3 = None
        self.user2 = None
        self.password2 = None
        self.root2 = None
        self.root3 = None
        self.conn = sqlite3.connect("Login/passmanager.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        self.update_records_list()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Username TEXT NOT NULL,
                Password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def update_records_list(self):
        conn = sqlite3.connect("Login/passmanager.db")
        cursor = conn.cursor()
        cursor.execute("SELECT *, oid FROM profile")
        records = cursor.fetchall()
        self.p_records = ""
        self.records_list = []
        for record in records:
            self.p_records += f"{record[0]} {record[1]} {record[2]}\n"
            self.records_list.append(record)
        print(self.p_records)
        conn.close()

    def check_input(self):
        if self.user.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            for record in self.records_list:
                if self.user.get() == record[1] and self.password.get() == record[2]:
                    messagebox.showinfo("Welcome", f"Welcome {self.user.get()}", parent=self.root)
                    self.access = True
                    self.conn.commit()
                    self.conn.close()
                    self.profile_user = self.user.get()
                    self.root.iconify()
                    # Close potential delete account and register windows
                    try:
                        self.root2.iconify()
                        self.root3.iconify()
                    except:
                        pass
                    update_login_log(f"LOGIN - User '{self.user.get()}' logged in")
                    webbrowser.open("http://127.0.0.1:10000")
                    return
            messagebox.showerror("Error", "Incorrect username and/or password.", parent=self.root)

    def register(self):
        self.root2 = Toplevel(self.root)
        self.root2.title("Register")
        self.root2.resizable(False, False)
        self.root2.geometry("863x540+878+30")
        root2_bg = ImageTk.PhotoImage(file="Login/SnowMountains.jpg")
        root2_bg_img = Label(self.root2, image=root2_bg).place(x=0, y=0, relwidth=1, relheight=1)
        register_frame2 = Frame(self.root2, bg="#C9C8C4")
        register_frame2.place(x=15, y=15, width=280, height=210)
        register_frame = Frame(self.root2, bg="#009AFC")
        register_frame.place(x=20, y=20, width=270, height=200)
        user2_txt = Label(register_frame, text="Username", font=("eurostile.TTF", 15, "bold"), fg="black",
                          bg="#009AFC").place(x=15, y=10)
        self.user2 = Entry(register_frame, font=("eurostile.TTF", 15, "bold"), bg="#0072D7")
        self.user2.place(x=15, y=40)
        password2_txt = Label(register_frame, text="Password", font=("eurostile.TTF", 15, "bold"), fg="black",
                              bg="#009AFC").place(x=15, y=75)
        self.password2 = Entry(register_frame, show='*', font=("eurostile.TTF", 15, "bold"), bg="#0072D7")
        self.password2.place(x=15, y=105)
        register_btn = Button(register_frame, command=self.check_input_register, text="Register", bd=0,
                              font=("eurostile.TTF", 30, "bold"), bg="#D7C100", fg="#444A19").place(x=15, y=145)
        self.root2.mainloop()

    def check_input_register(self):
        if self.user2.get() == "" or self.password2.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root2)
        else:
            new_user_id = self.get_next_user_id()
            conn = sqlite3.connect("Login/passmanager.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO profile VALUES (:UserID, :Username, :Password)",
                           {
                               'UserID': new_user_id,
                               'Username': self.user2.get(),
                               'Password': self.password2.get()
                           })
            conn.commit()
            conn.close()
            self.update_records_list()  # Refresh the records list after registration
            update_login_log(f"LOGIN - User '{self.user2.get()}' created account")
            messagebox.showinfo("Register Success", "Register Success", parent=self.root2)
            self.user2.delete(0, END)
            self.password2.delete(0, END)

    def delete_account(self):
        self.root3 = Toplevel(self.root)
        self.root3.title("Delete Account")
        self.root3.resizable(False, False)
        self.root3.geometry("863x540+15+570")
        root3_bg = ImageTk.PhotoImage(file="Login/Goldengate.jpg")
        root3_bg_img = Label(self.root3, image=root3_bg).place(x=0, y=0, relwidth=1, relheight=1)
        register_frame2_del = Frame(self.root3, bg="#73ACC1")
        register_frame2_del.place(x=15, y=15, width=280, height=260)
        register_frame_del = Frame(self.root3, bg="#FFD500")
        register_frame_del.place(x=20, y=20, width=270, height=250)
        del_acc_txt = Label(register_frame_del, text="Delete Account", font=("eurostile.TTF", 30, "bold"), fg="#444A19",
                            bg="#FFD500").place(x=15, y=15)
        user3_txt = Label(register_frame_del, text="Username", font=("eurostile.TTF", 15, "bold"), fg="black",
                          bg="#FFD500").place(x=15, y=60)
        self.user3 = Entry(register_frame_del, font=("eurostile.TTF", 15, "bold"), bg="#D7C100")
        self.user3.place(x=15, y=90)
        password3_txt = Label(register_frame_del, text="Password", font=("eurostile.TTF", 15, "bold"), fg="black",
                              bg="#FFD500").place(x=15, y=125)
        self.password3 = Entry(register_frame_del, show='*', font=("eurostile.TTF", 15, "bold"), bg="#D7C100")
        self.password3.place(x=15, y=155)
        del_acc = Button(register_frame_del, command=self.check_input_del_acc, text="Delete Account", bd=0,
                         font=("eurostile.TTF", 30, "bold"), bg="#D7C100", fg="#444A19").place(x=15, y=190)
        self.root3.mainloop()

    def check_input_del_acc(self):
        if self.user3.get() == "" or self.password3.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root3)
        else:
            for record in self.records_list:
                if self.user3.get() == record[1] and self.password3.get() == record[2]:
                    conn = sqlite3.connect("Login/passmanager.db")
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM profile WHERE oid = {record[0]}")
                    conn.commit()
                    conn.close()
                    self.update_records_list()
                    update_login_log(f"LOGIN - User '{self.user3.get()}' deleted account")
                    messagebox.showinfo("Account Deleted", "Account Deleted", parent=self.root3)
                    self.user3.delete(0, END)
                    self.password3.delete(0, END)
                    return
            messagebox.showerror("Error", "Invalid username and/or password", parent=self.root3)

    def get_next_user_id(self):
        with open("Login/userID.txt", "r+") as file:
            user_id = int(file.read().strip())
            new_id = user_id + 1
            file.seek(0)
            file.write(str(new_id))
        return new_id
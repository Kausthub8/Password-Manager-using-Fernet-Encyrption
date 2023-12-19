from cryptography.fernet import Fernet
import sqlite3
from tkinter import *
import random
from tkinter import messagebox
import os
import webbrowser
import random


my_password = ""


my_fernet = ""


root = Tk()
root.geometry("600x600")
root.title("Password Manager Using Fernet Encryption")


main_frame = Frame(root, padx=5, pady=5)
secondary_frame = Frame(root, padx=5, pady=5)
rbutton_frame = Frame(root, padx=5, pady=5)
output_frame = Frame(root, padx=5, pady=5)
bottom_bar = Frame(root, padx=5, pady=5)

main_frame.pack(padx=20, pady=0)
secondary_frame.pack(padx=20, pady=20)
rbutton_frame.pack(padx=10, pady=0)
output_frame.pack(padx=15, pady=5)
bottom_bar.pack(side=BOTTOM)

title = Label(main_frame, text="Password Generator")
title.pack(padx=20, pady=0)

length = Label(secondary_frame, text="Password Length b/w (2-20):")
length.grid(row=0, column=0)

length_entry = Entry(secondary_frame)
length_entry.grid(row=0, column=1)


def encrypt_db():
    with open('pw.db', 'rb') as to_encrypt:
        data = to_encrypt.read()
        data = my_fernet.encrypt(data)
        with open('pw.db', "wb") as encrypt:
            encrypt.write(data)


def decrypt_db():
    with open('pw.db', 'rb') as to_decrypt:
        data = to_decrypt.read()
        data = my_fernet.decrypt(data)
        with open('pw.db', 'wb') as decrypt:
            decrypt.write(data)


# Function for saving master password
def save_master():
   
    with open('key.key', 'wb') as f:
        key = Fernet.generate_key()
        global my_fernet
        my_fernet = Fernet(key)
        f.seek(0)
        f.write(key)

    # Writing Encoded Master Password
    with open('pw.txt', 'wb') as f:
        f.seek(0)
        global my_password
        my_password = masterpassword.get()
        password_write = my_password.encode('utf-8')
        password_write = my_fernet.encrypt(password_write)
        f.write(password_write)
    First_time.destroy()
    root.deiconify()
    encrypt_db()



with open('TestRun.txt', 'a+') as f:
    f.seek(0)
    f_contents = f.read()
    if f_contents == '1':
        with open('key.key', 'rb') as kf:
            kf.seek(0)
            kf_contents = kf.read()
            key = kf_contents
            my_fernet = Fernet(key)

        # Get Master Password
        with open('pw.txt', 'rb') as pf:
            pf.seek(0)
            pf_contents = pf.read()
            pf_contents = my_fernet.decrypt(pf_contents)
            pf_contents = pf_contents.decode('utf-8')
            my_password = pf_contents
    else:
        root.withdraw()
        f.seek(0)
        f.write('1')
        db = sqlite3.connect('pw.db')
        cursor = db.cursor()
        cursor.execute('''
        CREATE TABLE passwords (
        app_id VARCHAR [255],
        username_email VARCHAR [255],
        password VARCHAR [255])
        ''')
        db.commit()
        db.close()

        # First Time run Popup
        First_time = Toplevel()
        First_time.title('Setup')
        First_time.geometry('250x140')

    
        labelframe = LabelFrame(
            First_time, text="Set a master password for all your passwords.")
        labelframe.pack(fill="both", expand="yes")
        button_frame = Frame(First_time)
        button_frame.pack()

        
        masterpassword = Entry(labelframe, width=25)
        masterpassword.pack(padx=10, pady=0)

    

        
        AddButton = Button(
            button_frame, text='Set Master Password', command=save_master)
        AddButton.pack()


def Pw_Notebook():
    notebook = Toplevel()
    notebook.title('Password Log')
    notebook.geometry('420x700')

    # Function for reloading a the Password Notebook.
    def Pw_Notebook_reload():
        notebook.destroy()
        Pw_Notebook()

    # Function for adding and deleting passwords
    def add_pass():

        def save_pw():
            decrypt_db()
            db = sqlite3.connect('pw.db')
            cursor = db.cursor()
            cursor.execute("INSERT INTO passwords VALUES (:App, :Username, :Password)",
                           {'App': app_id_e.get(),
                            'Username': username_e.get(),
                            'Password': password_e.get()
                            })
            db.commit()
            db.close()
            encrypt_db()
            a_pass.destroy()
            Pw_Notebook_reload()
            alert('Notification', 'Password Saved to Password Notebook')

        a_pass = Toplevel()
        a_pass.title('Add Password')
        a_pass.geometry('300x200')

        pw_add_frame = LabelFrame(
            a_pass, text='Add Password', padx=10, pady=10)
        pw_add_frame.pack(padx=5, pady=5)

        another_buttn_frame = Frame(a_pass, padx=10, pady=10)
        another_buttn_frame.pack(padx=0, pady=15)

        app_id = Label(pw_add_frame, text="Application Name: ")
        app_id.grid(row=0, column=0)
        app_id_e = Entry(pw_add_frame)
        app_id_e.grid(row=0, column=1)

        username = Label(pw_add_frame, text="Username: ")
        username.grid(row=1, column=0)
        username_e = Entry(pw_add_frame)
        username_e.grid(row=1, column=1)

        password_label = Label(pw_add_frame, text='Password: ')
        password_label.grid(row=2, column=0)

        password_e = Entry(pw_add_frame)
        password_e.grid(row=2, column=1)

        # Submit Button
        Add_record_bttn = Button(
            another_buttn_frame, text="Add Password", command=save_pw)
        Add_record_bttn.pack()

    def delete_pass():
        def delete_pw():
            decrypt_db()
            db = sqlite3.connect('pw.db')
            cursor = db.cursor()
            cursor.execute("DELETE FROM passwords WHERE app_id = :app", {
                'app': app_name_delete.get()
            })
            db.commit()
            db.close()
            encrypt_db()
            a_pass.destroy()
            Pw_Notebook_reload()
            alert('Notification', 'Password Deleted')

        a_pass = Toplevel()
        a_pass.title('Delete Password')
        a_pass.geometry('300x200')

        pw_add_frame = LabelFrame(
            a_pass, text='Add Password', padx=10, pady=10)
        pw_add_frame.pack(padx=5, pady=5)

        another_buttn_frame = Frame(a_pass, padx=10, pady=10)
        another_buttn_frame.pack(padx=0, pady=15)

        app_name = Label(pw_add_frame, text="Application name to delete: ")
        app_name.grid(row=0, column=0)
        app_name_delete = Entry(pw_add_frame)
        app_name_delete.grid(row=0, column=1)

        # Submit Button
        Add_record_bttn = Button(
            another_buttn_frame, text="Delete", command=delete_pw)
        Add_record_bttn.pack()

    # Creating an Label Frame to House Stuff.
    db_frame = LabelFrame(
        notebook, text="Passwords:")
    db_frame.pack(fill="both", expand="yes")

    # Creating another frame for housing add record button and delete.
    buttn_frame = Frame(notebook, padx=10, pady=10)
    buttn_frame.pack(padx=5, pady=25)

    # Creating Labels for the row.
    Appid_label = Label(db_frame, text="App Name")
    Appid_label.grid(row=0, column=1)

    username_label = Label(db_frame, text="Username")
    username_label.grid(row=0, column=2)

    password_label = Label(db_frame, text="Passwords")
    password_label.grid(row=0, column=3)

    # Acessing Our Database
    decrypt_db()
    db = sqlite3.connect('pw.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM passwords")

    i = 1
    for password_sql in cursor:
        for j in range(len(password_sql)):
            numberline = str(i)
            numberline = numberline + ". "
            l = Label(db_frame, text=numberline)
            l.grid(row=i, column=0)
            e = Entry(db_frame, width=20, fg='blue')
            u = j + 1
            e.grid(row=i, column=u)
            e.insert(END, password_sql[j])
        i = i+1
    encrypt_db()

    # Creating Buttons to add or delete
    add_record = Button(buttn_frame, text='Add Password', command=add_pass)
    add_record.grid(row=0, column=0)

    delete_record = Button(
        buttn_frame, text='Delete Password', command=delete_pass)
    delete_record.grid(row=0, column=1)


# Function for launching Settings Page
def Settings():
    settings = Toplevel()
    settings.title('Settings')
    settings.geometry('300x300')

    change_m_frame = LabelFrame(
        settings, text="Change Master Password", padx=10, pady=10)
    change_m_frame.pack(padx=10, pady=10)

    settings_buttn_frame = Frame(settings)
    settings_buttn_frame.pack(padx=10, pady=20)

    def change_m():
        with open('pw.txt', 'wb') as f:
            f.seek(0)
            global my_password
            my_password = masterpassword_new.get()
            password_write = my_password.encode('utf-8')
            password_write = my_fernet.encrypt(password_write)
            f.write(password_write)
            alert('Info', 'Master Password has been changed')

    masterpassword_new = Entry(change_m_frame)
    masterpassword_new.pack()

    change_m_buttn = Button(settings_buttn_frame,
                            text="Change Master Password", command=change_m)
    change_m_buttn.pack()


import random

def Authentication1():

    # Define function to generate random code
    def generate_code():
        code = ''.join(random.choices('0123456789', k=6)) # Generate 6-digit code
        code_label.config(text=code) # Update code label with generated code

    # Creating Tkinter Window
    Authenticate = Toplevel()
    Authenticate.title('Authenticate')
    Authenticate.geometry('200x200')

    # Creating Components of the Window
    AuthenticateFrame = LabelFrame(
        Authenticate, text="Enter Master Password")
    AuthenticateFrame.pack(fill="both", expand="yes")

    # Add label for random code
    code_label = Label(AuthenticateFrame, text="Click on the button to get a randomzied code")
    code_label.pack()

    # Button to generate random code
    code_button = Button(AuthenticateFrame, text='Generate Code', command=generate_code)
    code_button.pack()

    button_frame1 = Frame(AuthenticateFrame)
    button_frame1.pack()

    # Entry Field for Password
    my_password_entry = Entry(AuthenticateFrame, width=25)
    my_password_entry.pack()

    # Where the real authentication code goes.
    # This one is for Password Notebook.:
    def RealAuthenticate1():
        m_entry = my_password_entry.get()
        if m_entry == my_password and code_entry.get() == code_label.cget("text"): # Check if password and code match
            Authenticate.destroy()
            Pw_Notebook()

        else:
            alert('Authentication Failed', 'Password or Code  is Incorrect', kind='warning')

    # Entry Field for Code
    code_entry = Entry(AuthenticateFrame, width=6)
    code_entry.pack()

    Auth_Button = Button(
        button_frame1, text='Authenticate', command=RealAuthenticate1)
    Auth_Button.pack()




def Authentication2():

    # Define function to generate random code
    def generate_code():
        code = ''.join(random.choices('0123456789', k=6)) # Generate 6-digit code
        code_label.config(text=code) # Update code label with generated code

    # Creating Tkinter Window
    Authenticate = Toplevel()
    Authenticate.title('Authenticate')
    Authenticate.geometry('200x200')

    # Creating Components of the Window
    AuthenticateFrame = LabelFrame(
        Authenticate, text="Enter Master Password")
    AuthenticateFrame.pack(fill="both", expand="yes")

    # Add label for random code
    code_label = Label(AuthenticateFrame, text="Click on the button to get a randomized code")
    code_label.pack()

    # Button to generate random code
    code_button = Button(AuthenticateFrame, text='Generate Code', command=generate_code)
    code_button.pack()

    button_frame1 = Frame(AuthenticateFrame)
    button_frame1.pack()

    # Entry Field for Password
    my_password_entry = Entry(AuthenticateFrame, width=25)
    my_password_entry.pack()

    # Where the real authentication code goes.
    # This one is for Password Notebook.:
    def RealAuthenticate2():
        m_entry = my_password_entry.get()
        if m_entry == my_password and code_entry.get() == code_label.cget("text"): # Check if password and code match
            Authenticate.destroy()
            Settings()

        else:
            alert('Authentication Failed', 'Password or Code is Incorrect', kind='warning')

    # Entry Field for Code
    code_entry = Entry(AuthenticateFrame, width=6)
    code_entry.pack()

    Auth_Button = Button(
        button_frame1, text='Authenticate', command=RealAuthenticate2)
    Auth_Button.pack()


# Bottom Bar Buttons
Password_Notebook_Bttn = Button(
    bottom_bar, text="Password Notebook", command = lambda: Authentication1())
Password_Notebook_Bttn.grid(row=0, column=0)


# Settings Button
Settings_Bttn = Button(bottom_bar, text="Settings", command=Authentication2)
Settings_Bttn.grid(row=1, column=0)




def alert(title, message, kind='info', hidemain=True):
    if kind not in ('error', 'warning', 'info'):
        raise ValueError('Unsupported alert kind.')

    show_method = getattr(messagebox, 'show{}'.format(kind))
    show_method(title, message)


# Function for generating Password
def generate_pass():
    password_length = int(length_entry.get())
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZADEFKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789&{([-_@)]}=+*$%!?&{([-_@)]}=+*$%!?"
    generated_password = ""
    for x in range(0, password_length):
        generated_password += str(random.choice(characters))

    def save_main():
        decrypt_db()
        db = sqlite3.connect('pw.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO passwords VALUES (:App, :Username, :Password)",
                       {'App': app_id_entry.get(),
                        'Username': username_input.get(),
                        'Password': output_e.get()
                        })
        db.commit()
        db.close()
        encrypt_db()
        alert('Information', 'Password Saved to Password Notebook')

    app_id_label = Label(output_frame, text="Application Name: ")
    app_id_label.grid(row=1, column=0)
    app_id_entry = Entry(output_frame)
    app_id_entry.grid(row=1, column=1)

    username_label = Label(output_frame, text="Username/Email: ")
    username_label.grid(row=2, column=0)
    username_input = Entry(output_frame)
    username_input.grid(row=2, column=1)

    output_label = Label(output_frame, text='Generated Password: ')
    output_label.grid(row=0, column=0)

    output_e = Entry(output_frame)
    output_e.insert(END, generated_password)
    output_e.grid(row=0, column=1)

    root.clipboard_clear()
    root.clipboard_append(generated_password)

    save_main_button = Button(
        output_frame, text="Save Password", command=save_main)
    save_main_button.grid(row=3, column=1)
    root.geometry("300x400")


generate_button = Button(
    rbutton_frame, text="Generate Password", command=generate_pass)
generate_button.grid(row=0, column=0)

generate_text = Label(
    rbutton_frame, text="Text will automatically be copied to clipboard.")
generate_text.grid(row=1, column=0)


# Starting the Windows
root.mainloop()




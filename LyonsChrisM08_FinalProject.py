import tkinter as tk
from tkinter import ttk, messagebox
import string
import random
import re


class WelcomePage:
    def __init__(self, master):
        self.master = master
        master.title("PassSafe")
        master.geometry("500x700")
        master.configure(bg="white")

        # create a label for the welcome message
        self.welcome_label = tk.Label(master, text="Welcome to PassSafe", font=("Arial", 20, "bold"), fg="#3871C1", bg="white")
        self.welcome_label.pack(pady=50)

        # create a label for the image
        self.image = tk.PhotoImage(file="C:/Users/chris\OneDrive/Pictures/PassSafe.gif")
        image_label = tk.Label(master, image=self.image, bg="white")
        image_label.pack(side="top", fill="both", expand=True, padx=50, pady=20)

        # create a login button
        self.login_button = tk.Button(master, text="Login", font=("Arial", 12), width=10, command=self.login_callback, fg="#F14624")
        self.login_button.pack(pady=20)

        # create a create account button
        self.create_account_button = tk.Button(master, text="Create an Account", font=("Arial", 12), width=15, command=self.create_account_callback, fg="#F14624")
        self.create_account_button.pack(pady=20)

        # create a quit button
        self.quit_button = tk.Button(master, text="Quit", font=("Arial", 12), width=10, command=self.quit_callback, fg="#F14624")
        self.quit_button.pack(pady=20)

    def quit_callback(self):
        self.master.destroy()

    def login_callback(self):
        login_window = tk.Toplevel(root)
        login_window.title("Login")


        # create labels and entry boxes
        tk.Label(login_window, text="Email Address: ").grid(row=0, column=0)
        email_entry = tk.Entry(login_window)
        email_entry.grid(row=0, column=1)
        tk.Label(login_window, text="Password: ").grid(row=1, column=0)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.grid(row=1, column=1)

        def submit_callback():
            # retrieve user info from file
            with open('users.txt', 'r') as file:
                user_info = file.readlines()
            # loop through user info to find a match
            for user in user_info:
                user = user.strip().split(',')
                if user[2] == email_entry.get() and user[3] == password_entry.get():
                    tk.messagebox.showinfo("Success", "Login Successful")
                    login_window.destroy()
                    # create new window
                    new_window = tk.Toplevel()
                    new_window.title("Password Manager")
                    new_window.geometry("600x400")
                    new_window.configure(bg="white")

                    # add images to the new window
                    global left_image
                    global right_image

                    left_image = tk.PhotoImage(file="C:/Users/chris\OneDrive/Pictures/Orange Lock.gif")
                    right_image = tk.PhotoImage(file="C:/Users/chris\OneDrive/Pictures/Blue Lock.gif")

                    left_image_label = tk.Label(new_window, image=left_image, bg="white")
                    left_image_label.place(relx=0, rely=0.5, anchor="w")

                    right_image_label = tk.Label(new_window, image=right_image, bg="white")
                    right_image_label.place(relx=1, rely=0.5, anchor="e")

                    # add buttons to the new window
                    # Create a frame to hold the buttons
                    button_frame = tk.Frame(new_window, bg="white")
                    button_frame.pack(expand=True)

                    store_password_button = tk.Button(button_frame, text="Store Password", width=15, height=2,
                                                      command=store_password, fg="#F14624")
                    store_password_button.pack(pady=10)

                    retrieve_password_button = tk.Button(button_frame, text="Retrieve Passwords", width=15, height=2,command=retrieve_passwords, fg="#F14624")
                    retrieve_password_button.pack(pady=10)

                    create_password_button = tk.Button(button_frame, text="Create A Password", width=15, height=2, command=create_password, fg="#F14624")
                    create_password_button.pack(pady=10)

                    grade_password_button = tk.Button(button_frame, text="Grade My Password", width=15, height=2, command=grade_my_password, fg="#F14624")
                    grade_password_button.pack(pady=10)

                    logout_button = tk.Button(button_frame, text="Logout", width=15, height=2, command=logout, fg="#F14624")
                    logout_button.pack(pady=10)

                    break
            else:
                tk.messagebox.showerror("Error", "Invalid email address or password")

        current_user = ""

        def login():
            # set the value of current_user when the user logs in
            global current_user
            current_user = "username"  # replace with the actual username input from the user

        def store_password():
            # create a new window for storing passwords
            store_password_window = tk.Toplevel()
            store_password_window.title("Store Password")
            store_password_window.geometry("300x200")

            # create labels and entries for account name, email, and password
            account_name_label = tk.Label(store_password_window, text="Account Name:")
            account_name_label.pack()
            account_name_entry = tk.Entry(store_password_window)
            account_name_entry.pack()

            email_label = tk.Label(store_password_window, text="Email:")
            email_label.pack()
            email_entry = tk.Entry(store_password_window)
            email_entry.pack()

            password_label = tk.Label(store_password_window, text="Password:")
            password_label.pack()
            password_entry = tk.Entry(store_password_window, show="*")
            password_entry.pack()

            def on_submit():
                # create a filename for the user's password file
                filename = f"{current_user}_passwords.txt"

                # append the new account info to the user's password file
                with open(filename, 'a') as password_file:
                    password_file.write(f"{account_name_entry.get()},{email_entry.get()},{password_entry.get()}\n")

                # clear the input fields
                account_name_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)

                # show success message
                tk.messagebox.showinfo("Success", "Account Info Stored Successfully")

            # create a button for submitting the form
            submit_button = tk.Button(store_password_window, text="Submit", command=on_submit)
            submit_button.pack()

        def retrieve_passwords():
            # create a new window for retrieving passwords
            retrieve_passwords_window = tk.Toplevel()
            retrieve_passwords_window.title("Retrieve Passwords")
            retrieve_passwords_window.geometry("800x600")

            # create a frame for the password listbox
            listbox_frame = tk.Frame(retrieve_passwords_window)
            listbox_frame.pack(pady=10)

            # add headers to the listbox
            account_name_label = tk.Label(listbox_frame, text="Account Name", borderwidth=1, relief="solid", width=20)
            account_name_label.grid(row=0, column=0, sticky="nsew")
            email_label = tk.Label(listbox_frame, text="Email", borderwidth=1, relief="solid", width=30)
            email_label.grid(row=0, column=1, sticky="nsew")
            password_label = tk.Label(listbox_frame, text="Password", borderwidth=1, relief="solid", width=20)
            password_label.grid(row=0, column=2, sticky="nsew")

            # create a filename for the user's password file
            filename = f"{current_user}_passwords.txt"

            # read the user's password file and add each account to the listbox
            with open(filename, 'r') as password_file:
                row_index = 1
                for line in password_file:
                    account_info = line.strip().split(",")
                    account_name, email, password = account_info

                    account_name_label = tk.Label(listbox_frame, text=account_name, borderwidth=1, relief="solid",
                                                  width=20)
                    account_name_label.grid(row=row_index, column=0, sticky="nsew")

                    email_label = tk.Label(listbox_frame, text=email, borderwidth=1, relief="solid", width=30)
                    email_label.grid(row=row_index, column=1, sticky="nsew")

                    password_label = tk.Label(listbox_frame, text=password, borderwidth=1, relief="solid", width=20)
                    password_label.grid(row=row_index, column=2, sticky="nsew")

                    row_index += 1

            # create gridlines
            for i in range(3):
                listbox_frame.grid_columnconfigure(i, weight=1, minsize=100)
            for i in range(row_index):
                listbox_frame.grid_rowconfigure(i, weight=1, minsize=30)

            # create a button for closing the window
            close_button = tk.Button(retrieve_passwords_window, text="Close", command=retrieve_passwords_window.destroy)
            close_button.pack(pady=10)

        def generate_password(length):
            """Generates a random password of given length."""
            chars = string.ascii_letters + string.digits + string.punctuation
            return ''.join(random.choice(chars) for _ in range(length))

        def create_password():
            # create a new window for generating a password
            create_password_window = tk.Toplevel()
            create_password_window.title("Create Password")
            create_password_window.geometry("500x300")

            # create a label to show the generated password
            password_label = tk.Label(create_password_window, text="", font=("Arial", 12))
            password_label.pack(pady=10)

            # ask the user for the desired length of the password
            length_label = tk.Label(create_password_window, text="Enter password length (12-30):")
            length_label.pack()
            length_entry = tk.Entry(create_password_window)
            length_entry.pack()

            # ask the user for the number of passwords to generate
            num_passwords_label = tk.Label(create_password_window, text="Enter number of passwords (1-10):")
            num_passwords_label.pack()
            num_passwords_entry = tk.Entry(create_password_window)
            num_passwords_entry.pack()

            # create a button for generating the password(s)
            def generate():
                try:
                    length = int(length_entry.get())
                    if length < 12 or length > 30:
                        raise ValueError
                    num_passwords = int(num_passwords_entry.get())
                    if num_passwords < 1 or num_passwords > 10:
                        raise ValueError
                    passwords = [generate_password(length) for _ in range(num_passwords)]
                    password_label.configure(text='\n\n'.join(passwords))
                except ValueError:
                    password_label.configure(text="Invalid input")

            generate_button = tk.Button(create_password_window, text="Generate", command=generate)
            generate_button.pack(pady=10)

            # create a button for closing the window
            close_button = tk.Button(create_password_window, text="Close", command=create_password_window.destroy)
            close_button.pack()

        def grade_password(password):
            """Grades a password based on strength criteria."""
            lowercase = bool(re.search(r'[a-z]', password))
            uppercase = bool(re.search(r'[A-Z]', password))
            special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
            number = bool(re.search(r'\d', password))
            length = len(password) >= 12

            metrics = [lowercase, uppercase, special, number, length]
            num_metrics_met = sum(metrics)

            if num_metrics_met == 5:
                return "Strong Password"
            elif num_metrics_met >= 3:
                return "Moderate Password"
            else:
                return "Weak Password"

        def grade_my_password():
            # create a new window for grading a password
            grade_password_window = tk.Toplevel()
            grade_password_window.title("Grade My Password")
            grade_password_window.geometry("400x200")

            # create a label to ask the user for their password
            password_label = tk.Label(grade_password_window, text="Enter your password:")
            password_label.pack(pady=10)

            # create an entry for the user to type their password
            password_entry = tk.Entry(grade_password_window)
            password_entry.pack()

            # create a button for grading the password
            def grade():
                password = password_entry.get()
                grade_label.configure(text=grade_password(password))

            grade_button = tk.Button(grade_password_window, text="Grade", command=grade)
            grade_button.pack(pady=10)

            # create a label to show the password grade
            grade_label = tk.Label(grade_password_window, text="")
            grade_label.pack()

            # create a button for closing the window
            close_button = tk.Button(grade_password_window, text="Close", command=grade_password_window.destroy)
            close_button.pack()

        def logout():
            # create a pop-up message
            messagebox.showinfo("PassSafe", "Thank you for using PassSafe!")

            # destroy the main window and end the program
            root.destroy()



        submit_button = tk.Button(login_window, text="Submit", command=submit_callback)
        submit_button.grid(row=2, column=0, columnspan=2)
        login_window




    def create_account_callback(self):
        # callback function for the create account button
        self.create_account_window = tk.Toplevel(self.master)
        self.create_account_window.title("Create an Account")
        self.create_account_window.geometry("400x300")

        # create labels and entry fields for the input fields
        tk.Label(self.create_account_window, text="First Name:").grid(row=0, column=0, padx=10, pady=10)
        self.first_name_entry = tk.Entry(self.create_account_window)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.create_account_window, text="Last Name:").grid(row=1, column=0, padx=10, pady=10)
        self.last_name_entry = tk.Entry(self.create_account_window)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.create_account_window, text="Email Address:").grid(row=2, column=0, padx=10, pady=10)
        self.email_entry = tk.Entry(self.create_account_window)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.create_account_window, text="Password:").grid(row=3, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.create_account_window, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=10)

        # create a button to submit the user's information
        submit_button = tk.Button(self.create_account_window, text="Submit", command=self.submit_callback)
        submit_button.grid(row=4, column=1, padx=10, pady=20)

    def submit_callback(self):
        # callback function for the submit button
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        # perform input validation to ensure all fields are filled out
        if not first_name:
            tk.messagebox.showerror("Error", "Please enter your first name")
            return
        if not last_name:
            tk.messagebox.showerror("Error", "Please enter your last name")
            return
        if not email:
            tk.messagebox.showerror("Error", "Please enter your email address")
            return
        if not password:
            tk.messagebox.showerror("Error", "Please enter a password")
            return

        # store the user's information in a local file
        with open("users.txt", "a") as file:
            file.write(f"{first_name},{last_name},{email},{password}\n")

        # close the create account window and show a message
        self.create_account_window.destroy()
        tk.messagebox.showinfo("Success", "Your account has been created")


root = tk.Tk()
welcome_page = WelcomePage(root)
root.mainloop()

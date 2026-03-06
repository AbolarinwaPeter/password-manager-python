from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_password():
    letter_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
                   ,'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    num_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    symbol_list = ["!", "#", "$", "%", "(", ")", "*", "+"]
    letter_count = random.randint(8,10)
    num_count = random.randint(2, 4)
    symbol_count = random.randint(2, 4)
    password = [random.choice(letter_list) for _ in range(letter_count)]
    password.extend([random.choice(num_list) for _ in range(num_count)])
    password.extend([random.choice(symbol_list) for _ in range(symbol_count)])
    random.shuffle(password)
    password_string = "".join(password)
    pyperclip.copy(password_string)
    password_entry.insert(0,password_string)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_password():
    website_name = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    file_data = {website_name: {"Email": email, "Password": password}}
    if len(website_name) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showerror("Error", "Please fill all fields")
    else:
        is_ok = messagebox.askokcancel(title = website_name, message= f"These are the details entered:\nEmail: {email}\nPassword: {password}")
        if is_ok:
            try:
                with open("passwords.json", "r") as password_file:
                    data = json.load(password_file)
                    data.update(file_data)
            except FileNotFoundError:
                data = file_data
            finally:
                with open("passwords.json", mode= "w") as file:
                    json.dump(data, file, indent=4)
            website_entry.delete(0, END)
            # email_entry.delete(0, END)
            password_entry.delete(0, END)
# ---------------------------- SEARCH PASSWORDS ----------------------- #
def get_password():
    try:
        with open("passwords.json", "r") as file:
            my_passwords = json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Error", "You dont have any passwords saved")
    else:
        if website_entry.get() in my_passwords:
            search_result = my_passwords[website_entry.get()]
            messagebox.showinfo(website_entry.get(),
                                f"Email: {search_result["Email"]}\nPassword: {search_result["Password"]}")
        else:
            messagebox.showerror(website_entry.get(), f"You dont have any passwords saved for this site")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
canvas = Canvas(width= 200, height=200, highlightthickness=5, highlightcolor="black", background="white")
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
# canvas.create_rectangle(0, 0, 200, 200,)
canvas.grid(row=0, column=1)
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
website_entry = Entry(width = 24)
website_entry.grid(row= 1, column=1, columnspan=1)
website_entry.focus()
email_entry = Entry(width=42)
email_entry.insert(0, "your-email@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=24)
password_entry.grid(row=3, column=1)
generate_password = Button(text="Generate Password", command=gen_password)
generate_password.grid(row=3, column=2)
add_button = Button(text="Add Password", width=36, command= add_password)
add_button.grid(row=4, column=1, columnspan=2)
search_button = Button(text="Search", command=get_password, width=15)
search_button.grid(row=1, column=2, columnspan=2)


window.mainloop()
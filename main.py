from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list.extend([random.choice(letters) for i in range(nr_letters)])
    password_list.extend([random.choice(symbols) for i in range(nr_symbols)])
    password_list.extend([random.choice(numbers) for i in range(nr_numbers)])

    random.shuffle(password_list)
    passwords = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(END, passwords)
    pyperclip.copy(passwords)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def write_to_file():
    web = website_entry.get().title()
    user = email_entry.get()
    pw = password_entry.get()
    new_data = {
        web: {
            "email": user,
            "password": pw,
        }
    }

    if len(web) == 0 or len(pw) == 0 or len(user) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=web, message=f"These are the details entered: \nEmail: {user} "
                                                          f"\nPassword: {pw} \nIs it ok to save?")
        if is_ok:
            try:
                with open("my_password.json", "r") as file:
                    # read
                    data = json.load(file)
            except FileNotFoundError:
                with open("my_password.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # update
                data.update(new_data)

                with open("my_password.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    web = website_entry.get().title()
    try:
        with open("my_password.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="Add at least one password to enable search function")
    else:
        if web in data:
            result_email = data[web]["email"]
            password = str(data[web]["password"])
            pyperclip.copy(password)
            messagebox.showinfo(title="Your details", message=f"Email: {result_email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Oops", message=f"No password for {web} has been saved here")


# ---------------------------- UI SETUP ------------------------------- #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=200, height=200)
lock_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_image)
canvas.grid(column=1, row=0)

# Labels
website = Label(text="Website: ")
email = Label(text="Email/Username: ")
password = Label(text="Password: ")
website.grid(column=0, row=1)
email.grid(column=0, row=2)
password.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21)
email_entry = Entry(width=38)
password_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(END, "liangjitian777@gmail.com")
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", width=36, command=write_to_file)
generate_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", command=search_password, width=13)
search_button.grid(column=2, row=1)

window.mainloop()

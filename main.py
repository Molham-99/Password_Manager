from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
FONT = "Arial"


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letters_pass = [random.choice(letters) for _ in range(nr_letters)]
    symbols_pass = [random.choice(symbols) for _ in range(nr_symbols)]
    number_pass = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = letters_pass + symbols_pass + number_pass
    random.shuffle(password_list)
    password = "".join(password_list)
    enter_password.delete(0, END)
    enter_password.insert(END, string=password)
    pyperclip.copy(password)


def save():
    website_content = enter_website.get()
    email_content = enter_email.get()
    password_content = enter_password.get()
    new_data = {
        website_content: {
        "email": email_content,
        "password": password_content,
        }
    }
    if website_content == "" or email_content == "" or password_content == "":
        messagebox.showinfo(title="Oops!!!!", message="Please don't leave any fields empty! ")
    else:
        is_ok = messagebox.askokcancel(title="Details message!", message=f"Those are the details entered :\n"
                                                                         f" Website: {website_content}\n"
                                                                         f" Email: {email_content}\n"
                                                                         f" Password: {password_content}")
        if is_ok:
            try:
                with open("data.json", mode="r") as data:
                    data_file = json.load(data)
            except FileNotFoundError:
                with open("data.json", mode="w") as data:
                    json.dump(new_data, data, indent=4)
            except:
                with open("data.json", mode="w") as data:
                    json.dump(new_data, data, indent=4)
            else:
                data_file.update(new_data)
                with open("data.json", mode="w") as data:
                    json.dump(data_file, data, indent=4)
            finally:
                enter_website.delete(0, END)
                enter_password.delete(0, END)


def search():
    website_content = enter_website.get()
    try:
        with open("data.json", mode="r") as data:
            data_file = json.load(data)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data Found!")
    else:

        if len(website_content) == 0:
            messagebox.showinfo(title="Error", message="the field is empty!")

        if website_content in data_file:
            info = data_file[website_content]
            messagebox.showinfo(title=f"{website_content}", message=f"Email: {info['email']}\n"
                                                                    f" Password: {info['password']}")
            enter_password.insert(END, string=info['password'])
            pyperclip.copy(info['password'])
        else:
            messagebox.showinfo(title=f"{website_content}", message=f"No details for {website_content} exist!")


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website: ", font=(FONT, 8, "bold"))
website_label.grid(column=0, row=1)

email_user_label = Label(text="Email/Username: ", font=(FONT, 8, "bold"))
email_user_label.grid(column=0, row=2)

password_label = Label(text="Password: ", font=(FONT, 8, "bold"))
password_label.grid(column=0, row=3)

add_button = Button(text="Add", width=45, font=(FONT, 8, "bold"), command=save)
add_button.grid(column=1, row=4, columnspan=2)

create_button = Button(text="Create Password", font=(FONT, 8, "bold"), width=14, command=generate_password)
create_button.grid(column=2, row=3)

search_button = Button(text="Search", font=(FONT, 8, "bold"), width=14, command=search)
search_button.grid(column=2, row=1)

enter_website = Entry(width=34)
enter_website.grid(column=1, row=1)
enter_website.focus()

enter_email = Entry(width=53)
enter_email.grid(column=1, row=2, columnspan=2)
enter_email.insert(0, "Example@gmail.com")

enter_password = Entry(width=34)
enter_password.grid(column=1, row=3)

window.mainloop()

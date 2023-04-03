from tkinter import *
from client import


class LoginWindow:
    def __init__(self, win):
        self.master = win
        self.master.title("Login")

        self.label_username = Label(self.master, text="Username")
        self.label_password = Label(self.master, text="Password")

        self.entry_username = Entry(self.master)
        self.entry_password = Entry(self.master, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.checkbutton = Checkbutton(self.master, text="Keep me logged in")
        self.checkbutton.grid(columnspan=2)

        self.login_button = Button(self.master, text="Login", command=self.login)
        self.login_button.grid(columnspan=2)

    def login(self):
        # Perform login validation
        user_id = 123  # Replace with actual user ID
        self.master.destroy()
        self.open_main_window(user_id)

    def open_main_window(self, user_id):
        root = Tk()
        app = MainWindow(root, user_id)
        root.mainloop()


if __name__ == '__main__':
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()

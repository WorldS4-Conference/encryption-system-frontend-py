from tkinter import *
from client import *
from constants import *


def open_main_window(user_id):
    # self.master.destroy()
    root = Tk()
    Client(root, user_id)
    root.mainloop()


class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.resizable(False, False)
        self.master.title("Login")
        self.master.geometry("350x450")

        # Set background color and font
        self.master.configure(bg="white")
        self.font = ("Helvetica", 12)

        # Create title label
        self.title_label = ttk.Label(self.master, text='CipherHorizon', style="Title.TLabel")
        self.title_label.pack(fill=X, padx=10, pady=10)

        # Create labels and entries
        self.label_username = ttk.Label(self.master, text="Email", font=self.font, style="Label.TLabel")
        self.label_password = ttk.Label(self.master, text="Password", font=self.font, style="Label.TLabel")

        self.entry_username = ttk.Entry(self.master, font=self.font)
        self.entry_password = ttk.Entry(self.master, show="*", font=self.font)

        # Create checkbox and button
        style = ttk.Style()
        style.configure("TCheckbutton", font=self.font)
        style.configure("TCheckbutton", background="white")
        self.checkbutton = ttk.Checkbutton(self.master, text="Keep me logged in", style="TCheckbutton")
        self.login_button = ttk.Button(self.master, text="Login", command=self.login, style="Accent.TButton")

        # Set pack layout
        self.label_username.pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_username.pack(side=TOP, padx=10, pady=10, fill=X)
        self.label_password.pack(side=TOP, padx=10, pady=10, fill=X)
        self.entry_password.pack(side=TOP, padx=10, pady=10, fill=X)
        self.checkbutton.pack(side=TOP, padx=10, pady=10, fill=X)
        self.login_button.pack(side=TOP, padx=10, pady=10, fill=X)

        # Create a label to display error messages
        self.error_label = ttk.Label(master, foreground="red", background="white")
        self.error_label.pack(side=TOP, padx=10, pady=10, fill=X)

        # Style the button
        style.configure("Accent.TButton", background="#1E90FF", foreground="#fff", font=self.font, width=15, pady=6)

        # Style the labels
        style.configure("Label.TLabel", background="white")
        style.configure("Title.TLabel", background="light yellow", font=("Helvetica", 18, "italic", "bold"))
        self.title_label.pack(fill=X, padx=0, pady=10, expand=True)
        self.title_label.configure(anchor=CENTER)

    def login(self):
        # Get the username and password from the Entry widgets
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if the username and password fields are filled
        if not username:
            self.error_label.configure(text="Error, " + "Please enter a username.")
            return
        elif not password:
            self.error_label.configure(text="Error, " + "Please enter a password.")
            return

        # TODO: Add code to authenticate the user with the provided username and password
        login_url = 'http://127.0.0.1:8000/api/login/'
        data = {'email': username, 'password': password}
        response = requests.post(login_url, data=data)
        if response.status_code == 200:
            # Login successful
            auth_token = response.json()['auth_token']
            # Display a message indicating that the user has successfully logged in
            self.error_label.configure(text="Success, " + "You have successfully logged in.")

            # Perform login validation
            self.master.destroy()
            open_main_window(username)
            # Do something with the auth_token, such as store it for future requests
        else:
            # Login failed
            # reponse  = (response.json())
            # print(response)
            self.error_label.configure(text=response.json()['message'])

            print('Login failed. Status code:', response.status_code)




if __name__ == '__main__':
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()

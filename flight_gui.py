from tkinter import *
from tkinter import messagebox

from data_manager import DataManager
from notification_manager import NotificationManager

FONT = ("Courier", 14, "bold")
ROW = 1


def is_valid(data: list) -> bool:
    """
    User input validation.
    :return:
    """
    for item in data:
        if item is None or item == '':
            messagebox.showwarning(title="Oops", message="Don't leave any fields empty.")
            return False

    if '@' not in data[2]:
        messagebox.showwarning(title="Oops", message="Invalid email address.")
        return False

    return True


class FlightGUI:

    def __init__(self, data_manager: DataManager, notification_manager: NotificationManager, flight_objects: list):
        # Attributes:
        self.data_manager = data_manager
        self.notification_manager = notification_manager
        self.flights = flight_objects

        # ----------------------- UI SETUP -----------------------

        window = Tk()
        window.title("Flight Finder")
        window.config(padx=50, pady=50)

        canvas = Canvas(width=400, height=400, highlightthickness=0)
        logo_img = PhotoImage(file="logo.png")
        canvas.create_image(100, 100, image=logo_img)
        # canvas.pack()
        canvas.grid(column=0, row=0, columnspan=2)

        # ------------- LABELS -------------------

        first_label = Label(text="First Name:", font=FONT)
        first_label.grid(column=0, row=ROW, sticky=W)

        last_label = Label(text="Last Name:", font=FONT)
        last_label.grid(column=0, row=ROW + 1, sticky=W)

        email_label = Label(text="Email:", font=FONT)
        email_label.grid(column=0, row=ROW + 2, sticky=W)

        # ---------- ENTRIES -------------

        self.first_entry = Entry(width=21)
        self.first_entry.focus()
        self.first_entry.grid(column=1, row=ROW, sticky=W)

        self.last_entry = Entry(width=21)
        self.last_entry.grid(column=1, row=ROW + 1, sticky=W)

        self.email_entry = Entry(width=35)
        self.email_entry.insert(0, "danielmakmal14@gmail.com")
        self.email_entry.grid(column=1, row=ROW + 2, sticky=W)

        # -------------- BUTTONS -------------------

        self.add_button = Button(text="Add User", width=10, command=self.add_user)
        self.add_button.grid(column=0, row=ROW + 4, )

        self.send_button = Button(text="Send", width=10, command=self.send)
        self.send_button.grid(column=0, row=ROW + 5)

        window.mainloop()

    def add_user(self):
        """
        To Google spreadsheet.
        :return:
        """
        first_name = self.first_entry.get()
        last_name = self.last_entry.get()
        email = self.email_entry.get()

        data = [first_name, last_name, email]

        if is_valid(data):
            if self.data_manager.add_row(first_name, last_name, email):
                messagebox.showinfo(title="Success",
                                    message=f"User {first_name} {last_name}\n"
                                            f"at {email},\n"
                                            f"was successfully added.")
            else:
                messagebox.showwarning(title="Sorry...",
                                       message="We were unsuccessful in adding your account.")

    def send(self):
        """
        Sends notification to all registered emails (regarding flight prices).
        :return:
        """
        users_data = self.data_manager.get_users_data()
        for entry in users_data:
            self.notification_manager.send_email(recipient_email=entry['email'],
                                                 sbj="Low Flight Prices Alert!",
                                                 msg=self.create_message())

    def create_message(self) -> str:
        """
        Constructs the text that will be sent via email.
        :return:
        """
        message = ""
        for flight in self.flights:
            if flight.prices['current'] <= flight.prices['lowest']:
                # Cheaper than usual.
                message += (f"\nFly from: {flight.dep}-{flight.codes['dep_city']}\n"
                            f"To: {flight.dest}-{flight.codes['dest_city']}"
                            f"\n\nDeparture Dates:\n"
                            f"From - {flight.dates['first']}\n"
                            f"To - {flight.dates['last']}"
                            f"\n\nFor only: {flight.prices}\n"
                            f"-----------------------------------")
                if flight.stop_overs > 0:
                    message += f"There are {flight.stop_overs} along the way."
        if message == "":
            message += "No cheap flight price deals found..."

        return message

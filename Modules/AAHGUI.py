import Class
from tkinter import *


class AccountFrame:
    account_frame = Frame
    email_entry = Entry
    password_entry = Entry
    label = Label
    button = Button
    clicks_label = Label

    account_class = Class.Player

    clicks_done = 0
    after_id = 0
    email = ""
    password = ""
    working = False

    def __init__(self):
        self.account_frame = Frame(root)
        self.email_entry = Entry(self.account_frame)
        self.password_entry = Entry(self.account_frame)
        self.button = Button(self.account_frame, text="Вперед:)")
        self.button.bind("<Button-1>", self.button_clicked)
        self.label = Label(self.account_frame, width=100)
        self.clicks_label = Label(self.account_frame, text="Мною тыкнуто: 0", width=15)
        self.clicks_label.grid(row=0, column=0)
        self.email_entry.grid(row=0, column=1)
        self.password_entry.grid(row=0, column=2)
        self.button.grid(row=0, column=3)
        self.label.grid(row=0, column=4)
        self.account_frame.pack()

    def read_entries(self):
        self.email = self.email_entry.get()
        self.password = self.password_entry.get()

    def make_help(self):
        return self.account_class.gui_make_help()

    def enter_account(self):
        return self.account_class.gui_enter_account()

    def start(self, relogin=False):
        if relogin:
            self.enter_account()
        help_result = self.make_help()
        if help_result[0]:
            self.change_text_to("Помог, жду 20 мин...")
            self.update_clicks_amount()
            ms_to_w8 = 20 * 60 * 1000
            relogin = False
        else:
            self.change_text_to(help_result[1])
            ms_to_w8 = 10 * 1000
            relogin = True
        self.after_id = self.account_frame.after(ms_to_w8, self.start, relogin)

    def stop(self):
        self.account_frame.after_cancel(self.after_id)
        self.working = False
        self.clicks_done = 0
        self.change_button_text_to(0)  # Начать
        self.change_text_to("")

    def check(self):
        enter_result = self.enter_account()
        if enter_result[0]:
            help_result = self.make_help()
            if help_result[0]:
                self.change_text_to("Помог, жду 20 мин...")
                self.update_clicks_amount()
                self.change_button_text_to(0)
            return help_result
        else:
            return enter_result

    def button_clicked(self, event):
        self.read_entries()
        self.account_class = Class.Player(self.email, self.password)
        if not self.working:
            result = self.check()
            if result[0]:  # if everything is correct - start repeating
                self.after_id = self.account_frame.after(20 * 60 * 1000, self.start)
            else:  # tell an error
                self.change_text_to(result[1])
        else:  # if was working
            self.stop()

    def change_text_to(self, text):
        self.label.config(text=text)

    def change_button_text_to(self, text_id):
        text = ["Начать", "Остановить"]
        self.button.config(text=text[text_id])

    def update_clicks_amount(self):
        self.clicks_done += 1
        self.clicks_label.config(text="Мною тыкнуто: " + str(self.clicks_done))

root = Tk()
root.geometry('{}x{}'.format(root.winfo_screenwidth(), 300))
root.title("Сказочный тыкобот:)")
for i in range(0, 10):
    AccountFrame()
root.mainloop()

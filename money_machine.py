from tkinter import messagebox

class MoneyMachine:

    CURRENCY = "$"

    COIN_VALUES = {
        "quarters": 0.25,
        "dimes": 0.10,
        "nickles": 0.05,
        "pennies": 0.01
    }

    def __init__(self):
        self.profit = 0
        self.money_received = 0

    def report(self):
        """Prints the current profit"""
        messagebox.showinfo("Profit Report", f"Money: {self.CURRENCY}{self.profit}")


    def make_payment(self, cost):
        """Returns True when payment is accepted, or False if insufficient. """


        if self.money_received >= cost:
            change = round(self.money_received - cost, 2)
            messagebox.showinfo("Change", f"Here is {self.CURRENCY}{change} in change.")
            self.profit += change
            return True
        else:
            messagebox.showerror("Payment Error", "Sorry, that's not enough money. Money refunded.")
            self.money_received = 0
            return False
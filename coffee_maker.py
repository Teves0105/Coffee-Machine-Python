from tkinter import messagebox

class CoffeeMaker:
    """Models the machine that makes the coffee"""
    def __init__(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }

    def report(self):
        """Prints a report of all resources."""
        report_message = (
            f"Water: {self.resources['water']}ml\n"
            f"Milk: {self.resources['milk']}ml\n"
            f"Coffee: {self.resources['coffee']}ml"
        )
        messagebox.showinfo("Resource Report", report_message)

    def is_resource_sufficient(self, drink):
        """Return True when order can be made, False if ingredients are insufficient."""
        can_make = True
        for item in drink.ingredients:
            if drink.ingredients[item] > self.resources[item]:
                messagebox.showerror("Insufficient Resources", f"Sorry, there is not enough {item}.")
                can_make = False
        return can_make

    def make_coffee(self, order):
        """Deducts the required ingredients from the resources."""
        for item in order.ingredients:
            self.resources[item] -= order.ingredients[item]

    def refill(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
        }
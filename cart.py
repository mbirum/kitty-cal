from tkinter import *

class CartFrame(Frame):
    def __init__(self, cart, master=None):
        super().__init__(master, bg="#99B898")
        self.master = master
        self.cart = cart
        self.create_widgets()

    def create_widgets(self):
        self.cart_label = Label(self, text="Cart", font="Verdana 20 bold")
        self.cart_label.pack(pady=10)

        self.confirm_button = Button(self, text="Confirm", command=self.confirm_cart)
        self.confirm_button.pack(pady=10)

    def confirm_cart(self):
        print("Checking out cart...")
        self.master.load_calories_today()
        for item, quantity in self.cart.items():
            if item in self.master.calories_today:
                self.master.calories_today[item] += quantity
                if item == "wet_quantity":
                    self.master.calories_today["wet_cal"] += int(quantity * self.master.wet_cal_per_gram)
                elif item == "dry_quantity":
                    self.master.calories_today["dry_cal"] += int(quantity * self.master.dry_cal_per_cup)
                elif item == "minnow_quantity":
                    self.master.calories_today["minnow_cal"] += int(quantity * self.master.minnow_cal_per_unit)
                elif item == "egg_quantity":
                    self.master.calories_today["egg_cal"] += int(quantity * self.master.egg_cal_per_unit)
                elif item == "giblet_quantity":
                    self.master.calories_today["giblet_cal"] += int(quantity * self.master.giblet_cal_per_unit)
        self.cart_label.config(text="Saving...")
        self.master.save_calories_today()
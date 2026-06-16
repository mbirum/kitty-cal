#!/usr/bin/python	
from tkinter import *
from datetime import date
from cart import CartFrame
from home import HomeFrame
import subprocess
import os

class KittyCalApp(Tk):

    wet_default_quantity = 50
    wet_cal_per_gram = 0.6

    dry_cal_per_cup = 120
    dry_default_quantity = 1

    minnow_cal_per_unit = 2
    minnow_default_quantity = 5

    egg_cal_per_unit = 10
    egg_default_quantity = 1

    giblet_cal_per_unit = 2
    giblet_default_quantity = 1

    bova_needed_per_day = 2
    drop_needed_per_day = 4
    nausea_needed_per_day = 1

    cart = {}

    def __init__(self):
        super().__init__()
        self.wm_title("KittyCal")
        self.attributes("-fullscreen", True)
        self.get_initial_calories()
        self.load_calories_today()
        self.home_frame = HomeFrame(self)
        self.home_frame.pack(fill=BOTH, expand=True)

    def get_initial_calories(self):
        print("Initializing calories for today...")
        self.calories_today = {
            "wet_cal": 0,
            "wet_quantity": 0,
            "dry_cal": 0,
            "dry_quantity": 0,
            "minnow_cal": 0,
            "minnow_quantity": 0,
            "egg_cal": 0,
            "egg_quantity": 0,
            "giblet_cal": 0,
            "giblet_quantity": 0,
            "bova_taken": 0,
            "drops_taken": 0,
            "nausea_taken": 0
        }
        return self.calories_today


    def load_calories_today(self):
        print("Loading calories for today...")
        self.log_file_path = f"log/{date.today()}.txt"
        subprocess.run(["./gitpull.sh"], check=True)
        if os.path.exists(self.log_file_path):
            with open(self.log_file_path, "r") as f:
                for line in f:
                    item, value = line.strip().split("=")
                    self.calories_today[item] = int(value)
        else:
            with open(self.log_file_path, "w") as f:
                for item, value in self.calories_today.items():
                    f.write(f"{item}={value}\n")

    def save_calories_today(self):
        print("Saving calories for today...")
        with open(self.log_file_path, "w") as f:
            for item, value in self.calories_today.items():
                f.write(f"{item}={int(value)}\n")
        subprocess.run(["./gitpush.sh"], check=True)
        self.home_frame.update_total_calories_label()


    def add_to_cart(self, item, quantity):
        print(f"Adding {item} to cart...")
        if item in self.cart:
            self.cart[item] += quantity
        else:
            self.cart[item] = quantity

    def get_total_calories(self):
        print("Calculating total calories...")
        total_calories = (self.calories_today["wet_cal"] + self.calories_today["dry_cal"] +
                        self.calories_today["minnow_cal"] + self.calories_today["egg_cal"] +
                        self.calories_today["giblet_cal"])
        return total_calories
        
    def checkout_cart(self):
        self.home_frame.destroy()
        self.cart_frame = CartFrame(self.cart, self)
        self.cart_frame.pack(fill=BOTH, expand=True)
        
    # we can exit when we press the escape key
    def end_fullscreen(self, event):
        self.attributes("-fullscreen", False)


if __name__ == "__main__":
    app = KittyCalApp()
    app.mainloop()
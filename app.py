#!/usr/bin/python	
from tkinter import *
from datetime import date
import subprocess
import os

root = Tk()
root.wm_title("KittyCal")
root.configure(bg="#99B898")
root.attributes("-fullscreen", True)

today = date.today()
log_file_path = f'log/{today}.txt'

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

print("Initializing calories for today...")
calories_today = {
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

cart = {}

def load_calories_today():
    print("Loading calories for today...")
    subprocess.run(["./gitpull.sh"], check=True)
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as f:
            for line in f:
                item, value = line.strip().split("=")
                calories_today[item] = int(value)
    else:
        with open(log_file_path, "w") as f:
            for item, value in calories_today.items():
                f.write(f"{item}={value}\n")

def save_calories_today():
    print("Saving calories for today...")
    with open(log_file_path, "w") as f:
        for item, value in calories_today.items():
            f.write(f"{item}={value}\n")
    subprocess.run(["./gitpush.sh"], check=True)

def add_to_cart(item, quantity):
    print(f"Adding {quantity} {item} to cart...")
    if item in cart:
        cart[item] += quantity
    else:
        cart[item] = quantity

def checkout_cart():
    print("Checking out cart...")
    for item, quantity in cart.items():
        if item in calories_today:
            calories_today[item] += quantity
            if item == "wet_quantity":
                calories_today["wet_cal"] += quantity * wet_cal_per_gram
            elif item == "dry_quantity":
                calories_today["dry_cal"] += quantity * dry_cal_per_cup
            elif item == "minnow_quantity":
                calories_today["minnow_cal"] += quantity * minnow_cal_per_unit
            elif item == "egg_quantity":
                calories_today["egg_cal"] += quantity * egg_cal_per_unit
            elif item == "giblet_quantity":
                calories_today["giblet_cal"] += quantity * giblet_cal_per_unit
    save_calories_today()

def get_total_calories():
    print("Calculating total calories...")
    total_calories = (calories_today["wet_cal"] + calories_today["dry_cal"] +
                      calories_today["minnow_cal"] + calories_today["egg_cal"] +
                      calories_today["giblet_cal"])
    return total_calories

def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


load_calories_today()

label_header = Label(root, text="Junie Birum", font="Verdana 26 bold",
			fg="#000",
			bg="#99B898",
			pady = 60,
			padx = 100)

total_calories_label = Label(root, text=f"{get_total_calories()} Total Calories Today", font="Verdana 20 bold",
            fg="#000",
            bg="#99B898",
            pady = 20,
            padx = 100)

exitButton = Button(root, text="Exit", background = "#C06C84",
      command=btnExit, height=10, width=40, font = "Arial 16 bold")
	
wetFoodButton = Button(root, text="Wet Food", background = "#C06C84",
      command=lambda: add_to_cart("wet_quantity", wet_default_quantity), height=10, width=40, font = "Arial 16 bold")

checkoutButton = Button(root, text="Checkout", background = "#C06C84",
      command=checkout_cart, height=10, width=40, font = "Arial 16 bold")

label_header.grid(row=0, column=0)
total_calories_label.grid(row=1, column=0)
wetFoodButton.grid(row = 2 ,column =1)
exitButton.grid(row = 2 ,column = 0)
checkoutButton.grid(row = 3 ,column = 0)
root.bind("<Escape>", end_fullscreen)

root.mainloop()
#!/usr/bin/python
from tkinter import *
from tkinter import ttk
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
    minnow_default_quantity = 1

    egg_cal_per_unit = 10
    egg_default_quantity = 1

    giblet_cal_per_unit = 2
    giblet_default_quantity = 1

    # New items
    churu_cal_per_tube = 6
    churu_default_quantity = 0.5

    greenie_cal_per_unit = 1.5
    greenie_default_quantity = 1

    bova_needed_per_day = 2
    drop_needed_per_day = 4
    nausea_needed_per_day = 1

    cart = {}

    def __init__(self):
        super().__init__()
        self.wm_title("KittyCal")
        # self.geometry("1000x800")
        # Set fullscreen after window creation; on some platforms (macOS)
        # toggling fullscreen is more reliable after the window is mapped.
        # We'll also re-assert fullscreen shortly after startup.
        self.attributes("-fullscreen", True)
        self.configure(bg="#0f1419")
        
        # Configure custom ttk styles
        self.configure_styles()
        
        self.get_initial_calories()
        self.load_calories_today()
        self.home_frame = HomeFrame(self)
        self.home_frame.pack(fill=BOTH, expand=True)

        # Re-assert fullscreen after the UI is mapped (helps on macOS)
        try:
            self.after(100, lambda: self.attributes("-fullscreen", True))
        except Exception:
            pass
    
    def configure_styles(self):
        """Configure modern ttk styles with custom colors"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define color palette
        bg_dark = "#0f1419"
        bg_light = "#1a2332"
        accent_primary = "#ff6b9d"
        accent_secondary = "#a78bfa"
        text_primary = "#ffffff"
        text_secondary = "#b0b9c1"
        
        # Configure frame background
        style.configure('TFrame', background=bg_dark)
        style.configure('Card.TFrame', background=bg_light, relief='solid', borderwidth=1)
        
        # Configure labels
        style.configure('TLabel', background=bg_dark, foreground=text_primary, font=('Helvetica', 13))
        style.configure('Header.TLabel', background=bg_dark, foreground=text_primary, font=('Helvetica', 32, 'bold'))
        style.configure('Subheader.TLabel', background=bg_dark, foreground=text_secondary, font=('Helvetica', 16))
        style.configure('CartCal.TLabel', background=bg_dark, foreground=text_secondary, font=('Helvetica', 13))
        style.configure('Card.TLabel', background=bg_light, foreground=text_primary, font=('Helvetica', 13))
        
        # Configure buttons
        style.configure('Primary.TButton', font=('Helvetica', 12, 'bold'), padding=20)
        style.map('Primary.TButton',
                  background=[('pressed', accent_secondary), ('active', accent_primary)],
                  foreground=[('pressed', bg_dark), ('active', bg_dark)])
        
        style.configure('Accent.TButton', font=('Helvetica', 12, 'bold'), padding=20)
        style.map('Accent.TButton',
                  background=[('pressed', '#ff4d85'), ('active', accent_primary)],
                  foreground=[('pressed', text_primary), ('active', text_primary)])

        style.configure('NarrowAccent.TButton', font=('Helvetica', 14, 'bold'), padding=15)
        style.map('NarrowAccent.TButton',
                  background=[('pressed', '#ff4d85'), ('active', accent_primary)],
                  foreground=[('pressed', text_primary), ('active', text_primary)])

        # Smaller button style for compact footer actions
        style.configure('Small.TButton', font=('Helvetica', 12), padding=6)
        style.map('Small.TButton',
              background=[('pressed', '#ff4d85'), ('active', accent_primary)],
              foreground=[('pressed', text_primary), ('active', text_primary)])
        
        # Configure separator
        style.configure('TSeparator', background=bg_light)

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
            "churu_cal": 0,
            "churu_quantity": 0,
            "greenie_cal": 0,
            "greenie_quantity": 0,
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
                    if item == "weight":
                        self.calories_today[item] = float(value)
                    else:
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
        self.cart = {}
        self.restore_home_frame()


    def add_to_cart(self, item, quantity):
        print(f"Adding {item} to cart...")
        if item in self.cart:
            self.cart[item] += quantity
        else:
            self.cart[item] = quantity
        # Update home frame cart display
        if hasattr(self, 'home_frame') and self.home_frame.winfo_exists():
            self.home_frame.update_cart_display()
    
    def get_cart_icon_map(self):
        """Return mapping of cart item names to icons"""
        return {
            "wet_quantity": "🍣",
            "dry_quantity": "🧆",
            "minnow_quantity": "🐟",
            "egg_quantity": "🥚",
            "giblet_quantity": "🦴",
            "churu_quantity": "🧴",
            "greenie_quantity": "🟢",
            "bova_taken": "💊",
            "drops_taken": "💧",
            "nausea_taken": "🤢"
        }

    def get_total_calories(self):
        print("Calculating total calories...")
        total_calories = (self.calories_today["wet_cal"] + self.calories_today["dry_cal"] +
                        self.calories_today["minnow_cal"] + self.calories_today["egg_cal"] +
                        self.calories_today["giblet_cal"] +
                        self.calories_today["churu_cal"] +
                        self.calories_today["greenie_cal"])
        return total_calories
        
    def checkout_cart(self):
        self.home_frame.destroy()
        self.cart_frame = CartFrame(self.cart, self)
        self.cart_frame.pack(fill=BOTH, expand=True)

    def restore_home_frame(self):
        self.cart_frame.destroy()
        self.home_frame = HomeFrame(self)
        self.home_frame.pack(fill=BOTH, expand=True)


if __name__ == "__main__":
    app = KittyCalApp()
    app.mainloop()
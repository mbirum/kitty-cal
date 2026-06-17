from tkinter import *
from tkinter import ttk

class CartFrame(ttk.Frame):
    def __init__(self, cart, master=None):
        super().__init__(master)
        self.master = master
        self.cart = cart
        self.create_widgets()

    def create_widgets(self):
        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill=BOTH, expand=True, padx=40, pady=40)
        
        # Header
        header = ttk.Label(main_container, text="🛒 Order Summary", style='Header.TLabel')
        header.pack(pady=(0, 30))
        
        # Separator
        sep1 = ttk.Separator(main_container, orient=HORIZONTAL)
        sep1.pack(fill=X, pady=(0, 20))
        
        # Cart items
        items_frame = ttk.Frame(main_container, style='Card.TFrame')
        items_frame.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        if not self.cart.items():
            empty_label = ttk.Label(items_frame, text="Your cart is empty", style='Card.TLabel')
            empty_label.pack(pady=20, padx=20)
        else:
            item_labels_frame = ttk.Frame(items_frame)
            item_labels_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
            
            for item, quantity in self.cart.items():
                item_row = ttk.Frame(item_labels_frame)
                item_row.pack(fill=X, pady=8)
                
                item_name = ttk.Label(item_row, text=f"{item}", style='Card.TLabel')
                item_name.pack(side=LEFT)
                
                item_qty = ttk.Label(item_row, text=f"× {quantity}", style='Subheader.TLabel')
                item_qty.pack(side=RIGHT)
        
        # Separator
        sep2 = ttk.Separator(main_container, orient=HORIZONTAL)
        sep2.pack(fill=X, pady=(0, 20))
        
        # Confirm button
        self.confirm_button = ttk.Button(main_container, text="✓ Confirm Order", 
            command=self.confirm_cart, style='Accent.TButton')
        self.confirm_button.pack(fill=X, pady=10)
        
        # Back button
        self.back_button = ttk.Button(main_container, text="← Back", 
            command=self.go_back, style='Primary.TButton')
        self.back_button.pack(fill=X)
        
        # Status label
        self.cart_label = ttk.Label(main_container, text="", style='Subheader.TLabel')
        self.cart_label.pack(pady=20)
    
    def go_back(self):
        """Return to home frame without saving"""
        self.master.restore_home_frame()

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
        self.cart_label.config(text="✓ Saving order...")
        self.cart_label.update()
        self.master.save_calories_today()
from tkinter import *
from tkinter import ttk

class HomeFrame(ttk.Frame):    

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        # Ensure cart display reflects current app cart when frame is created
        try:
            self.update_cart_display()
        except Exception:
            pass

    def create_widgets(self):
        # Main container with minimal padding for small screen
        main_container = ttk.Frame(self)
        main_container.pack(fill=BOTH, expand=True, padx=8, pady=8)
        
        # Header: compact name + calories in one row
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=X, pady=(0, 8))

        self.label_header = ttk.Label(header_frame, text="Junie Birum", style='Header.TLabel')
        self.label_header.pack(side=LEFT, padx=(0, 10))
        
        # Calories display inline with header
        self.total_calories_label = ttk.Label(header_frame, 
            text=f"{self.master.get_total_calories()} kcal", 
            style='Subheader.TLabel')
        self.total_calories_label.pack(side=RIGHT)

        # Cart display section - compact
        cart_frame = ttk.Frame(main_container, style='Card.TFrame')
        cart_frame.pack(fill=X, pady=(0, 8))
        
        cart_label = ttk.Label(cart_frame, text="Cart:", style='Subheader.TLabel')
        cart_label.pack(side=LEFT, padx=8, pady=6)
        
        self.cart_display = ttk.Label(cart_frame, text="(empty)", style='Card.TLabel')
        self.cart_display.pack(side=LEFT, padx=8, pady=6, fill=X, expand=True)
        
        # Scrollable options area
        canvas = Canvas(main_container, bg="#0f1419", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True, pady=(0, 8))
        scrollbar.pack(side=RIGHT, fill=Y)
        
        # Food options section
        food_label = ttk.Label(scrollable_frame, text="FOOD", style='Subheader.TLabel')
        food_label.pack(pady=(10, 6), padx=4)
        
        # Food buttons in 2-column layout
        food_frame = ttk.Frame(scrollable_frame)
        food_frame.pack(fill=X, padx=4, pady=(0, 8))
        
        # Wet Food Button
        self.wetFoodButton = ttk.Button(food_frame, text="🍖 Wet Food", 
            command=lambda: self.master.add_to_cart("wet_quantity", self.master.wet_default_quantity),
            style='Accent.TButton')
        self.wetFoodButton.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=4)
        
        # Dry Food Button
        self.dryFoodButton = ttk.Button(food_frame, text="🌾 Dry Food",
            command=lambda: self.master.add_to_cart("dry_quantity", self.master.dry_default_quantity),
            style='Accent.TButton')
        self.dryFoodButton.pack(side=LEFT, fill=BOTH, expand=True, padx=2, pady=4)
        
        # Extras section
        extras_label = ttk.Label(scrollable_frame, text="EXTRAS", style='Subheader.TLabel')
        extras_label.pack(pady=(12, 6), padx=4)
        
        # Extras in 2-column grid layout
        extras_row1 = ttk.Frame(scrollable_frame)
        extras_row1.pack(fill=X, padx=4, pady=(0, 4))
        
        # Minnow button
        minnow_btn = ttk.Button(extras_row1, text="🐟 Minnow",
            command=lambda: self.add_extra_item("minnow_quantity"),
            style='Accent.TButton')
        minnow_btn.pack(side=LEFT, fill=BOTH, expand=True, padx=2)
        
        # Egg button
        egg_btn = ttk.Button(extras_row1, text="🥚 Egg",
            command=lambda: self.add_extra_item("egg_quantity"),
            style='Accent.TButton')
        egg_btn.pack(side=LEFT, fill=BOTH, expand=True, padx=2)
        
        # Giblet button takes full width on second row
        giblet_btn = ttk.Button(scrollable_frame, text="🦴 Giblet",
            command=lambda: self.add_extra_item("giblet_quantity"),
            style='Accent.TButton')
        giblet_btn.pack(fill=X, padx=4, pady=(0, 8))
        
        # Medicines section
        medicines_label = ttk.Label(scrollable_frame, text="MEDICINES", style='Subheader.TLabel')
        medicines_label.pack(pady=(12, 6), padx=4)
        
        # Medicines in 2-column grid layout
        medicines_row1 = ttk.Frame(scrollable_frame)
        medicines_row1.pack(fill=X, padx=4, pady=(0, 4))
        
        # Bova button
        bova_btn = ttk.Button(medicines_row1, text="💊 Bova",
            command=lambda: self.add_medicine("bova_taken"),
            style='Accent.TButton')
        bova_btn.pack(side=LEFT, fill=BOTH, expand=True, padx=2)
        
        # Drops button
        drops_btn = ttk.Button(medicines_row1, text="💧 Drops",
            command=lambda: self.add_medicine("drops_taken"),
            style='Accent.TButton')
        drops_btn.pack(side=LEFT, fill=BOTH, expand=True, padx=2)
        
        # Nausea Meds button takes full width on second row
        nausea_btn = ttk.Button(scrollable_frame, text="🤢 Nausea Meds",
            command=lambda: self.add_medicine("nausea_taken"),
            style='Accent.TButton')
        nausea_btn.pack(fill=X, padx=4, pady=(0, 8))
        
        # Footer with compact action buttons: small Exit to left of Checkout
        footer_frame = ttk.Frame(main_container)
        footer_frame.pack(fill=X, pady=(0, 0))

        # Button container aligned to the right so actions don't span full width
        button_frame = ttk.Frame(footer_frame)
        button_frame.pack(side=RIGHT, padx=4, pady=4)

        # Exit button to the left of Checkout (small)
        self.exitButton = ttk.Button(button_frame, text="EXIT",
            command=self.master.quit, style='Small.TButton', width=8)
        self.exitButton.pack(side=RIGHT, padx=(4,0))

        # Checkout button (small) — match Exit button size and style
        self.checkoutButton = ttk.Button(button_frame, text="🛒 CHECKOUT",
            command=self.master.checkout_cart, style='Small.TButton', width=12)
        self.checkoutButton.pack(side=RIGHT, padx=(0,4))

    
    def update_cart_display(self):
        """Update the cart display with current items"""
        if not self.master.cart:
            self.cart_display.config(text="(empty)")
        else:
            icon_map = self.master.get_cart_icon_map()
            cart_items = []
            for item, quantity in self.master.cart.items():
                icon = icon_map.get(item, "")
                cart_items.append(f"{icon} {quantity}x")
            display_text = "  ".join(cart_items)
            self.cart_display.config(text=display_text)
    
    def add_extra_item(self, item):
        """Handle extra item additions"""
        if item == "minnow_quantity":
            self.master.add_to_cart(item, self.master.minnow_default_quantity)
        elif item == "egg_quantity":
            self.master.add_to_cart(item, self.master.egg_default_quantity)
        elif item == "giblet_quantity":
            self.master.add_to_cart(item, self.master.giblet_default_quantity)
    
    def add_medicine(self, item):
        """Handle medicine additions"""
        self.master.add_to_cart(item, 1)


    def update_total_calories_label(self):
        self.total_calories_label.config(text=f"{self.master.get_total_calories()} Total Calories Today")
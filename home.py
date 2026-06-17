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
        # Main container with padding
        main_container = ttk.Frame(self)
        main_container.pack(fill=BOTH, expand=True, padx=40, pady=40)
        
        # Header section
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=X, pady=(0, 30))

        self.label_header = ttk.Label(header_frame, text="Junie Birum", style='Header.TLabel')
        self.label_header.pack(side=LEFT, padx=(0, 20))

       # Calories display card
        calories_frame = ttk.Frame(main_container, style='Card.TFrame')
        calories_frame.pack(fill=X, pady=(0, 10))
        
        self.total_calories_label = ttk.Label(calories_frame, 
            text=f"{self.master.get_total_calories()} Total Calories Today", 
            style='Subheader.TLabel')
        self.total_calories_label.pack(pady=5, padx=5)

        # Cart display section
        cart_frame = ttk.Frame(main_container, style='Card.TFrame')
        cart_frame.pack(fill=X, pady=(0, 20))
        
        cart_label = ttk.Label(cart_frame, text="Cart", style='Subheader.TLabel')
        cart_label.pack(side=LEFT, padx=10, pady=8)
        
        self.cart_display = ttk.Label(cart_frame, text="(empty)", style='Card.TLabel')
        self.cart_display.pack(side=LEFT, padx=10, pady=8, fill=X, expand=True)
        
        # Separator
        separator = ttk.Separator(header_frame, orient=HORIZONTAL)
        separator.pack(side=LEFT, fill=X, expand=True)
        
        # Food options section
        options_frame = ttk.Frame(main_container)
        options_frame.pack(fill=BOTH, expand=True, pady=(0, 30))
        
        # Wet Food Button
        self.wetFoodButton = ttk.Button(options_frame, text="🍖 Wet Food", 
            command=lambda: self.master.add_to_cart("wet_quantity", self.master.wet_default_quantity),
            style='Accent.TButton')
        self.wetFoodButton.pack(fill=X, pady=10)
        
        # Dry Food Button
        self.dryFoodButton = ttk.Button(options_frame, text="🌾 Dry Food",
            command=lambda: self.master.add_to_cart("dry_quantity", self.master.dry_default_quantity),
            style='Accent.TButton')
        self.dryFoodButton.pack(fill=X, pady=10)
        
        # Additional items section
        extras_label = ttk.Label(options_frame, text="Extras", style='Subheader.TLabel')
        extras_label.pack(pady=(20, 10))
        
        extras_frame = ttk.Frame(options_frame)
        extras_frame.pack(fill=X, pady=(0, 20))
        
        # Minnow, Egg, Giblet buttons
        for text, item in [("🐟 Minnow", "minnow_quantity"), ("🥚 Egg", "egg_quantity"), ("🦴 Giblet", "giblet_quantity")]:
            btn = ttk.Button(extras_frame, text=text,
                command=lambda i=item: self.add_extra_item(i),
                style='Primary.TButton')
            btn.pack(fill=X, pady=5)
        
        # Checkout button - footer
        footer_frame = ttk.Frame(main_container)
        footer_frame.pack(fill=X, pady=(20, 0))
        
        self.checkoutButton = ttk.Button(footer_frame, text="🛒 Checkout",
            command=self.master.checkout_cart, style='Accent.TButton')
        self.checkoutButton.pack(fill=X)
    
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


    def update_total_calories_label(self):
        self.total_calories_label.config(text=f"{self.master.get_total_calories()} Total Calories Today")
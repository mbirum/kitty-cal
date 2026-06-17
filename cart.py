from tkinter import *
from tkinter import ttk

class CartFrame(ttk.Frame):
    def __init__(self, cart, master=None):
        super().__init__(master)
        self.master = master
        self.cart = cart
        self.create_widgets()

    def create_widgets(self):
        # Main container - minimal padding for small screen
        main_container = ttk.Frame(self)
        main_container.pack(fill=BOTH, expand=True, padx=8, pady=8)
        
        # Header
        header = ttk.Label(main_container, text="🛒 ORDER SUMMARY", style='Header.TLabel')
        header.pack(pady=(0, 8))
        
        # Cart items with scrolling
        items_frame = ttk.Frame(main_container, style='Card.TFrame')
        items_frame.pack(fill=BOTH, expand=True, pady=(0, 8))
        # expose for updates when quantities change
        self.items_frame = items_frame

        # Initialize item widget refs map
        self.item_widgets = {}
        
        if not self.cart.items():
            empty_label = ttk.Label(items_frame, text="Your cart is empty", style='Card.TLabel')
            empty_label.pack(pady=20, padx=20)
        else:
            # Scrollable items area
            canvas = Canvas(items_frame, bg="#1a2332", highlightthickness=0)
            scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
            
            item_labels_frame = ttk.Frame(canvas, style='Card.TFrame')
            item_labels_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=item_labels_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side=LEFT, fill=BOTH, expand=True)
            scrollbar.pack(side=RIGHT, fill=Y)

            # Human readable name and calorie calculation map
            readable_map = {
                "wet_quantity": ("Wet Food", lambda q, m: int(q * getattr(m, 'wet_cal_per_gram', 0))),
                "dry_quantity": ("Dry Food", lambda q, m: int(q * getattr(m, 'dry_cal_per_cup', 0))),
                "minnow_quantity": ("Minnow", lambda q, m: int(q * getattr(m, 'minnow_cal_per_unit', 0))),
                "egg_quantity": ("Egg", lambda q, m: int(q * getattr(m, 'egg_cal_per_unit', 0))),
                "giblet_quantity": ("Giblet", lambda q, m: int(q * getattr(m, 'giblet_cal_per_unit', 0))),
                "bova_taken": ("Bova", lambda q, m: 0),
                "drops_taken": ("Drops", lambda q, m: 0),
                "nausea_taken": ("Nausea Meds", lambda q, m: 0)
            }

            icon_map = {}
            if hasattr(self.master, 'get_cart_icon_map'):
                icon_map = self.master.get_cart_icon_map()

            # Keep references to widgets so we can update them when quantities change
            self.item_widgets = {}

            for item, quantity in self.cart.items():
                item_row = ttk.Frame(item_labels_frame)
                item_row.pack(fill=X, pady=6, padx=4)

                name, calc = readable_map.get(item, (item, lambda q, m: 0))
                icon = icon_map.get(item, "")

                # Left: icon + readable name
                left_text = f"{icon} {name}"
                left_label = ttk.Label(item_row, text=left_text, style='Card.TLabel')
                # make the name expand so the row uses the full width
                left_label.pack(side=LEFT, fill=X, expand=True)

                # Right side: calories (if any) and quantity controls
                right_frame = ttk.Frame(item_row)
                right_frame.pack(side=RIGHT)

                # Calculated calories label (only for food items)
                calories = calc(quantity, self.master)
                if calories > 0:
                    cal_label = ttk.Label(right_frame, text=f"{calories} kcal", style='CartCal.TLabel')
                    cal_label.pack(side=RIGHT, padx=(8,0))
                else:
                    cal_label = None

                # Quantity controls: - [qty] +
                qty_frame = ttk.Frame(right_frame)
                qty_frame.pack(side=RIGHT)

                # Determine increment per item type
                if item == 'wet_quantity':
                    incr = 5
                elif item == 'dry_quantity':
                    incr = 0.5
                else:
                    incr = 1

                # Decrement button (smaller)
                dec_btn = ttk.Button(qty_frame, text='−', width=2,
                    command=lambda i=item, d=-incr: self.adjust_quantity(i, d))
                dec_btn.pack(side=LEFT, padx=(0,2))

                # Quantity label
                def fmt_qty(q):
                    if isinstance(q, float) and not q.is_integer():
                        return f"{q:.1f}x"
                    else:
                        return f"{int(q)}x"

                qty_label = ttk.Label(qty_frame, text=fmt_qty(quantity), style='CartCal.TLabel', width=4, anchor='center')
                qty_label.pack(side=LEFT, padx=2)

                # Increment button (smaller)
                inc_btn = ttk.Button(qty_frame, text='+', width=2,
                    command=lambda i=item, d=incr: self.adjust_quantity(i, d))
                inc_btn.pack(side=LEFT, padx=(2,0))

                # Save widget refs
                self.item_widgets[item] = {
                    'qty_label': qty_label,
                    'cal_label': cal_label,
                    'incr': incr,
                    'row': item_row,
                    'has_calories': calories > 0
                }
        
        # Buttons section - stacked vertically, large for touchscreen
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=X, pady=(0, 0))
        
        # Confirm button
        self.confirm_button = ttk.Button(button_frame, text="✓ CONFIRM", 
            command=self.confirm_cart, style='Accent.TButton')
        self.confirm_button.pack(fill=X, pady=(0, 4))
        
        # Back button
        self.back_button = ttk.Button(button_frame, text="← BACK", 
            command=self.go_back, style='Primary.TButton')
        self.back_button.pack(fill=X)
        
        # Status label
        self.cart_label = ttk.Label(main_container, text="", style='Subheader.TLabel')
        self.cart_label.pack(pady=4)
    
    def go_back(self):
        """Return to home frame without saving"""
        self.master.restore_home_frame()

    def adjust_quantity(self, item, delta):
        """Adjust the quantity for `item` by `delta` and update UI labels."""
        # Ensure item exists
        if item not in self.cart:
            return

        current = self.cart[item]
        # support floats
        new_qty = current + delta

        # Prevent negative quantities
        if new_qty < 0:
            new_qty = 0

        # If increment is integer-like, store as int
        incr = self.item_widgets.get(item, {}).get('incr', 1)
        if isinstance(incr, int) and float(new_qty).is_integer():
            new_qty = int(new_qty)

        self.cart[item] = new_qty

        # Update labels
        widgets = self.item_widgets.get(item)
        if widgets:
            qty_label = widgets['qty_label']
            cal_label = widgets['cal_label']

            # format qty
            if isinstance(new_qty, float) and not float(new_qty).is_integer():
                qty_text = f"{new_qty:.1f}x"
            else:
                qty_text = f"{int(new_qty)}x"
            qty_label.config(text=qty_text)

            # recalc calories using same calc logic as in create_widgets
            # reuse readable_map logic inline
            if item == "wet_quantity":
                calories = int(new_qty * getattr(self.master, 'wet_cal_per_gram', 0))
            elif item == "dry_quantity":
                calories = int(new_qty * getattr(self.master, 'dry_cal_per_cup', 0))
            elif item == "minnow_quantity":
                calories = int(new_qty * getattr(self.master, 'minnow_cal_per_unit', 0))
            elif item == "egg_quantity":
                calories = int(new_qty * getattr(self.master, 'egg_cal_per_unit', 0))
            elif item == "giblet_quantity":
                calories = int(new_qty * getattr(self.master, 'giblet_cal_per_unit', 0))
            else:
                calories = 0

            if cal_label and calories > 0:
                cal_label.config(text=f"{calories} kcal")

        # If quantity dropped to zero, remove the item row and cart entry
        if float(new_qty) == 0:
            # remove from cart data
            try:
                del self.cart[item]
            except Exception:
                pass
            # destroy widgets
            if widgets and 'row' in widgets:
                try:
                    widgets['row'].destroy()
                except Exception:
                    pass
            # remove widget refs
            if item in self.item_widgets:
                try:
                    del self.item_widgets[item]
                except Exception:
                    pass

            # if the cart is now empty, show empty label in items_frame
            if not self.cart:
                for child in list(self.items_frame.winfo_children()):
                    try:
                        child.destroy()
                    except Exception:
                        pass
                empty_label = ttk.Label(self.items_frame, text="Your cart is empty", style='Card.TLabel')
                empty_label.pack(pady=20, padx=20)

        # Update the home frame cart display if present
        if hasattr(self.master, 'home_frame') and hasattr(self.master.home_frame, 'update_cart_display'):
            try:
                self.master.home_frame.update_cart_display()
            except Exception:
                pass

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
                # Medicines don't add calories, just update the quantity directly
                elif item in ["bova_taken", "drops_taken", "nausea_taken"]:
                    pass
        self.cart_label.config(text="✓ Saving order...")
        self.cart_label.update()
        self.master.save_calories_today()
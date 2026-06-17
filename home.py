from tkinter import *

class HomeFrame(Frame):    

    def __init__(self, master=None):
        super().__init__(master, bg="#99B898")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label_header = Label(self, text="Junie Birum", font="Verdana 22 bold",
            fg="#000",
            bg="#99B898",
            pady = 60,
            padx = 100)
        self.label_header.grid(row=0, column=0, columnspan=2)
        

        self.total_calories_label = Label(self, text=f"{self.master.get_total_calories()} Total Calories Today", font="Verdana 26 bold",
            fg="#000",
            bg="#99B898",
            pady = 20,
            padx = 100)
        self.total_calories_label.grid(row=1, column=0, columnspan=2)

        self.j1_image = PhotoImage(file="j1.png")
        
        self.wetFoodButton = Button(self, text="Wet Food", image=self.j1_image, background = "#C06C84",
          command=lambda: self.master.add_to_cart("wet_quantity", self.master.wet_default_quantity), height=5, width=20, font = "Arial 13 bold")
        self.wetFoodButton.grid(row=2, column=0, padx=15, pady=15)

        self.dryFoodButton = Button(self, text="Dry Food", background = "#C06C84",
          command=lambda: self.master.add_to_cart("dry_quantity", self.master.dry_default_quantity), height=5, width=20, font = "Arial 13 bold")
        self.dryFoodButton.grid(row=2, column=1, padx=5, pady=5)

        self.checkoutButton = Button(self, text="Checkout", background = "#C06C84",
          command=self.master.checkout_cart, height=5, width=20, font = "Arial 13 bold")
        self.checkoutButton.grid(row=3, column=12, columnspan=6, padx=5, pady=5)


    def update_total_calories_label(self):
        self.total_calories_label.config(text=f"{self.master.get_total_calories()} Total Calories Today")
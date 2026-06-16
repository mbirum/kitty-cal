from tkinter import *

class HomeFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#99B898")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.label_header = Label(self, text="Junie Birum", font="Verdana 26 bold",
            fg="#000",
            bg="#99B898",
            pady = 60,
            padx = 100)
        self.label_header.pack()
        

        self.total_calories_label = Label(self, text=f"{self.master.get_total_calories()} Total Calories Today", font="Verdana 20 bold",
            fg="#000",
            bg="#99B898",
            pady = 20,
            padx = 100)
        self.total_calories_label.pack()
        

        self.wetFoodButton = Button(self, text="Wet Food", background = "#C06C84",
          command=lambda: self.master.add_to_cart("wet_quantity", self.master.wet_default_quantity), height=10, width=40, font = "Arial 16 bold")
        self.wetFoodButton.pack()

        self.checkoutButton = Button(self, text="Checkout", background = "#C06C84",
          command=self.master.checkout_cart, height=10, width=40, font = "Arial 16 bold")
        self.checkoutButton.pack()
from tkinter import *
from tkinter import ttk
from datetime import date


class WeighInFrame(ttk.Frame):
    """Frame to display and edit the current weight for today.

    Usage: WeighInFrame(parent, app, show_home_callback=...)
    """

    def __init__(self, master=None, app=None, show_home_callback=None):
        super().__init__(master)
        self.app = app
        self.show_home_callback = show_home_callback
        self.current_weight = 0.0
        # initialize from app if available
        try:
            if self.app and hasattr(self.app, 'calories_today'):
                self.current_weight = float(self.app.calories_today.get('weight', 0.0) or 0.0)
        except Exception:
            self.current_weight = 0.0
        self.create_widgets()

    def create_widgets(self):
        main = ttk.Frame(self)
        main.pack(fill=BOTH, expand=True, padx=8, pady=8)

        header = ttk.Label(main, text="Weigh In", style='Header.TLabel')
        header.pack(pady=(0, 8))

        # Large central area for weight + and - buttons
        center = ttk.Frame(main, style='Card.TFrame')
        center.pack(fill=X, expand=False, pady=(0, 12), padx=8)

        dec_btn = ttk.Button(center, text='−', width=3, command=lambda: self._adjust(-0.1))
        dec_btn.pack(side=LEFT, padx=(8, 12), pady=16)

        self.weight_label = ttk.Label(center, text=f"{self.current_weight:.1f}", style='Header.TLabel')
        self.weight_label.pack(side=LEFT, padx=12)

        inc_btn = ttk.Button(center, text='+', width=3, command=lambda: self._adjust(0.1))
        inc_btn.pack(side=LEFT, padx=(12, 8), pady=16)

        # Status label
        self.status_label = ttk.Label(main, text="", style='Subheader.TLabel')
        self.status_label.pack(pady=(0, 8))

        # Confirm button at bottom (same look/behavior as cart confirm)
        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=X, pady=(4, 8))

        self.confirm_button = ttk.Button(btn_frame, text="✓ CONFIRM", command=self._confirm, style='Accent.TButton')
        self.confirm_button.pack(fill=X)

    def _adjust(self, delta):
        try:
            new_w = round(self.current_weight + delta, 1)
            if new_w < 0:
                new_w = 0.0
            self.current_weight = new_w
            self.weight_label.config(text=f"{self.current_weight:.1f}")
        except Exception:
            pass

    def _confirm(self):
        """Save the weight for today, overwriting any existing weight value."""
        if not self.app:
            return
        # Ensure today's data is loaded (creates file if needed)
        try:
            self.app.load_calories_today()
        except Exception:
            pass
        # overwrite the weight for today
        try:
            self.app.calories_today['weight'] = float(self.current_weight)
        except Exception:
            try:
                self.app.calories_today['weight'] = float(str(self.current_weight))
            except Exception:
                self.app.calories_today['weight'] = 0.0

        # Show saving status same as cart
        try:
            self.status_label.config(text="✓ Saving...")
            self.status_label.update()
        except Exception:
            pass

        try:
            self.app.save_calories_today()
        except Exception:
            pass

        # Return to home if callback provided
        if callable(self.show_home_callback):
            try:
                self.show_home_callback()
            except Exception:
                pass

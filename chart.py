from tkinter import *
from tkinter import ttk
from datetime import datetime
import os

class ChartFrame(ttk.Frame):
    """Frame that displays a calorie-per-day chart with a toolbar and dark theme.

    Reads `log/*.txt` files (YYYY-MM-DD.txt) and sums calorie fields to plot daily totals.
    """

    def __init__(self, master=None, show_home_callback=None):
        super().__init__(master)
        self.show_home_callback = show_home_callback
        self.create_widgets()

    def create_widgets(self):
        # Try to import matplotlib; if unavailable, show a helpful message
        try:
            import matplotlib
            matplotlib.use('TkAgg')
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        except Exception:
            msg = (
                "matplotlib not available — install it to see charts.\n"
                "Run: pip install matplotlib"
            )
            placeholder = ttk.Label(self, text=msg, style='Subheader.TLabel')
            placeholder.pack(padx=12, pady=12)
            return

        dates, totals = self._load_daily_totals()

        # Create figure and apply dark theme colors matching the app
        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        bg_dark = '#0f1419'
        bg_light = '#1a2332'
        text_primary = '#ffffff'
        text_secondary = '#b0b9c1'
        accent_primary = '#ff6b9d'

        fig.patch.set_facecolor(bg_dark)
        ax.set_facecolor(bg_light)

        if dates:
            ax.plot(dates, totals, marker='o', color=accent_primary, markerfacecolor=text_primary)
            ax.set_title('Calories per Day', color=text_primary)
            ax.set_ylabel('Calories', color=text_secondary)
            ax.tick_params(colors=text_secondary)
            for spine in ax.spines.values():
                spine.set_color(text_secondary)
            fig.autofmt_xdate()
        else:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center', color=text_secondary)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=BOTH, expand=True, padx=8, pady=8)

        # Return button at bottom
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=X, pady=(4, 8))
        # Return button styled like Checkout
        self.return_btn = ttk.Button(btn_frame, text='Return', command=self._on_return, style='NarrowAccent.TButton')
        self.return_btn.pack(fill=X)

    def _on_return(self):
        if callable(self.show_home_callback):
            try:
                self.show_home_callback()
            except Exception:
                pass

    def _load_daily_totals(self):
        """Read `log/*.txt` files and compute total calories per file.

        Returns (dates, totals) where dates is a list of datetime.date and totals
        is a list of ints.
        """
        log_dir = os.path.join(os.path.dirname(__file__), 'log')
        totals_by_date = []
        if not os.path.isdir(log_dir):
            return [], []

        for fname in os.listdir(log_dir):
            if not fname.endswith('.txt'):
                continue
            try:
                date_obj = datetime.fromisoformat(fname.replace('.txt', '')).date()
            except Exception:
                continue
            path = os.path.join(log_dir, fname)
            total = 0
            try:
                with open(path, 'r') as f:
                    for line in f:
                        if '=' not in line:
                            continue
                        key, val = line.strip().split('=', 1)
                        # Only sum the explicit _cal fields
                        if key in ('wet_cal','dry_cal','minnow_cal','egg_cal','giblet_cal','churu_cal','greenie_cal'):
                            try:
                                total += int(val)
                            except Exception:
                                try:
                                    total += int(float(val))
                                except Exception:
                                    pass
            except Exception:
                continue
            totals_by_date.append((date_obj, total))

        # Sort by date
        totals_by_date.sort()
        dates = [d for d, t in totals_by_date]
        totals = [t for d, t in totals_by_date]
        return dates, totals

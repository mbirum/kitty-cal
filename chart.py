from tkinter import *
from tkinter import ttk
from datetime import datetime
import os

class ChartFrame(ttk.Frame):
    """Frame that displays a calorie-per-day chart with a toolbar and dark theme.

    Reads `log/*.txt` files (YYYY-MM-DD.txt) and sums calorie fields to plot daily totals.
    """

    def __init__(self, master=None, app=None, show_home_callback=None):
        super().__init__(master)
        self.app = app
        self.show_home_callback = show_home_callback
        # default view is weight by day
        self.current_view = 'weight'  # 'weight' or 'calories'
        self._dates = []
        self._calories = []
        self._weights = []
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

        # Load both calories and weight data
        dates, calories, weights = self._load_daily_data()
        self._dates = dates
        self._calories = calories
        self._weights = weights

        # Tabs: create a Notebook with two tabs (Weight, Calories)
        self.notebook = ttk.Notebook(self)
        # Limit notebook height so the Return button remains visible on small screens.
        # Use place with a relative height (82% of the available height) so the
        # Return button can occupy the remaining area at the bottom.
        self.notebook.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.82)

        self.weight_frame = ttk.Frame(self.notebook)
        self.calories_frame = ttk.Frame(self.notebook)
        self.today_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.weight_frame, text='Weight')
        self.notebook.add(self.calories_frame, text='Calories')
        self.notebook.add(self.today_frame, text='Today')

        # Draw both charts into their respective tab frames and populate Today tab
        self._draw_chart('weight', self.weight_frame)
        self._draw_chart('calories', self.calories_frame)
        self._draw_today_tab(self.today_frame)

        # ensure the notebook shows the Weight tab first
        try:
            self.notebook.select(0)
        except Exception:
            pass

        # Return button at bottom
        btn_frame = ttk.Frame(self)
        # Ensure the button frame is always at the bottom
        btn_frame.pack(side=BOTTOM, fill=X, pady=(4, 8))
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
        # Deprecated; kept for backward compatibility. Use _load_daily_data instead.
        dates, calories, weights = self._load_daily_data()
        return dates, calories

    def _load_daily_data(self):
        """Read `log/*.txt` files and compute total calories and weight per file.

        Returns (dates, calories, weights) where dates is a list of datetime.date,
        calories is a list of ints, and weights is a list of floats or None.
        """
        log_dir = os.path.join(os.path.dirname(__file__), 'log')
        rows = []
        if not os.path.isdir(log_dir):
            return [], [], []

        for fname in os.listdir(log_dir):
            if not fname.endswith('.txt'):
                continue
            try:
                date_obj = datetime.fromisoformat(fname.replace('.txt', '')).date()
            except Exception:
                continue
            path = os.path.join(log_dir, fname)
            total = 0
            weight = None
            try:
                with open(path, 'r') as f:
                    for line in f:
                        if '=' not in line:
                            continue
                        key, val = line.strip().split('=', 1)
                        # calories fields
                        if key in ('wet_cal','dry_cal','minnow_cal','egg_cal','giblet_cal','churu_cal','greenie_cal'):
                            try:
                                total += int(val)
                            except Exception:
                                try:
                                    total += int(float(val))
                                except Exception:
                                    pass
                        elif key == 'weight':
                            try:
                                weight = float(val)
                            except Exception:
                                try:
                                    weight = float(val.replace(',', '.'))
                                except Exception:
                                    weight = None
            except Exception:
                continue
            rows.append((date_obj, total, weight))

        # Sort by date
        rows.sort()
        dates = [d for d, c, w in rows]
        calories = [c for d, c, w in rows]
        weights = [w for d, c, w in rows]
        return dates, calories, weights

    def _draw_chart(self, view, target_frame):
        # Clear previous canvas in the provided target frame
        try:
            for child in target_frame.winfo_children():
                child.destroy()
        except Exception:
            pass

        # Lazy import matplotlib here (already imported earlier in create_widgets)
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        bg_dark = '#0f1419'
        bg_light = '#1a2332'
        text_primary = '#ffffff'
        text_secondary = '#b0b9c1'
        accent_primary = '#ff6b9d'

        fig, ax = plt.subplots(figsize=(8, 3), dpi=100)
        fig.patch.set_facecolor(bg_dark)
        ax.set_facecolor(bg_light)

        if view == 'weight':
            # filter dates with weight present
            pts = [(d, w) for d, w in zip(self._dates, self._weights) if w is not None]
            if pts:
                xs = [d for d, _ in pts]
                ys = [w for _, w in pts]
                ax.plot(xs, ys, marker='o', color=accent_primary, markerfacecolor=text_primary)
                ax.set_title('Weight per Day', color=text_primary)
                ax.set_ylabel('Weight', color=text_secondary)
            else:
                ax.text(0.5, 0.5, 'No weight data available', ha='center', va='center', color=text_secondary)
        else:
            if self._dates:
                ax.plot(self._dates, self._calories, marker='o', color=accent_primary, markerfacecolor=text_primary)
                ax.axhline(200, color='red', linewidth=1, linestyle='-', alpha=0.8)
                ax.set_title('Calories per Day', color=text_primary)
                ax.set_ylabel('Calories', color=text_secondary)
            else:
                ax.text(0.5, 0.5, 'No calorie data available', ha='center', va='center', color=text_secondary)

        ax.tick_params(colors=text_secondary)
        for spine in ax.spines.values():
            spine.set_color(text_secondary)
        fig.autofmt_xdate()

        # Chart canvas placed directly into the provided target frame
        canvas = FigureCanvasTkAgg(fig, master=target_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=BOTH, expand=True)
        # don't store globally; each tab keeps its own canvas if needed

    def _draw_today_tab(self, target_frame):
        # Clear previous contents
        try:
            for child in target_frame.winfo_children():
                child.destroy()
        except Exception:
            pass
        bg_light = '#1a2332'
        text_primary = '#ffffff'

        # Fetch calories_today data
        cal_data = {}
        try:
            cal_data = getattr(self.app, 'calories_today', {}) or {}
        except Exception:
            cal_data = {}

        # Create a container row for two columns and fix its height so view stays short
        container = ttk.Frame(target_frame)
        container.pack(fill=X, padx=8, pady=8)
        # prepare items split roughly in half for two columns
        items = list(cal_data.items()) if cal_data else []
        mid = (len(items) + 1) // 2
        left_items = items[:mid]
        right_items = items[mid:]

        # Determine a reasonable text height (lines) so overall height is smaller
        per_col = max(1, mid)
        lines = min(max(4, per_col), 20)
        # approximate pixel height per line and compute container height
        pixel_per_line = 18
        pixel_height = lines * pixel_per_line + 8
        # lock container height so it doesn't expand and push the Return button offscreen
        container.pack_propagate(False)
        try:
            container.config(height=pixel_height)
        except Exception:
            pass

        # Left column Text (placed to occupy exactly half width)
        left_txt = Text(container, bg=bg_light, fg=text_primary, font=('Courier', 12), bd=0, highlightthickness=0, wrap=NONE)
        left_txt.place(relx=0.0, rely=0.0, relwidth=0.5, relheight=1.0)

        # Right column Text (placed to occupy exactly half width)
        right_txt = Text(container, bg=bg_light, fg=text_primary, font=('Courier', 12), bd=0, highlightthickness=0, wrap=NONE)
        right_txt.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=1.0)

        if items:
            left_lines = [f"{k}={v}" for k, v in left_items]
            right_lines = [f"{k}={v}" for k, v in right_items]
            left_txt.insert('1.0', '\n'.join(left_lines))
            right_txt.insert('1.0', '\n'.join(right_lines))
        else:
            left_txt.insert('1.0', 'No calories_today data available')

        left_txt.config(state=DISABLED)
        right_txt.config(state=DISABLED)

    def refresh(self):
        """Reload data from logs and redraw both tabs."""
        dates, calories, weights = self._load_daily_data()
        self._dates = dates
        self._calories = calories
        self._weights = weights

        # redraw into existing frames
        try:
            self._draw_chart('weight', self.weight_frame)
        except Exception:
            pass
        try:
            self._draw_chart('calories', self.calories_frame)
        except Exception:
            pass

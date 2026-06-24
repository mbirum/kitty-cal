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
        self.notebook.pack(fill=BOTH, expand=True, padx=8, pady=8)

        self.weight_frame = ttk.Frame(self.notebook)
        self.calories_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.weight_frame, text='Weight')
        self.notebook.add(self.calories_frame, text='Calories')

        # Draw both charts into their respective tab frames (default tab is Weight)
        self._draw_chart('weight', self.weight_frame)
        self._draw_chart('calories', self.calories_frame)

        # ensure the notebook shows the Weight tab first
        try:
            self.notebook.select(0)
        except Exception:
            pass

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
                ax.set_title('Calories per Day', color=text_primary)
                ax.set_ylabel('Calories', color=text_secondary)
            else:
                ax.text(0.5, 0.5, 'No calorie data available', ha='center', va='center', color=text_secondary)

        ax.tick_params(colors=text_secondary)
        for spine in ax.spines.values():
            spine.set_color(text_secondary)
        fig.autofmt_xdate()

        # Create a container so we can show a left column next to the chart
        container = ttk.Frame(target_frame)
        container.pack(fill=BOTH, expand=True)

        # Left column: show `calories_today` contents in monospace
        left_frame = ttk.Frame(container)
        left_frame.pack(side=LEFT, fill=Y, padx=(6, 8), pady=6)

        # Use a Text widget for monospaced, multiline display and set it read-only
        cal_text = Text(left_frame, bg=bg_light, fg=text_primary, font=('Courier', 12), bd=0, highlightthickness=0)
        cal_text.pack(fill=Y, expand=False)

        # Fetch calories_today from the application root if available
        cal_data = {}
        try:
            cal_data = getattr(self.app, 'calories_today', {}) or {}
        except Exception:
            cal_data = {}

        if cal_data:
            lines = []
            # keep a stable order similar to app.get_initial_calories
            for k, v in cal_data.items():
                lines.append(f"{k}={v}")
            cal_text.insert('1.0', '\n'.join(lines))
        else:
            cal_text.insert('1.0', 'No calories_today data available')

        cal_text.config(state=DISABLED)

        # Chart canvas placed to the right of the left column
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=LEFT, fill=BOTH, expand=True)
        # don't store globally; each tab keeps its own canvas if needed

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

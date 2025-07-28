import tkinter as tk

class Tooltip:
    def __init__(self, widget, text, border_color="#336699"):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.border_color = border_color
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert") or (0, 0, 0, 0)
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 20
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        # Frame per bordo colorato
        frame_bordo = tk.Frame(self.tooltip, background=self.border_color, padx=2, pady=2)
        frame_bordo.pack()

        # Label tooltip dentro il frame
        label = tk.Label(frame_bordo, text=self.text, justify='left',
                         background="#ffffff", font=("Calibri", 16), wraplength=250)
        label.pack()

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

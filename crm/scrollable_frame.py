import tkinter as tk
from tkinter import ttk

class ScrollableFrame(ttk.Frame):
    """class reprsenting a special tkinter object - scrollable frame"""

    def __init__(self, container, height=300, width=500, *args, **kwargs):
        """initialize widgets scrollable frame contains from"""

        super().__init__(container, *args, **kwargs)

        # canvas containing a scrollbar and output frame
        canvas = tk.Canvas(self)
        canvas.config(height=height, width=width)

        # scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        # output frame
        self.scrollable_frame = ttk.Frame(canvas)

        # bind scrollbar to the frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def destroy(self):
        super().destroy()
        self.scrollable_frame.destroy()

import tkinter as tk
from tkinter import ttk


class Intro(ttk.Frame):  # we are calling super class to make self into the frame
    def __init__(self, parent, controller, show_welcome, show_game_window):
        super().__init__(parent)

        self["style"] = "Background.TFrame"  # assigning Background style

        welcome_description = ttk.Label(self,
                                        text="Welcome! Click on the buttons below to navigate. Enjoy......!",
                                        style="LightText.TLabel",
                                        )
        welcome_description.grid(row=0, column=0, sticky="W", padx=(10, 0), pady=(10, 0))

        # button container
        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(sticky="EW", padx=10)
        button_container.columnconfigure(0, weight=1)

        welcome_description.grid(row=0, column=0, sticky="N", padx=10, pady=(10, 10))

        # back button
        timer_button = ttk.Button(button_container,
                                  text="Back",
                                  command=show_welcome,
                                  style="PomodoroButton.TButton",
                                  cursor="hand2")
        timer_button.grid(row=0, column=5, sticky="N", padx=0, pady=(10, 10))

        # game button calling show_timer function in app.py (lambda function)
        game_button = ttk.Button(button_container,
                                 text="Game",
                                 command=show_game_window,
                                 style="PomodoroButton.TButton",
                                 cursor="hand2")
        game_button.grid(row=1, column=5, sticky="W", padx=0, pady=(10, 10))



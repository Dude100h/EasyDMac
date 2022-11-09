import os.path
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from playsound import playsound

MOVE_INCREMENT = 20  # SPACE TO MOVE AFTER FIRST HEAD
MOVES_PER_SECOND = 15  # MOVES PER SEC, AFFECTS GAME SPEED DIRECTLY, CHANGE THIS TO ALTER THE GAME SPEED
GAME_SPEED = 1000 // MOVES_PER_SECOND  # DEFINES THE GAME SPEED


class Game(ttk.Frame):
    def __init__(self, parent, controller, show_welcome, background):
        super().__init__(parent)

        labelframe = LabelFrame(self, background=background)
        labelframe.pack(fill="x", expand="yes", pady=(5, 800), padx=5)
        button_container = ttk.Frame(labelframe,
                                     padding=10,
                                     style="Background.TFrame")
        button_container.pack(expand=True, fill="both")

        # welcome button calling show_timer function in app.py (lambda function)

        welcome_button = ttk.Button(button_container,
                                    text="Welcome",
                                    command=show_welcome,
                                    style="PomodoroButton.TButton",
                                    cursor="hand2")
        welcome_button.pack(expand="True", fill="both", padx=50, pady=(0, 0))

        class Snake(tk.Canvas):  # canvas class

            def __init__(self):
                super().__init__(width=600, height=620, background="black",
                                highlightthickness=0)  # super class contain canvas

                self.snake_positions = [(100, 100), (80, 100),
                                        (60, 100)]  # assign position to snake_body as each box of 20 pixels
                self.food_position = (200, 100)
                self.score = 0
                self.direction = "Right"  # default snake moves in right
                self.bind_all("<Key>",
                              self.on_key_press)  # <Key> means any key pressed on the keyboard, on key press we call the function specified

                self.load_assets()
                self.create_objects()

                self.after(GAME_SPEED, self.perform_actions)

            def load_assets(self):
                try:
                    self.snake_body_image = Image.open("./assets/snake.png")  # opens image
                    self.snake_body = ImageTk.PhotoImage(self.snake_body_image)  # assigns image to snake_body

                    self.food_image = Image.open("./assets/food.png")  # opens image
                    self.food = ImageTk.PhotoImage(self.food_image)  # assigns image to food

                except IOError as error:
                    print(error)
                    # Snake.destroy(self)

            def create_objects(self):  # place the assets into the window
                self.create_text(
                    45, 12, text=f"Score {self.score}", tag="score", fill="#fff", font=("TkDefaultFont", 14)
                )  # allows to create text and add updating info like score

                for x_position, y_position in self.snake_positions:
                    self.create_image(x_position, y_position, image=self.snake_body,
                                      tag="snake")  # method within the canvas which create image assets
                self.create_image(*self.food_position, image=self.food,
                                  tag="food")  # create food image and place it in the window
                self.create_rectangle(7, 27, 593, 613, outline="#525d69")  # creates a boundary

            def move_snake(self):
                head_x_position, head_y_position = self.snake_positions[0]  # extract the initial head values

                if self.direction == "Left":
                    new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)  # new head position
                elif self.direction == "Right":
                    new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
                elif self.direction == "Down":
                    new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
                elif self.direction == "Up":
                    new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

                self.snake_positions = [new_head_position] + self.snake_positions[
                                                         :-1]  # when head move we chop off the last element of the tail

                for segement, position in zip(self.find_withtag("snake"),
                                              self.snake_positions):  # we get all the snake images with their positions, zip creates tuple of first element with its position and so on
                    self.coords(segement,
                                position)  # we fetch the image and position and use this function to change the position of that image

            def perform_actions(self):  # function to perform actions
                if self.check_collisions():
                    return  # this means the game stops as we return here, perform_actions is not called again

                self.move_snake()
                self.after(GAME_SPEED,
                           self.perform_actions)  # calls function perform_action agter 75 milliseconds, not the value that function returns

            def check_collisions(self):
                head_x_position, head_y_position = self.snake_positions[0]  # extract the initial head values

                return (
                        head_x_position in (0, 600)  # check wether snake collides with the side walls
                        or head_y_position in (20, 620)  # checks wether snake collides with the top/bottom walls
                        or (head_x_position, head_y_position) in self.snake_positions[1:]
                    # check wether the snake collides with itself
                )

            def on_key_press(self, e):
                new_direction = e.keysym
                all_directions = ("Up", "Down", "Left", "Right")  # tuple of given directions
                opposites = ({"Up", "Down"}, {"Left", "Right"})  # tuple with set of opposite directions

                if (
                        new_direction in all_directions  # check new direction in given directions
                        and {new_direction, self.direction} not in opposites
                        # check new direction not opposite i.e up/down, left/right
                ):
                    self.direction = new_direction

        #
        # root = tk.Tk()
        # root.title("Application")  # title
        # root.resizable(False, False)  # window size
        #
        # board = Snake()  # instance for App class
        # board.grid()  # put everything into the App Window
        #
        # root.mainloop()

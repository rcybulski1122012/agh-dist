import tkinter as tk

WIDTH = HEIGHT = 400

gui = tk.Tk()
gui.geometry(f"{WIDTH}x{HEIGHT}")

label = tk.Label(gui, text="Hello, world!")

label.pack()

gui.mainloop()


# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\ProjectLaoHu\Python\TestPrivateGPT\Petch\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1500x800")
window.configure(bg = "#E6E6E6")


canvas = Canvas(
    window,
    bg = "#E6E6E6",
    height = 800,
    width = 1500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    109.0,
    90.0,
    image=image_image_1
)

canvas.create_rectangle(
    30.0,
    209.0,
    1441.0,
    662.0,
    fill="#EE9292",
    outline="")

canvas.create_rectangle(
    44.0,
    222.0,
    1428.0,
    645.0,
    fill="#FBFBFB",
    outline="")

canvas.create_text(
    188.0,
    53.0,
    anchor="nw",
    text="LAOHU",
    fill="#000000",
    font=("JotiOne Regular", 55 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=500.0,
    y=68.0,
    width=281.0,
    height=75.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=1149.0,
    y=687.0,
    width=255.0,
    height=67.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=30.0,
    y=170.0,
    width=179.0,
    height=39.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
button_4.place(
    x=209.0,
    y=170.0,
    width=179.0,
    height=39.0
)
window.resizable(True, True)
window.mainloop()

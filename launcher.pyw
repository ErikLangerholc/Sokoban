from tkinter import *
from tkinter.ttk import *
import game

def start():
    if not value.get().isnumeric():
        input.invoke("buttondown")
    levelnumber = int(value.get())
    levelnumber = min(90, levelnumber)
    levelnumber = max(1, levelnumber)
    try:
        text2 = ""
        for vrstica in text.split("\n"):
            if vrstica.split()[0] == "StartingLevel":
                text2 += "StartingLevel " + str(levelnumber) + "\n"
            else:
                text2 += vrstica + "\n"
        settingsfile = open("settings.txt", "w")
        settingsfile.write(text2.rstrip())
        settingsfile.close()
    except:
        print("Error reading settings file. Defaulting to level 1")
    w.destroy()
    game.Run()


w = Tk()
w.title("Sokoban")
w.resizable(0, 0)
text = Label(w, text="\nWelcome to Sokoban!\n\nSelect level (1-90):\n", justify=CENTER)
text.grid(column=1, row=0)
navodila = Label(w, text="You are a warehause keeper.\nPush all crates to where they belong.\nArrow keys - move\nEsc - restart level\nDouble Esc - exit\n\nGood luck!", justify=CENTER)
navodila.grid(column=1, row=4)
knof = Button(w, text="Start", command=start)
knof.grid(column=1, row=3)
empty = "          "
empty1 = Label(w, text=empty)
empty1.grid(column=0, row=0)
empty2 = Label(w, text=empty)
empty2.grid(column=2, row=0)

try:
    settingsfile = open("settings.txt.")
    text = settingsfile.read()
    for setting, values in [(x[0], x[1:]) for x in [x.split() for x in text.split("\n")]]:
        if setting == "StartingLevel":
            levelnumber = int(values[0])
    settingsfile.close()
except:
    print("Error reading settings file")
    levelnumber = 1

value = StringVar(w)
value.set(levelnumber)
input = Spinbox(w, from_=1, to=90, justify=CENTER, width=5, textvariable=value)
input.grid(column=1, row=1)
input.focus()

w.mainloop()

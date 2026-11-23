
import tkinter as tk
import random

jokes = []
current_punchline = ""

#Reads jokes from the text file! (Ai used in this part, couldn't figure out why the jokes won't show up with the previous method.)
import os

def loadJokes():
    global jokes

    file_path = os.path.join(os.path.dirname(__file__), "randomJokes.txt")

    try:
        file = open(file_path, "r", encoding="utf-8")
        jokes = file.readlines()
        file.close()
        print("Jokes loaded:", len(jokes))

    except FileNotFoundError:
        print("ERROR: Text file not found!")
        print("Looking for:", file_path)

#Selects and displays a random joke!
def tellJoke():
    global current_punchline

    if len(jokes) == 0:
        setup_label.config(text="No jokes found!")
        punchline_label.config(text="")
        return

    selected_joke = random.choice(jokes)

    if "?" in selected_joke:
        setup, punchline = selected_joke.split("?", 1)

        setup_label.config(text=setup + "?")
        current_punchline = punchline.strip()
        punchline_label.config(text="")
    else:
        setup_label.config(text="Invalid joke format!")
        punchline_label.config(text="")
        current_punchline = ""

def showPunchline():
    if current_punchline:
        punchline_label.config(text=current_punchline)

#Gets another random joke!
def nextJoke():
    tellJoke()

#Main window!
root = tk.Tk()
root.title("Alexa Tell Me a Joke")
root.geometry("500x400")
root.resizable(False, False)
root.configure(bg="#FFF0F3")

#Reads the joke file!
try:
    loadJokes()
except FileNotFoundError:
    jokes = []

#Main heading!
title_label = tk.Label(
    root,
    text="♡ ALEXA, TELL ME A JOKE ♡",
    font=("Georgia", 19, "bold"),
    bg="#FFF0F3",
    fg="#C76D7E"
)
title_label.pack(pady=25)

instruction_label = tk.Label(
    root,
    text="Ready for a little laugh?",
    font=("Arial", 12),
    bg="#FFF0F3",
    fg="#713F4A"
)
instruction_label.pack(pady=5)

#This will display the joke setup!
setup_label = tk.Label(
    root,
    text="Click the button below to hear a joke!",
    font=("Arial", 13, "bold"),
    bg="#FFFFFF",
    fg="#713F4A",
    wraplength=400,
    width=40,
    height=3
)
setup_label.pack(pady=20)

#this part displays the punchline!
punchline_label = tk.Label(
    root,
    text="",
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#C76D7E",
    wraplength=400,
    width=40,
    height=2
)
punchline_label.pack(pady=5)

#Joke buttons!
tell_button = tk.Button(
    root,
    text="Alexa tell me a Joke",
    font=("Arial", 11, "bold"),
    bg="#F4ACB7",
    fg="#713F4A",
    width=23,
    relief="flat",
    command=tellJoke
)
tell_button.pack(pady=7)

punchline_button = tk.Button(
    root,
    text="Show Punchline",
    font=("Arial", 11, "bold"),
    bg="#FADADD",
    fg="#713F4A",
    width=23,
    relief="flat",
    command=showPunchline
)
punchline_button.pack(pady=7)

next_button = tk.Button(
    root,
    text="Next Joke",
    font=("Arial", 11, "bold"),
    bg="#E88D9B",
    fg="#FFFFFF",
    width=23,
    relief="flat",
    command=nextJoke
)
next_button.pack(pady=7)

quit_button = tk.Button(
    root,
    text="Quit",
    font=("Arial", 10, "bold"),
    bg="#713F4A",
    fg="#FFFFFF",
    width=15,
    relief="flat",
    command=root.destroy
)
quit_button.pack(pady=12)

root.mainloop()

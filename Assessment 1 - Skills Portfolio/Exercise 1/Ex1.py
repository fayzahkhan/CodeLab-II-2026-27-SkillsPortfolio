

import tkinter as tk
import random
from pathlib import Path


def displayMenu():
    menu_frame.pack()
    quiz_frame.pack_forget()
    result_frame.pack_forget()


def randomInt(difficulty):
    if difficulty == "Easy":
        return random.randint(0, 9)
    
    elif difficulty == "Moderate":
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation():
    return random.choice(["+", "-"])


#Starts the quiz and resets the score!
def startQuiz(difficulty):
    global score, question_count, first_attempt
    global selected_difficulty

    score = 0
    question_count = 0
    first_attempt = True
    selected_difficulty = difficulty

    menu_frame.pack_forget()
    result_frame.pack_forget()
    quiz_frame.pack(pady=20)

    feedback_label.config(text="")
    updateScore()
    displayProblem()


#This function generates and displays each question!
def displayProblem():
    global num1, num2, operation, answer, first_attempt

    if question_count == 10:
        displayResults()
        return

    num1 = randomInt(selected_difficulty)
    num2 = randomInt(selected_difficulty)
    operation = decideOperation()

    if operation == "+":
        answer = num1 + num2
    else:
        answer = num1 - num2

    first_attempt = True

    question_label.config(
        text=f"Question {question_count + 1} of 10\n\n"
             f"{num1} {operation} {num2} = ?"
    )

    answer_entry.delete(0, tk.END)
    feedback_label.config(text="")
    submit_button.config(state="normal")
    answer_entry.focus()


# Checks the answer and updates the user's score!
def isCorrect():
    global score, question_count, first_attempt

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        feedback_label.config(
            text="Please enter a valid number!",
            fg="#C76D7E"
        )
        return

    if user_answer == answer:
        if first_attempt:
            score += 10
            feedback_label.config(
                text="Correct! +10 points ♡",
                fg="#719B79"
            )
        else:
            score += 5
            feedback_label.config(
                text="Correct! +5 points ♡",
                fg="#719B79"
            )

        question_count += 1
        updateScore()
        submit_button.config(state="disabled")
        root.after(1000, displayProblem)

    else:
        if first_attempt:
            first_attempt = False
            feedback_label.config(
                text="Not quite! Try one more time ♡",
                fg="#C76D7E"
            )
        else:
            feedback_label.config(
                text=f"Incorrect! The answer was {answer} :C",
                fg="#C76D7E"
            )

            question_count += 1
            submit_button.config(state="disabled")
            root.after(1500, displayProblem)


def updateScore():
    score_label.config(text=f"Score: {score}/100")


#Displays the final score and grade!
def displayResults():
    quiz_frame.pack_forget()
    result_frame.pack(pady=30)

    if score > 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    elif score >= 50:
        grade = "D"
    else:
        grade = "F"

    result_label.config(
        text=f"Quiz Complete! ♡\n\n"
             f"Your score: {score}/100\n"
             f"Your grade: {grade}"
    )


def playAgain():
    displayMenu()


#Main window!
root = tk.Tk()
root.title("Fay's Arithmetic Quiz")
root.geometry("500x520")
root.resizable(False, False)
root.configure(bg="#FFF0F3")

base_dir = Path(__file__).resolve().parent

#Logo!
icon_path = base_dir / "calculator.ico"
if icon_path.exists():
    try:
        root.iconbitmap(str(icon_path))
    except tk.TclError:
        icon_img = tk.PhotoImage(file=str(base_dir / "p.png"))
        root.iconphoto(False, icon_img)
else:
    icon_img = tk.PhotoImage(file=str(base_dir / "p.png"))
    root.iconphoto(False, icon_img)

#Background image! (Ai used in this section, I couldn't figure out why the image won't show up with the previos method.)
image_path = base_dir / "p.png"

print(image_path)
print(image_path.exists())

background_image = tk.PhotoImage(file=str(image_path))

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.lower()


score = 0
question_count = 0
first_attempt = True
selected_difficulty = ""

num1 = 0
num2 = 0
operation = ""
answer = 0


# Main menu!
menu_frame = tk.Frame(root, bg="#FFFFFF", padx=40, pady=20)

title_label = tk.Label(
    menu_frame,
    text="♡ ARITHMETIC QUIZ ♡",
    font=("Georgia", 21, "bold"),
    bg="#FFFFFF",
    fg="#C76D7E"
)
title_label.pack(pady=15)

instruction_label = tk.Label(
    menu_frame,
    text="Choose your difficulty level!",
    font=("Arial", 12),
    bg="#FFFFFF",
    fg="#713F4A"
)
instruction_label.pack(pady=10)


easy_button = tk.Button(
    menu_frame,
    text="Easy",
    width=20,
    font=("Arial", 12, "bold"),
    bg="#FADADD",
    fg="#713F4A",
    activebackground="#F4ACB7",
    relief="flat",
    cursor="hand2",
    command=lambda: startQuiz("Easy")
)
easy_button.pack(pady=7)

moderate_button = tk.Button(
    menu_frame,
    text="Moderate",
    width=20,
    font=("Arial", 12, "bold"),
    bg="#F4ACB7",
    fg="#713F4A",
    activebackground="#E88D9B",
    relief="flat",
    cursor="hand2",
    command=lambda: startQuiz("Moderate")
)
moderate_button.pack(pady=7)

advanced_button = tk.Button(
    menu_frame,
    text="Advanced",
    width=20,
    font=("Arial", 12, "bold"),
    bg="#E88D9B",
    fg="#FFFFFF",
    activebackground="#C76D7E",
    relief="flat",
    cursor="hand2",
    command=lambda: startQuiz("Advanced")
)
advanced_button.pack(pady=7)

menu_footer = tk.Label(
    menu_frame,
    text="10 QUESTIONS  •  100 POINTS",
    font=("Arial", 9, "bold"),
    bg="#FFFFFF",
    fg="#C76D7E"
)
menu_footer.pack(pady=15)


#Quiz screen! 
quiz_frame = tk.Frame(root, bg="#FFFFFF", padx=40, pady=25)

quiz_title = tk.Label(
    quiz_frame,
    text="♡ YOUR QUIZ ♡",
    font=("Georgia", 20, "bold"),
    bg="#FFFFFF",
    fg="#C76D7E"
)
quiz_title.pack(pady=10)

question_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 19, "bold"),
    bg="#FFFFFF",
    fg="#713F4A"
)
question_label.pack(pady=20)

score_label = tk.Label(
    quiz_frame,
    text="Score: 0/100",
    font=("Arial", 12, "bold"),
    bg="#FFFFFF",
    fg="#C76D7E"
)
score_label.pack(pady=10)

answer_entry = tk.Entry(
    quiz_frame,
    font=("Arial", 16),
    justify="center",
    width=15,
    bg="#FFF0F3",
    fg="#713F4A",
    relief="flat"
)
answer_entry.pack(pady=15)

submit_button = tk.Button(
    quiz_frame,
    text="Submit Answer",
    width=20,
    font=("Arial", 11, "bold"),
    bg="#E88D9B",
    fg="#FFFFFF",
    activebackground="#C76D7E",
    relief="flat",
    cursor="hand2",
    command=isCorrect
)
submit_button.pack(pady=10)

feedback_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 11, "bold"),
    bg="#FFFFFF",
    fg="#C76D7E"
)
feedback_label.pack(pady=15)

#back to menu button!
quit_button = tk.Button(
    quiz_frame,
    text="Quit",
    width=20,
    font=("Arial", 11, "bold"),
    bg="#FADADD",
    fg="#713F4A",
    activebackground="#F4ACB7",
    relief="flat",
    cursor="hand2",
    command=displayMenu
)
quit_button.pack(pady=5)


#Results screen
result_frame = tk.Frame(root, bg="#FFFFFF", padx=40, pady=30)

result_label = tk.Label(
    result_frame,
    text="",
    font=("Georgia", 19, "bold"),
    bg="#FFFFFF",
    fg="#C76D7E"
)
result_label.pack(pady=25)

replay_button = tk.Button(
    result_frame,
    text="Play Again ♡",
    width=20,
    font=("Arial", 11, "bold"),
    bg="#F4ACB7",
    fg="#713F4A",
    activebackground="#E88D9B",
    relief="flat",
    cursor="hand2",
    command=playAgain
)
replay_button.pack(pady=10)

exit_button = tk.Button(
    result_frame,
    text="Exit",
    width=20,
    font=("Arial", 11, "bold"),
    bg="#FADADD",
    fg="#713F4A",
    activebackground="#F4ACB7",
    relief="flat",
    cursor="hand2",
    command=root.destroy
)
exit_button.pack(pady=5)


displayMenu()

root.mainloop()
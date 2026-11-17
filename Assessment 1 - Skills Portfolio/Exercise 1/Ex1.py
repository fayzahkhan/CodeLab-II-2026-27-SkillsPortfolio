
import tkinter as tk
from tkinter import messagebox
import random


def displayMenu():
    menu_frame.pack()
    quiz_frame.pack_forget()

    title_label.config(text="ARITHMETIC QUIZ")
    instruction_label.config(text="Choose your difficulty level!!")


def randomInt(difficulty):
    if difficulty == "Easy":
        return random.randint(0, 9)
    elif difficulty == "Moderate":
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation():
    return random.choice(["+", "-"])


def startQuiz(difficulty):
    global score, question_count, first_attempt
    global selected_difficulty

    score = 0
    question_count = 0
    first_attempt = True
    selected_difficulty = difficulty

    menu_frame.pack_forget()
    quiz_frame.pack()

    feedback_label.config(text="")
    updateScore()
    displayProblem()


def displayProblem():
    global num1, num2, operation, answer
    global first_attempt

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


def isCorrect():
    global score, question_count, first_attempt

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        feedback_label.config(text="Please enter a valid number!")
        return

    if user_answer == answer:
        if first_attempt:
            score += 10
            feedback_label.config(text="Correct! +10 points")
        else:
            score += 5
            feedback_label.config(text="Correct! +5 points")

        question_count += 1
        updateScore()

        submit_button.config(state="disabled")
        root.after(1000, displayProblem)

    else:
        if first_attempt:
            first_attempt = False
            feedback_label.config(
                text="Not quite! Try one more time."
            )
        else:
            feedback_label.config(
                text=f"Incorrect! The answer was {answer} :C."
            )

            question_count += 1
            submit_button.config(state="disabled")
            root.after(1500, displayProblem)


def updateScore():
    score_label.config(text=f"Score: {score}/100")


def displayResults():
    quiz_frame.pack_forget()
    result_frame.pack()

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
        text=f"Quiz Complete!\n\n"
             f"Your score: {score}/100\n"
             f"Your grade: {grade}"
    )


def playAgain():
    result_frame.pack_forget()
    displayMenu()


root = tk.Tk()
root.title("Arithmetic Quiz")
root.geometry("450x400")
root.resizable(False, False)
root.configure(bg="#ffc4eb")

score = 0
question_count = 0
first_attempt = True
selected_difficulty = ""

num1 = 0
num2 = 0
operation = ""
answer = 0


menu_frame = tk.Frame(root, bg="#ffc4eb")

title_label = tk.Label(
    menu_frame,
    text="ARITHMETIC QUIZ",
    font=("Arial", 24, "bold"),
    bg="#ffc4eb"
)
title_label.pack(pady=20)

instruction_label = tk.Label(
    menu_frame,
    text="Choose your difficulty level!!",
    font=("Arial", 13),
    bg="#ffc4eb"
)
instruction_label.pack(pady=10)

easy_button = tk.Button(
    menu_frame,
    text="Easy",
    width=18,
    command=lambda: startQuiz("Easy")
)
easy_button.pack(pady=5)

moderate_button = tk.Button(
    menu_frame,
    text="Moderate",
    width=18,
    command=lambda: startQuiz("Moderate")
)
moderate_button.pack(pady=5)

advanced_button = tk.Button(
    menu_frame,
    text="Advanced",
    width=18,
    command=lambda: startQuiz("Advanced")
)
advanced_button.pack(pady=5)


quiz_frame = tk.Frame(root, bg="#ffc4eb")

question_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 20, "bold"),
    bg="#ffc4eb"
)
question_label.pack(pady=25)

score_label = tk.Label(
    quiz_frame,
    text="Score: 0/100",
    font=("Arial", 12),
    bg="#ffc4eb"
)
score_label.pack(pady=5)

answer_entry = tk.Entry(
    quiz_frame,
    font=("Arial", 16),
    justify="center",
    width=15
)
answer_entry.pack(pady=15)

submit_button = tk.Button(
    quiz_frame,
    text="Submit Answer",
    width=18,
    command=isCorrect
)
submit_button.pack(pady=5)

feedback_label = tk.Label(
    quiz_frame,
    text="",
    font=("Arial", 11),
    bg="#ffc4eb"
)
feedback_label.pack(pady=15)


result_frame = tk.Frame(root, bg="#ffc4eb")

result_label = tk.Label(
    result_frame,
    text="",
    font=("Arial", 18, "bold"),
    bg="#ffc4eb"
)
result_label.pack(pady=40)

replay_button = tk.Button(
    result_frame,
    text="Play Again",
    width=18,
    command=playAgain
)
replay_button.pack(pady=10)

exit_button = tk.Button(
    result_frame,
    text="Exit",
    width=18,
    command=root.destroy
)
exit_button.pack(pady=5)


displayMenu()

root.mainloop()

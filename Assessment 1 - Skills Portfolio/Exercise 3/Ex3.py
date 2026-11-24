import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

students = []
header_line = None

#this will read student information from the text file!
def loadStudents():
    global students, header_line

    file_path = os.path.join(os.path.dirname(__file__), "studentMarks.txt")

    try:
        file = open(file_path, "r")
        lines = file.readlines()
        file.close()

        header_line = lines[0] if lines else None
        students = []

        for line in lines[1:]:
            data = line.strip().split(",")

            if len(data) == 6:
                student = [
                    data[0],
                    data[1],
                    int(data[2]),
                    int(data[3]),
                    int(data[4]),
                    int(data[5])
                ]

                students.append(student)

        output.delete("1.0", tk.END)
        output.insert(tk.END, "Student records loaded successfully!")

    except FileNotFoundError:
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Student file not found!")

def saveStudents():
    file_path = os.path.join(os.path.dirname(__file__), "studentMarks.txt")

    try:
        with open(file_path, "w") as file:
            if header_line is not None:
                if header_line.strip().isdigit():
                    file.write(f"{len(students)}\n")
                else:
                    file.write(header_line if header_line.endswith("\n") else header_line + "\n")

            for student in students:
                line = f"{student[0]},{student[1]},{student[2]},{student[3]},{student[4]},{student[5]}\n"
                file.write(line)
        return True
    except OSError:
        messagebox.showerror("Error", "Could not save changes to studentMarks.txt.")
        return False

#This function will calculate the coursework mark out of 60!
def courseworkMark(student):
    return student[2] + student[3] + student[4]

#This function will calculate the overall mark out of 160!
def totalMark(student):
    return courseworkMark(student) + student[5]

#This function calculates the overall percentage!
def percentage(student):
    return (totalMark(student) / 160) * 100

#determines the student's grade!
def getGrade(student):
    mark = percentage(student)

    if mark >= 70:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 40:
        return "D"
    else:
        return "F"

#This will format the student's information for display!
def displayStudent(student):
    result = ""
    result += "Student Name: " + student[1] + "\n"
    result += "Student Number: " + student[0] + "\n"
    result += "Coursework Mark: " + str(courseworkMark(student)) + "/60\n"
    result += "Exam Mark: " + str(student[5]) + "/100\n"
    result += "Overall Percentage: " + format(percentage(student), ".2f") + "%\n"
    result += "Grade: " + getGrade(student) + "\n"
    result += "-----------------------------\n"

    return result

#This function displays all student records and class average!
def viewAll():
    output.delete("1.0", tk.END)

    if len(students) == 0:
        output.insert(tk.END, "No student records available.")
        return

    total_percentage = 0

    for student in students:
        output.insert(tk.END, displayStudent(student))
        total_percentage += percentage(student)

    average = total_percentage / len(students)

    output.insert(tk.END, "\nCLASS SUMMARY\n")
    output.insert(tk.END, "Number of students: " + str(len(students)) + "\n")
    output.insert(tk.END, "Class average: " + format(average, ".2f") + "%")

#This function searches for a student using their name or student number!
def viewIndividual():
    search = search_entry.get().strip().lower()
    output.delete("1.0", tk.END)

    found = False

    for student in students:
        if search == student[0] or search == student[1].lower():
            output.insert(tk.END, displayStudent(student))
            found = True

    if not found:
        output.insert(tk.END, "Student not found!")

#This will find the student with the highest overall mark!
def highestStudent():
    output.delete("1.0", tk.END)

    if len(students) == 0:
        output.insert(tk.END, "No student records available.")
        return

    highest = students[0]

    for student in students:
        if totalMark(student) > totalMark(highest):
            highest = student

    output.insert(tk.END, "STUDENT WITH HIGHEST MARK\n\n")
    output.insert(tk.END, displayStudent(highest))

#This finds the student with the lowest overall mark!
def lowestStudent():
    output.delete("1.0", tk.END)

    if len(students) == 0:
        output.insert(tk.END, "No student records available.")
        return

    lowest = students[0]

    for student in students:
        if totalMark(student) < totalMark(lowest):
            lowest = student

    output.insert(tk.END, "STUDENT WITH LOWEST MARK\n\n")
    output.insert(tk.END, displayStudent(lowest))

def addStudent():
    dialog = tk.Toplevel(root)
    dialog.title("Add New Student")
    dialog.geometry("320x340")
    dialog.resizable(False, False)
    dialog.configure(bg="#FCE4EC")
    dialog.transient(root)
    dialog.grab_set()

    fields = [
        ("Student Number:", ""),
        ("Student Name:", ""),
        ("Coursework 1 (0-20):", ""),
        ("Coursework 2 (0-20):", ""),
        ("Coursework 3 (0-20):", ""),
        ("Exam Mark (0-100):", "")
    ]
    entries = []

    for label_text, default_val in fields:
        tk.Label(
            dialog,
            text=label_text,
            font=("Arial", 9, "bold"),
            bg="#FCE4EC",
            fg="#8E4A59"
        ).pack(pady=(6, 1))
        entry = tk.Entry(dialog, font=("Arial", 10), width=26, bg="#FFFFFF", fg="#333333")
        entry.insert(0, default_val)
        entry.pack()
        entries.append(entry)

    def submit_new():
        stu_num = entries[0].get().strip()
        stu_name = entries[1].get().strip()

        if not stu_num or not stu_name:
            messagebox.showwarning("Missing Info", "Please enter both student number and name.", parent=dialog)
            return

        if any(s[0] == stu_num for s in students):
            messagebox.showwarning("Duplicate ID", "A student with this number already exists.", parent=dialog)
            return

        try:
            cw1 = int(entries[2].get().strip())
            cw2 = int(entries[3].get().strip())
            cw3 = int(entries[4].get().strip())
            exam = int(entries[5].get().strip())
        except ValueError:
            messagebox.showwarning("Invalid Marks", "Marks must be whole numbers.", parent=dialog)
            return

        if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20 and 0 <= exam <= 100):
            messagebox.showwarning("Out of Range", "Coursework marks must be 0-20 and exam mark 0-100.", parent=dialog)
            return

        new_student = [stu_num, stu_name, cw1, cw2, cw3, exam]
        students.append(new_student)

        if saveStudents():
            output.delete("1.0", tk.END)
            output.insert(tk.END, "New student added successfully!\n\n")
            output.insert(tk.END, displayStudent(new_student))
            dialog.destroy()

    tk.Button(
        dialog,
        text="Save Student",
        command=submit_new,
        font=("Arial", 9, "bold"),
        bg="#FFFFFF",
        fg="#C76D7E",
        relief="flat",
        bd=1,
        width=18
    ).pack(pady=14)

def editStudent():
    if len(students) == 0:
        output.delete("1.0", tk.END)
        output.insert(tk.END, "No student records available to edit.")
        return

    query = search_entry.get().strip().lower()
    target_index = None

    if query:
        for idx, student in enumerate(students):
            if query == student[0].lower() or query == student[1].lower():
                target_index = idx
                break

    dialog = tk.Toplevel(root)
    dialog.title("Edit Student Record")
    dialog.geometry("340x390")
    dialog.resizable(False, False)
    dialog.configure(bg="#FCE4EC")
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(
        dialog,
        text="Select Student:",
        font=("Arial", 9, "bold"),
        bg="#FCE4EC",
        fg="#8E4A59"
    ).pack(pady=(8, 2))

    options = [f"{s[0]} - {s[1]}" for s in students]
    selected_var = tk.StringVar(dialog)
    initial_idx = target_index if target_index is not None else 0
    selected_var.set(options[initial_idx])

    selector = tk.OptionMenu(dialog, selected_var, *options)
    selector.config(font=("Arial", 9), bg="#FFFFFF", fg="#333333", width=28)
    selector.pack(pady=(0, 6))

    labels = [
        "Student Number:",
        "Student Name:",
        "Coursework 1 (0-20):",
        "Coursework 2 (0-20):",
        "Coursework 3 (0-20):",
        "Exam Mark (0-100):"
    ]
    entries = []

    for label_text in labels:
        tk.Label(
            dialog,
            text=label_text,
            font=("Arial", 9, "bold"),
            bg="#FCE4EC",
            fg="#8E4A59"
        ).pack(pady=(4, 1))
        entry = tk.Entry(dialog, font=("Arial", 10), width=26, bg="#FFFFFF", fg="#333333")
        entry.pack()
        entries.append(entry)

    def populate_fields(*_):
        choice = selected_var.get()
        idx = options.index(choice)
        rec = students[idx]
        for entry, val in zip(entries, rec):
            entry.delete(0, tk.END)
            entry.insert(0, str(val))

    selected_var.trace_add("write", populate_fields)
    populate_fields()

    def save_edit():
        idx = options.index(selected_var.get())
        stu_num = entries[0].get().strip()
        stu_name = entries[1].get().strip()

        if not stu_num or not stu_name:
            messagebox.showwarning("Missing Info", "Please enter both student number and name.", parent=dialog)
            return

        if any(i != idx and s[0] == stu_num for i, s in enumerate(students)):
            messagebox.showwarning("Duplicate ID", "Another student already uses this number.", parent=dialog)
            return

        try:
            cw1 = int(entries[2].get().strip())
            cw2 = int(entries[3].get().strip())
            cw3 = int(entries[4].get().strip())
            exam = int(entries[5].get().strip())
        except ValueError:
            messagebox.showwarning("Invalid Marks", "Marks must be whole numbers.", parent=dialog)
            return

        if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20 and 0 <= exam <= 100):
            messagebox.showwarning("Out of Range", "Coursework marks must be 0-20 and exam mark 0-100.", parent=dialog)
            return

        updated_student = [stu_num, stu_name, cw1, cw2, cw3, exam]
        students[idx] = updated_student

        if saveStudents():
            output.delete("1.0", tk.END)
            output.insert(tk.END, "Student record updated successfully!\n\n")
            output.insert(tk.END, displayStudent(updated_student))
            dialog.destroy()

    tk.Button(
        dialog,
        text="Update Record",
        command=save_edit,
        font=("Arial", 9, "bold"),
        bg="#FFFFFF",
        fg="#C76D7E",
        relief="flat",
        bd=1,
        width=18
    ).pack(pady=12)


#This will create the main application window!
root = tk.Tk()
root.title("Student Manager")
win_w, win_h = 960, 540
root.geometry(f"{win_w}x{win_h}")
root.resizable(False, False)
root.configure(bg="#FFD6E7")

cut_path = os.path.join(os.path.dirname(__file__), "cut.png")
cut_pil = Image.open(cut_path).resize((32, 32), Image.Resampling.LANCZOS)
cut_icon = ImageTk.PhotoImage(cut_pil)
root.iconphoto(True, cut_icon)

bg_path = os.path.join(os.path.dirname(__file__), "m.png")
bg_image = Image.open(bg_path).resize((win_w, win_h), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=win_w, height=win_h, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

controls_frame = tk.Frame(root, bg="#FCE4EC")
controls_frame.place(x=675, y=68, width=240, height=360)

title_label = tk.Label(
    controls_frame,
    text="Student Manager",
    font=("Arial", 16, "bold"),
    bg="#FCE4EC",
    fg="#C76D7E"
)
title_label.pack(pady=(6, 4))

search_label = tk.Label(
    controls_frame,
    text="Enter student name or number:",
    font=("Arial", 9),
    bg="#FCE4EC",
    fg="#8E4A59"
)
search_label.pack()

search_entry = tk.Entry(controls_frame, font=("Arial", 10), width=22, bg="#FFFFFF", fg="#333333")
search_entry.pack(pady=(3, 8))

#Creates the menu buttons!
button_style = {
    "font": ("Arial", 9, "bold"),
    "bg": "#FFFFFF",
    "fg": "#C76D7E",
    "activebackground": "#FFF5F8",
    "activeforeground": "#A85062",
    "relief": "flat",
    "bd": 1,
    "width": 24
}

tk.Button(controls_frame, text="View All Student Records",
          command=viewAll, **button_style).pack(pady=3)

tk.Button(controls_frame, text="View Individual Student",
          command=viewIndividual, **button_style).pack(pady=3)

tk.Button(controls_frame, text="Highest Overall Mark",
          command=highestStudent, **button_style).pack(pady=3)

tk.Button(controls_frame, text="Lowest Overall Mark",
          command=lowestStudent, **button_style).pack(pady=3)

tk.Button(controls_frame, text="Add New Student",
          command=addStudent, **button_style).pack(pady=3)

tk.Button(controls_frame, text="Edit Student Record",
          command=editStudent, **button_style).pack(pady=3)

#This displays the results!
output_frame = tk.Frame(root, bg="#FFFFFF")
output_frame.place(x=62, y=80, width=545, height=375)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

output = tk.Text(
    output_frame,
    font=("Arial", 10),
    bg="#FFFFFF",
    fg="#333333",
    relief="flat",
    bd=0,
    wrap="word",
    yscrollcommand=scrollbar.set
)
output.pack(side="left", fill="both", expand=True)
scrollbar.config(command=output.yview)

loadStudents()

root.mainloop()
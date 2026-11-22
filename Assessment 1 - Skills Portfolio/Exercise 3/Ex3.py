
import tkinter as tk
import os

students = []

#this will read student information from the text file!
def loadStudents():
    global students

    file_path = os.path.join(os.path.dirname(__file__), "studentMarks.txt")

    try:
        file = open(file_path, "r")
        lines = file.readlines()
        file.close()

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

#This eill find the student with the highest overall mark!
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


#This will create the main application window!
root = tk.Tk()
root.title("Student Manager")
root.geometry("650x650")
root.configure(bg="#FFF0F3")

title_label = tk.Label(
    root,
    text="Student Manager",
    font=("Arial", 24, "bold"),
    bg="#FFF0F3",
    fg="#C76D7E"
)
title_label.pack(pady=15)

search_label = tk.Label(
    root,
    text="Enter student name or number:",
    font=("Arial", 12),
    bg="#FFF0F3"
)
search_label.pack()

search_entry = tk.Entry(root, font=("Arial", 12), width=30)
search_entry.pack(pady=8)

#Creates the menu buttons!
button_style = {
    "font": ("Arial", 11),
    "bg": "#F4ACB7",
    "width": 30
}

tk.Button(root, text="View All Student Records",
          command=viewAll, **button_style).pack(pady=5)

tk.Button(root, text="View Individual Student",
          command=viewIndividual, **button_style).pack(pady=5)

tk.Button(root, text="Highest Overall Mark",
          command=highestStudent, **button_style).pack(pady=5)

tk.Button(root, text="Lowest Overall Mark",
          command=lowestStudent, **button_style).pack(pady=5)

#This displays the results!
output = tk.Text(root, height=18, width=65, font=("Arial", 10))
output.pack(pady=15)

loadStudents()

root.mainloop()

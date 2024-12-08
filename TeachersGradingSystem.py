from colorama import Fore
import os, csv
 
# Global variables to store student data, subjects, and their records
students_list = []  # List of students
students_record = {}  # Dictionary to store student records, keyed by student names
subjects_set = set()  # Set to store unique subjects
 
# Initializing the "Students Records" key in the dictionary
students_record["Students Records"] = []
 
 
def init():
    """
    Initializes the application by checking and loading existing data from CSV files.
    Ensures the necessary files are created if they don't already exist.
    """
    global subjects_set, students_list, students_record
 
    # Handle 'subjects.csv': Create if not exists, or load data if it exists
    try:
        open("subjects.csv", "x").close()  # Create the file
    except FileExistsError:
        if os.path.getsize("subjects.csv") > 0:  # Load if file has data
            with open("subjects.csv", newline='', mode='r') as subjects_file:
                reader = csv.reader(subjects_file, delimiter=';')
                for row in reader:
                    subjects_set.update(row)  # Update subjects_set with data
 
    # Handle 'students.csv': Create if not exists, or load data if it exists
    try:
        open("students.csv", "x").close()
    except FileExistsError:
        if os.path.getsize("students.csv") > 0:
            with open("students.csv", newline='', mode='r') as students_file:
                reader = csv.reader(students_file, delimiter=';')
                for row in reader:
                    students_list.extend(row)  # Add loaded student names to the list
 
    # Handle 'students_record.csv': Create if not exists, or load data if it exists
    try:
        open("students_record.csv", "x").close()
    except FileExistsError:
        if os.path.getsize("students_record.csv") > 0:
            with open("students_record.csv", newline='', mode='r') as record_file:
                reader = csv.reader(record_file, delimiter=';')
                first_row = next(reader)
                students_record[first_row[0]] = first_row[1:]  # Add header subjects
 
                # Load student data row by row
                for row in reader:
                    key = row[0]  # Student name
                    # Safely handle non-integer grades
                    values = [int(value) if value.isdigit() else value for value in row[1:]]
                    students_record[key] = values
 
 
def display_menu():
    """
    Displays the main menu and prompts the user to choose an option.
    Routes the user to the corresponding function based on their input.
    """
    print(Fore.RED + "#### Welcome to main menu ####")
    print(Fore.BLUE + "Please input the number corresponding to the option you wish to use.")
    print(Fore.WHITE + "1. Add Students")
    print("2. Add Subject")
    print("3. Remove Subject")
    print("4. Input grades")
    print("5. Print record")
    user_choice = input("Please input a number, or Q to close the program : ")
    match user_choice:
        case "1":
            add_student()
        case "2":
            add_subject()
        case "3":
            del_subject()
        case "4":
            input_grades()
        case "5":
            print_record()
        case "q" | "Q":
            close_program()
        case _:
            print("This entry is unsupported. Please input a supported answer.")
            display_menu()
 
 
def new_action():
    """
    Asks the user if they want to perform another action.
    """
    user_choice = input("Do you want to do another action ? (Y/N) ")
    while user_choice not in ["Y", "y", "N", "n"]:
        user_choice = input("Unsupported answer. Please reply with Y or N. ")
    match user_choice:
        case "Y" | "y":
            display_menu()
        case "N" | "n":
            close_program()
 
 
def add_student():
    """
    Adds new students to the records. Ensures that new students have entries for all existing subjects.
    """
    nb_students =input("How many students do you want to add? ")
    try:    
        for x in range(int(nb_students)):
            student_name = input(f"Enter the name of Student {x+1}: ") 
            students_list.append(student_name)  # Add student to the list
            # Initialize their grades with "N/A" for all subjects
            students_record[student_name] = ["N/A"] * len(students_record["Students Records"])
        print("Added all students to the list.")
        new_action()
 
    except ValueError:
        print('Unsupported Answer Please Try Again. ')
        add_student()
 
 
 
def add_subject():
    """
    Adds a new subject to the subjects list and updates all student records accordingly.
    """
    new_subject = input("What subject do you want to add ? ")
    if new_subject not in subjects_set:
        subjects_set.add(new_subject)  # Add the new subject
        students_record["Students Records"].append(new_subject)  # Add subject to header
        # Add "N/A" for the new subject to all students
        for student in students_list:
            students_record[student].append("N/A")
        print("Subject added successfully.")
    new_action()
 
 
def del_subject():
    """
    Deletes a subject from the subjects list and updates all student records.
    """
    print("Available subjects:")
    for subject in subjects_set:
        print(subject)
 
    del_subject = input("Type the subject you want to delete (! THIS IS CASE SENSITIVE !): ")
    if del_subject in subjects_set:
        subjects_set.remove(del_subject)  # Remove the subject from the set
        students_record["Students Records"].remove(del_subject)  # Remove from header
        print("Subject deleted.")
    else:
        print("Subject not found.")
    new_action()
 
 
def input_grades():
    """
    Allows the user to input grades for a specific subject for all students.
    """
    if len(subjects_set) == 0:
        print("No subjects. Please add subjects before adding grades.")
        new_action()
        return
    elif len(students_list) == 0:
        print("No students. Please add students before adding grades.")
        new_action()
        return
 
    print("Available subjects:")
    for subject in subjects_set:
        print(subject)
 
    grade_subject = input("Input the subject you want to add a grade for (! THIS IS CASE SENSITIVE !): ")
    if grade_subject not in subjects_set:
        print("Subject does not exist.")
        new_action()
        return
 
    # Get the index of the subject in the records
    subject_index = students_record["Students Records"].index(grade_subject)
    for student in students_list:
        new_grade = input(f"Input grade for {student}: ")
        students_record[student][subject_index] = new_grade if new_grade else "N/A"
 
    print("Grades added.")
    new_action()
 
 
def print_record():
    """
    Prints the records of all students in a tabular format.
    """
    subjects = students_record.get("Students Records", [])
    if not subjects:
        print("No subjects found.")
        return
 
    if not students_record or len(students_record) <= 1:
        print("No student records found.")
        return
 
    # Determine the column width dynamically based on the longest entry
    column_width = max(
        max((len(str(item)) for item in subjects), default=0),
        max((len(str(student)) for student in students_record if student != "Students Records"), default=0),
        8
    )
    header = ["Student"] + subjects
    table_width = (column_width + 3) * len(header) + 1
 
    # Print table with borders
    print(f"┌{'─' * (table_width - 2)}┐")
    print("│" + "".join(f" {header[i]:<{column_width}} │" for i in range(len(header))))
    print(f"├{'─' * (table_width - 2)}┤")
 
    for student, grades in students_record.items():
        if student != "Students Records":
            row = [student] + [str(grade) for grade in grades]
            row_display = "│" + "".join(f" {str(row[i]):<{column_width}} │" for i in range(len(row)))
            print(row_display)
 
    print(f"└{'─' * (table_width - 2)}┘")
    new_action()
 
 
def close_program():
    """
    Asks the user whether to save changes before exiting the program.
    """
    user_choice = input("Do you want to save changes? (Y/N): ").strip().lower()
 
    if user_choice == 'y':
        try:
            # Save student records to 'students_record.csv'
            with open("students_record.csv", mode="w", newline='') as record_file:
                writer = csv.writer(record_file, delimiter=';')
                writer.writerow(["Students Records"] + students_record["Students Records"])  # Header
                for student, grades in students_record.items():
                    if student != "Students Records":
                        writer.writerow([student] + grades)
 
            # Save subjects to 'subjects.csv'
            with open("subjects.csv", mode="w", newline='') as subjects_file:
                writer = csv.writer(subjects_file, delimiter=';')
                writer.writerow(subjects_set)
 
            # Save students to 'students.csv'
            with open("students.csv", mode="w", newline='') as students_file:
                writer = csv.writer(students_file, delimiter=';')
                writer.writerow(students_list)  # Save student names
 
            print("Changes saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving: {e}")
    elif user_choice == 'n':
        print("Exiting without saving.")
    else:
        print("Invalid input. Please enter 'Y' or 'N'.")
        close_program()  # Recursively call to ensure valid input
 
    exit()  # Exit the program
 
 
# Initialize the program by loading or creating the necessary data files
init()
 
# Start the menu-driven interface
display_menu()
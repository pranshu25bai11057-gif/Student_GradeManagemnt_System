import json
import os

try:
    from tabulate import tabulate
    tabulate_available = True
except ImportError:
    tabulate_available = False
    
    
    def tabulate(data, headers, tablefmt):
        
        header_line = " | ".join(headers)
        separator = "-" * len(header_line)
        rows = "\n".join([" | ".join(map(str, row)) for row in data])
        return f"\n{header_line}\n{separator}\n{rows}"
    
    print(" WARNING: 'tabulate' library not found. Install it using 'pip install tabulate' for better formatting.")

data_file = 'students.json'

def load_data():
    
    if not os.path.exists(data_file):
        return []
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        
        print(f"Warning: Data file '{data_file}' is empty or invalid. Starting with no records.")
        return []

def save_data(data):
    
    try:
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error: Could not save data to file {data_file}. Details: {e}")

def calculate_grade(percentage):
    
    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    else:
        return 'F'

def add_student():
    
    data = load_data()
    
    student_id = input("Enter Student ID: ").strip()

    for s in data:
        if s['id'] == student_id:
            print("Error: Student ID already exists!")
            return

    name = input("Enter Student Name: ").strip()
    class_name = input("Enter Class/Section: ").strip()

    subjects = {}
    try:
        n_subjects_input = input("How many subjects? ")
        if not n_subjects_input.isdigit():
             print("Invalid input for number of subjects. Operation cancelled.")
             return
        n_subjects = int(n_subjects_input)
    except ValueError:
        
        print("Invalid number of subjects. Operation cancelled.")
        return

    for i in range(n_subjects):
        while True:
            sub = input(f"Subject {i+1} name: ").strip()
            if not sub:
                print("Subject name cannot be empty.")
                continue
                
            try:
                marks_input = input(f"Marks for {sub} (0-100): ")
                marks = int(marks_input)
                if 0 <= marks <= 100:
                    subjects[sub] = marks
                    break
                else:
                    print("Marks must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number for marks.")

    if not subjects:
        print("No subjects added. Record saved with no marks.")
        total = 0
        percentage = 0.0
    else:
        total = sum(subjects.values())
        percentage = total / len(subjects)

    grade = calculate_grade(percentage)

    student = {
        'id': student_id,
        'name': name,
        'class': class_name,
        'subjects': subjects,
        'total': total,
        'percentage': percentage,
        'grade': grade
    }

    data.append(student)
    save_data(data)
    print("Student added successfully!\n")

def view_all_students():
    
    data = load_data()
    if not data:
        print("No student records found!")
        return

    table = []
    for s in data:
        
        percent = s.get('percentage', 0.0)
        grade = s.get('grade', 'N/A')
        table.append([
            s['id'], s['name'], s['class'], f"{percent:.2f}%", grade
        ])

    print("\n--- All Students ---")
    
    table_format = "grid" if tabulate_available else "simple"
    print(tabulate(table, headers=["ID", "Name", "Class", "Percent", "Grade"], tablefmt=table_format))
    print()

def search_student():
    
    data = load_data()
    sid = input("Enter Student ID to search: ").strip()

    for s in data:
        if s['id'] == sid:
            print("\n--- Student Record ---")
            print(json.dumps(s, indent=4))
            print()
            return

    print("Student not found!\n")

def update_marks():
    
    data = load_data()
    sid = input("Enter Student ID to update: ").strip()
    student_found = False

    for s in data:
        if s['id'] == sid:
            student_found = True
            print(f"Updating marks for: {s['name']}")
            
            if not s.get('subjects'):
                print("No subjects found for this student. Cannot update marks.")
                return

            print("Current subjects:")
            for sub, mark in s['subjects'].items():
                print(f"  {sub}: {mark}")

            subject = input("Enter subject name to update: ").strip()
            if subject not in s['subjects']:
                print("Subject not found for this student!\n")
                return

            while True:
                try:
                    new_mark_input = input("Enter new marks (0-100): ")
                    new_mark = int(new_mark_input)
                    if 0 <= new_mark <= 100:
                        break
                    else:
                        print("Marks must be between 0 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a number for marks.")
            
            s['subjects'][subject] = new_mark

             
            s['total'] = sum(s['subjects'].values())
            
            if s['subjects']:
                s['percentage'] = s['total'] / len(s['subjects'])
                p = s['percentage']
                s['grade'] = calculate_grade(p)
            else:
                 s['percentage'] = 0.0
                 s['grade'] = 'F' 
            save_data(data)
            print("Marks updated successfully!\n")
            return

    if not student_found:
        print("Student not found!\n")

def delete_student():
    
    data = load_data()
    sid = input("Enter Student ID to delete: ").strip()

    new_data = [s for s in data if s['id'] != sid]

    if len(new_data) == len(data):
        print("Student not found!\n")
    else:
        save_data(new_data)
        print("Record deleted successfully!\n")

def menu():
    
    while True:
        print("\n===== Student Grade Management System =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Marks")
        print("5. Delete Student")
        print("6. Exit")

        try:
            
            choice = input("Enter your choice: ").strip()
        except EOFError:
            print("\n Input stream closed (EOF). Exiting non-interactively.")
            break

        if choice == '1':
            add_student()
        elif choice == '2':
            view_all_students()
        elif choice == '3':
            search_student()
        elif choice == '4':
            update_marks()
        elif choice == '5':
            delete_student()
        elif choice == '6':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice! Try again.\n")

if __name__ == "__main__":
    menu()
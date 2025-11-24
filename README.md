# Student_GradeManagemnt_System
• Project Title
Student Grade Management System
• Overview
This project is a command-line based application that helps manage
student academic records.
Users can add students, assign marks, calculate grades, view all
records, update marks, search, and delete student data.
Data is stored in a JSON file for persistence.
• Features
- Add new students
- View all student records
- Search student by ID
- Update marks for any subject
- Delete student records
- Auto-calculation of percentage and grade
- Safe handling of invalid inputs and missing data
- JSON-based data storage
• Technologies/Tools Used
- Python 3
- JSON for data storage
- ReportLab (for generating README PDF)
- Tabulate (optional, for formatted table display)
• Steps to Install & Run the Project
1. Ensure Python is installed on your system.
2. Install required libraries:
- `pip install tabulate`
3. Place the script and `students.json` (optional) in the same directory.
4. Run the program:
- `python student_grade_system.py`
• Instructions for Testing
1. Choose option **1** to add a student.
2. Choose option **2** to view all students.
3. Use option **3** to search for a student by ID.
4. Option **4** allows updating marks.
5. Option **5** deletes a student record.
6. Verify that changes persist in the `students.json` file.

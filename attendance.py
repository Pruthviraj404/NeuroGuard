from datetime import datetime
import openpyxl
import os

excel_file = 'attendance.xlsx'

# Load or create the Excel workbook
if os.path.exists(excel_file):
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook.active
else:
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(['Student Name', 'Timestamp'])  # Add header row
    workbook.save(excel_file)  # Save the newly created file

# Keep track of students already marked during the current session
marked_students = set()

def mark_attendance(student_name):
    if student_name == "Unknown":
        return  # Ignore unknown names

    if student_name not in marked_students:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sheet.append([student_name, timestamp])
        workbook.save(excel_file)
        marked_students.add(student_name)  # Add student to the session's marked list
        print("Attendance Marked:", student_name)
    else:
        print(f"Attendance for {student_name} already marked in this session.")


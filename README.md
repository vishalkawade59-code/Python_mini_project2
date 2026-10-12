# Advanced Student Management & Academic Information System

A Python-based Student Management System for managing student records, academic marks, attendance, statistics, reports, exports, authentication, and backups.

## Features

- Add, search, update, and delete student records
- JSON-based permanent data storage
- Student marks management
- Total marks and percentage calculation
- Grade and Pass/Fail calculation
- Student ranking
- Search by roll number, name, and department
- Student sorting
- Academic statistics
- Attendance management
- Low-attendance warnings
- Student, class, and department reports
- CSV export
- TXT export
- PDF export
- Admin and viewer login system
- Password hashing
- Admin-only operations
- Automatic and manual backups
- Backup restoration
- Input validation and error handling

## Technologies Used

- Python
- JSON
- CSV
- File Handling
- SHA-256 Hashing
- Regular Expressions
- PDF generation
- Git
- GitHub

## Project Structure

```text
Student-Record-Management-System/
│
├── programs/
│   └── student_record_system.py
│
├── backups/
├── exports/
├── students.json
├── .gitignore
├── README.md
└── other project documentation

## Function Documentation

The system contains approximately 85 functions organized into 10 functional groups.

### 1. File Handling

- `hash_password` — Converts passwords into SHA-256 hashes.
- `normalize` — Fills missing fields in older student records.
- `read_students_file` — Reads and validates student data from the JSON file.
- `save_students` — Safely saves student data to `students.json`.

### 2. Input & Validation

- `get_number` — Accepts numbers with range validation.
- `get_roll_number` — Accepts and validates roll numbers.
- `get_marks` — Accepts marks between 0 and 100.
- `get_text` — Accepts and validates text input.
- `get_gender` — Validates gender input.
- `ask_yes_no` — Accepts Yes/No confirmation.
- `valid_email` — Validates email format.
- `valid_phone` — Validates a 10-digit phone number.
- `valid_dob` — Validates date of birth.
- `require_admin` — Restricts protected operations to administrators.

### 3. Calculations

- `find_student` — Finds a student using roll number.
- `pick_student` — Selects a student interactively.
- `has_marks` — Checks whether all subject marks are available.
- `total_marks` — Calculates total marks.
- `percentage` — Calculates percentage.
- `grade_for` — Determines grade from percentage.
- `result_for` — Determines Pass/Fail status.
- `attendance_percentage` — Calculates attendance percentage.
- `fmt_pct` — Formats percentage output.
- `fmt_num` — Formats numerical output.
- `students_with_marks` — Returns students whose marks are complete.
- `ranked_students` — Generates student rankings and gives equal ranks to students with equal percentages.

### 4. Display & Reports

- `student_table` — Creates formatted student tables.
- `print_student` — Displays complete student details.
- `build_report` — Builds a report for an individual student.
- `class_report_lines` — Builds class report content.
- `department_report_lines` — Builds department report content.

### 5. Student Operations

- `add_student` — Adds a new student.
- `get_all_marks` — Collects marks for all subjects.
- `search_by_roll` — Searches by roll number.
- `search_by_name` — Searches by student name.
- `search_by_department` — Searches by department.
- `show_matches` — Displays matching students.
- `display_students` — Displays all students.
- `sort_students` — Sorts student records.
- `count_students` — Counts total students.
- `update_details` — Updates personal details.
- `update_marks` — Updates student marks.
- `update_student` — Provides the student update submenu.
- `delete_student` — Deletes a student after confirmation.
- `student_report` — Displays an individual student report.

### 6. Statistics

- `need_marks` — Checks whether marks are available.
- `highest_scorer` — Finds the highest scorer.
- `lowest_scorer` — Finds the lowest scorer.
- `class_average` — Calculates class average.
- `department_average` — Calculates department averages.
- `pass_fail_count` — Counts Pass and Fail students.
- `grade_count` — Counts students by grade.
- `rank_list` — Displays the ranked student list.
- `statistics_menu` — Provides the academic statistics menu.

### 7. Attendance

- `update_attendance` — Updates student attendance and warns below 75%.
- `view_attendance` — Displays a student's attendance.
- `low_attendance_list` — Lists students below the attendance threshold.
- `attendance_menu` — Provides the attendance menu.

### 8. Export & Reports

- `stamp` — Generates timestamps for filenames.
- `export_text` — Exports content to TXT.
- `export_pdf` — Exports content to PDF.
- `write_simple_pdf` — Generates a simple PDF file.
- `export_csv` — Exports student data to CSV.
- `export_class_text` — Exports the class report to TXT.
- `export_class_pdf` — Exports the class report to PDF.
- `export_student_report` — Exports an individual student report.
- `show_class_report` — Displays the class report.
- `show_department_report` — Displays the department report.
- `reports_menu` — Provides the reports and export menu.

### 9. Backup & Recovery

- `create_backup` — Creates a backup of student data.
- `manual_backup` — Creates a backup manually.
- `list_backups` — Lists available backup files.
- `show_backups` — Displays available backups.
- `backup_time` — Formats backup timestamps.
- `restore_backup` — Restores a selected backup and requires admin access.
- `backup_menu` — Provides the backup and recovery menu.

### 10. Menus & Login

- `run_menu` — Reusable submenu engine.
- `search_menu` — Provides search and view options.
- `print_main_menu` — Displays the main menu.
- `read_password` — Handles password input.
- `login` — Handles authentication with a maximum of three attempts.
- `main` — Starts and controls the main program flow.
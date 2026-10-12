"""Advanced Student Management & Academic Information System.

Features: student records, marks/percentage/grade, statistics, rank,
search, sorting, attendance, reports, CSV/TXT/PDF export, admin login,
backup & restore.

Default logins (change them in USERS below):
    admin / admin123   -> full access
    staff / staff123   -> view-only
"""

import csv
import getpass
import hashlib
import hmac
import json
import os
import re
import shutil
import sys
from datetime import datetime

# ---------------------------------------------------------------- constants
FILE_NAME = "students.json"
BACKUP_DIR = "backups"
EXPORT_DIR = "exports"
SUBJECTS = ["C Programming", "Python", "Mathematics", "Physics"]
MAX_MARKS = 100
PASS_PERCENTAGE = 40
LOW_ATTENDANCE = 75
MAX_LOGIN_ATTEMPTS = 3
HIDE_PASSWORD = False  # True kela tar password type kartana dista nahi (hidden)
GRADES = ["A+", "A", "B+", "B", "C", "F"]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


USERS = {
    "admin": {"password": hash_password("admin123"), "role": "admin"},
    "staff": {"password": hash_password("staff123"), "role": "viewer"},
}
current_user = {"name": None, "role": None}


# ------------------------------------------------------------ file handling
def normalize(student):
    """Fill missing fields so old records keep working."""
    for key in ("email", "phone", "gender", "address", "dob"):
        student.setdefault(key, "")
    student.setdefault("age", "")
    if not isinstance(student.get("marks"), dict):
        student["marks"] = {}
    if not isinstance(student.get("attendance"), dict):
        student["attendance"] = {"total_days": 0, "present_days": 0}
    return student


def read_students_file(path):
    """Return list of students from path, or None if file is unusable."""
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, list):
        return None
    clean = []
    for item in data:
        if isinstance(item, dict) and "roll_number" in item:
            item.setdefault("name", "")
            item.setdefault("department", "")
            clean.append(normalize(item))
    return clean


def save_students():
    tmp = FILE_NAME + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
        os.replace(tmp, FILE_NAME)
    except OSError as error:
        print("Could not save data:", error)


students = read_students_file(FILE_NAME) or []


# --------------------------------------------------------------- input help
def get_number(prompt, low, high, cast=int):
    while True:
        try:
            value = cast(input(prompt).strip())
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        if low <= value <= high:
            return value
        print(f"Value must be between {low} and {high}.")


def get_roll_number(prompt="Enter Roll Number: "):
    return get_number(prompt, 1, 10**9)


def get_marks(prompt):
    value = get_number(prompt, 0, MAX_MARKS, float)
    return int(value) if value.is_integer() else value


def get_text(prompt, validator=None, error="Invalid input!"):
    while True:
        value = input(prompt).strip()
        if not value:
            print("This field cannot be empty!")
        elif validator and not validator(value):
            print(error)
        else:
            return value


def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please enter y or n.")


def valid_email(value):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value) is not None


def valid_phone(value):
    return value.isascii() and value.isdigit() and len(value) == 10


def valid_dob(value):
    try:
        return datetime.strptime(value, "%d-%m-%Y") <= datetime.now()
    except ValueError:
        return False


def get_gender(prompt="Enter Gender (M/F/O): "):
    options = {"m": "Male", "f": "Female", "o": "Other"}
    while True:
        value = input(prompt).strip().lower()
        if value in options:
            return options[value]
        print("Enter M, F or O.")


# (key, label, function that asks for the value)
FIELDS = [
    ("name", "Name", lambda: get_text("Enter Name: ")),
    ("department", "Department", lambda: get_text("Enter Department: ")),
    ("email", "Email", lambda: get_text("Enter Email: ", valid_email, "Invalid email!")),
    ("phone", "Phone", lambda: get_text("Enter Phone (10 digits): ", valid_phone, "Phone must be 10 digits!")),
    ("gender", "Gender", get_gender),
    ("age", "Age", lambda: get_number("Enter Age: ", 1, 120)),
    ("address", "Address", lambda: get_text("Enter Address: ")),
    ("dob", "Date of Birth", lambda: get_text("Enter Date of Birth (DD-MM-YYYY): ", valid_dob, "Invalid date! Use DD-MM-YYYY.")),
]


def require_admin():
    if current_user["role"] != "admin":
        print("Access denied! Only admin can do this.")
        return False
    return True


# ------------------------------------------------------------ calculations
def find_student(roll_number):
    for student in students:
        if student["roll_number"] == roll_number:
            return student
    return None


def pick_student(prompt="Enter Roll Number: "):
    student = find_student(get_roll_number(prompt))
    if student is None:
        print("Student not found!")
    return student


def has_marks(student):
    return all(subject in student["marks"] for subject in SUBJECTS)


def total_marks(student):
    return sum(student["marks"].get(subject, 0) for subject in SUBJECTS)


def percentage(student):
    if not has_marks(student):
        return None
    return total_marks(student) / (len(SUBJECTS) * MAX_MARKS) * 100


def grade_for(pct):
    if pct is None:
        return "-"
    if pct >= 90:
        return "A+"
    if pct >= 80:
        return "A"
    if pct >= 70:
        return "B+"
    if pct >= 60:
        return "B"
    if pct >= PASS_PERCENTAGE:
        return "C"
    return "F"


def result_for(pct):
    if pct is None:
        return "-"
    return "Pass" if pct >= PASS_PERCENTAGE else "Fail"


def attendance_percentage(student):
    att = student["attendance"]
    if att.get("total_days", 0) <= 0:
        return None
    return att["present_days"] / att["total_days"] * 100


def fmt_pct(pct):
    return "-" if pct is None else f"{pct:.2f}%"


def fmt_num(value):
    return f"{value:g}"


def students_with_marks():
    return [s for s in students if has_marks(s)]


def ranked_students():
    """List of (rank, student); equal percentages share a rank."""
    ordered = sorted(students_with_marks(), key=percentage, reverse=True)
    ranked = []
    for index, student in enumerate(ordered):
        if index > 0 and percentage(student) == percentage(ordered[index - 1]):
            rank = ranked[-1][0]
        else:
            rank = index + 1
        ranked.append((rank, student))
    return ranked


# -------------------------------------------------------------- display help
def student_table(student_list, with_rank=None):
    lines = []
    head = f"{'Roll':<8}{'Name':<20}{'Department':<16}{'Total':>7}{'Percent':>10}{'Grade':>6}"
    if with_rank:
        head = f"{'Rank':<6}" + head
    lines.append(head)
    lines.append("-" * len(head))
    for item in student_list:
        rank, student = item if with_rank else (None, item)
        pct = percentage(student)
        total = fmt_num(total_marks(student)) if pct is not None else "-"
        row = (f"{student['roll_number']:<8}{student['name'][:19]:<20}"
               f"{student['department'][:15]:<16}{total:>7}{fmt_pct(pct):>10}"
               f"{grade_for(pct):>6}")
        if with_rank:
            row = f"{rank:<6}" + row
        lines.append(row)
    return lines


def print_student(student):
    print("--------------------")
    print("Roll Number :", student["roll_number"])
    for key, label, _ in FIELDS:
        print(f"{label:<12}: {student[key] or '-'}")
    if has_marks(student):
        for subject in SUBJECTS:
            print(f"{subject:<14}: {fmt_num(student['marks'][subject])}")
        pct = percentage(student)
        print("Total       :", fmt_num(total_marks(student)))
        print("Percentage  :", fmt_pct(pct))
        print("Grade       :", grade_for(pct))
        print("Result      :", result_for(pct))
    else:
        print("Marks       : not entered")
    print("Attendance  :", fmt_pct(attendance_percentage(student)))


def build_report(student):
    line = "=" * 32
    out = [line, "       STUDENT REPORT", line, "",
           f"Roll Number : {student['roll_number']}"]
    for key, label, _ in FIELDS:
        out.append(f"{label:<12}: {student[key] or '-'}")
    out += ["", "Marks"]
    if has_marks(student):
        for subject in SUBJECTS:
            out.append(f"{subject:<14}: {fmt_num(student['marks'][subject])}")
        pct = percentage(student)
        out += ["", f"Total         : {fmt_num(total_marks(student))}",
                f"Percentage    : {fmt_pct(pct)}",
                f"Grade         : {grade_for(pct)}",
                f"Result        : {result_for(pct)}"]
    else:
        out.append("Marks not entered yet")
    att = student["attendance"]
    out.append("")
    if att.get("total_days", 0) > 0:
        out += [f"Total Days    : {att['total_days']}",
                f"Present       : {att['present_days']}",
                f"Absent        : {att['total_days'] - att['present_days']}",
                f"Attendance    : {fmt_pct(attendance_percentage(student))}"]
        if attendance_percentage(student) < LOW_ATTENDANCE:
            out.append(f"WARNING: Attendance below {LOW_ATTENDANCE}%")
    else:
        out.append("Attendance    : not entered")
    out.append(line)
    return out


def class_report_lines():
    rated = students_with_marks()
    lines = ["=" * 60, "CLASS REPORT", "=" * 60,
             f"Total students      : {len(students)}",
             f"Students with marks : {len(rated)}"]
    if rated:
        pcts = [percentage(s) for s in rated]
        passed = sum(1 for p in pcts if p >= PASS_PERCENTAGE)
        lines += [f"Class average       : {fmt_pct(sum(pcts) / len(pcts))}",
                  f"Highest             : {fmt_pct(max(pcts))}",
                  f"Lowest              : {fmt_pct(min(pcts))}",
                  f"Pass / Fail         : {passed} / {len(pcts) - passed}"]
        counts = {g: 0 for g in GRADES}
        for p in pcts:
            counts[grade_for(p)] += 1
        lines.append("Grades              : " + ", ".join(f"{g}={counts[g]}" for g in GRADES))
        lines.append("")
        lines += student_table(ranked_students(), with_rank=True)
    return lines


def department_report_lines(department):
    members = [s for s in students if s["department"].lower() == department.lower()]
    lines = ["=" * 60, f"DEPARTMENT REPORT: {department}", "=" * 60,
             f"Students: {len(members)}"]
    rated = [s for s in members if has_marks(s)]
    if rated:
        avg = sum(percentage(s) for s in rated) / len(rated)
        lines.append(f"Average : {fmt_pct(avg)}")
    if members:
        lines.append("")
        lines += student_table(members)
    return lines


# --------------------------------------------------------------- operations
def add_student():
    roll_number = get_roll_number()
    if find_student(roll_number):
        print("A student with this roll number already exists!")
        return
    student = {"roll_number": roll_number}
    for key, _, ask in FIELDS:
        student[key] = ask()
    student["marks"] = {}
    student["attendance"] = {"total_days": 0, "present_days": 0}
    if ask_yes_no("Enter marks now? (y/n): "):
        student["marks"] = get_all_marks()
    students.append(student)
    save_students()
    print("Student added successfully!")


def get_all_marks():
    return {s: get_marks(f"Enter {s} marks (0-{MAX_MARKS}): ") for s in SUBJECTS}


def search_by_roll():
    student = pick_student("Enter Roll Number to Search: ")
    if student:
        print("Student Found!")
        print_student(student)


def search_by_name():
    query = get_text("Enter Name (full or part): ").lower()
    found = [s for s in students if query in s["name"].lower()]
    show_matches(found)


def search_by_department():
    query = get_text("Enter Department: ").lower()
    found = [s for s in students if s["department"].lower() == query]
    show_matches(found)


def show_matches(found):
    if not found:
        print("No students found!")
        return
    print(f"{len(found)} student(s) found:")
    for student in found:
        print_student(student)


def display_students():
    if not students:
        print("No student records found!")
        return
    print()
    print("\n".join(student_table(students)))


def sort_students():
    options = {
        "1": ("Roll Number", lambda s: s["roll_number"], False),
        "2": ("Name", lambda s: s["name"].lower(), False),
        "3": ("Percentage (high to low)",
              lambda s: -1 if percentage(s) is None else percentage(s), True),
        "4": ("Department", lambda s: (s["department"].lower(), s["roll_number"]), False),
    }
    for key, (label, _, _) in options.items():
        print(f"{key}. Sort by {label}")
    choice = input("Enter your choice: ").strip()
    if choice not in options:
        print("Invalid choice!")
        return
    _, key_func, reverse = options[choice]
    if not students:
        print("No student records found!")
        return
    print()
    print("\n".join(student_table(sorted(students, key=key_func, reverse=reverse))))


def count_students():
    print("Total Students:", len(students))


def update_details():
    if not require_admin():
        return
    student = pick_student("Enter Roll Number to Update: ")
    if not student:
        return
    for number, (_, label, _) in enumerate(FIELDS, 1):
        print(f"{number}. {label}")
    choice = get_number("Which field to update (1-8): ", 1, len(FIELDS))
    key, label, ask = FIELDS[choice - 1]
    student[key] = ask()
    save_students()
    print(f"{label} updated successfully!")


def update_marks():
    if not require_admin():
        return
    student = pick_student("Enter Roll Number to Update Marks: ")
    if not student:
        return
    for number, subject in enumerate(SUBJECTS, 1):
        current = student["marks"].get(subject, "-")
        print(f"{number}. {subject} (current: {current})")
    print(f"{len(SUBJECTS) + 1}. All subjects")
    choice = get_number("Enter your choice: ", 1, len(SUBJECTS) + 1)
    if choice == len(SUBJECTS) + 1:
        student["marks"] = get_all_marks()
    else:
        subject = SUBJECTS[choice - 1]
        student["marks"][subject] = get_marks(f"Enter {subject} marks (0-{MAX_MARKS}): ")
    save_students()
    print("Marks updated successfully!")


def update_student():
    options = [("Update personal details", update_details), ("Update marks", update_marks)]
    run_menu("UPDATE STUDENT", options)


def delete_student():
    if not require_admin():
        return
    student = pick_student("Enter Roll Number to Delete: ")
    if student and ask_yes_no(f"Delete {student['name']}? (y/n): "):
        students.remove(student)
        save_students()
        print("Student deleted successfully!")


def student_report():
    student = pick_student("Enter Roll Number for Report: ")
    if student:
        print()
        print("\n".join(build_report(student)))


# --------------------------------------------------------------- statistics
def need_marks():
    rated = students_with_marks()
    if not rated:
        print("No student has marks yet!")
    return rated


def highest_scorer():
    rated = need_marks()
    if rated:
        best = max(rated, key=percentage)
        top = [s for s in rated if percentage(s) == percentage(best)]
        for s in top:
            print(f"Highest Scorer: {s['name']} (Roll {s['roll_number']}) - {fmt_pct(percentage(s))}")


def lowest_scorer():
    rated = need_marks()
    if rated:
        worst = min(rated, key=percentage)
        low = [s for s in rated if percentage(s) == percentage(worst)]
        for s in low:
            print(f"Lowest Scorer: {s['name']} (Roll {s['roll_number']}) - {fmt_pct(percentage(s))}")


def class_average():
    rated = need_marks()
    if rated:
        print("Class Average:", fmt_pct(sum(percentage(s) for s in rated) / len(rated)))


def department_average():
    rated = need_marks()
    groups = {}
    for s in rated:
        groups.setdefault(s["department"].lower(), []).append(s)
    for members in groups.values():
        avg = sum(percentage(s) for s in members) / len(members)
        print(f"{members[0]['department']:<20}: {fmt_pct(avg)} ({len(members)} student(s))")


def pass_fail_count():
    rated = need_marks()
    if rated:
        passed = sum(1 for s in rated if percentage(s) >= PASS_PERCENTAGE)
        print("Pass:", passed)
        print("Fail:", len(rated) - passed)


def grade_count():
    rated = need_marks()
    if rated:
        counts = {g: 0 for g in GRADES}
        for s in rated:
            counts[grade_for(percentage(s))] += 1
        for grade in GRADES:
            print(f"{grade:<3}: {counts[grade]}")


def rank_list():
    if need_marks():
        print()
        print("\n".join(student_table(ranked_students(), with_rank=True)))


def statistics_menu():
    run_menu("ACADEMIC STATISTICS", [
        ("Highest Scorer", highest_scorer),
        ("Lowest Scorer", lowest_scorer),
        ("Class Average", class_average),
        ("Department Average", department_average),
        ("Pass / Fail Count", pass_fail_count),
        ("Grade-wise Count", grade_count),
        ("Rank List", rank_list),
    ])


# --------------------------------------------------------------- attendance
def update_attendance():
    if not require_admin():
        return
    student = pick_student("Enter Roll Number: ")
    if not student:
        return
    total = get_number("Enter Total Days: ", 1, 366)
    present = get_number("Enter Present Days: ", 0, total)
    student["attendance"] = {"total_days": total, "present_days": present}
    save_students()
    pct = attendance_percentage(student)
    print(f"Total Days: {total}\nPresent: {present}\nAbsent: {total - present}\nAttendance: {fmt_pct(pct)}")
    if pct < LOW_ATTENDANCE:
        print(f"WARNING: Attendance below {LOW_ATTENDANCE}%")


def view_attendance():
    student = pick_student("Enter Roll Number: ")
    if not student:
        return
    pct = attendance_percentage(student)
    if pct is None:
        print("Attendance not entered yet.")
        return
    print(f"Attendance: {fmt_pct(pct)}")
    if pct < LOW_ATTENDANCE:
        print(f"WARNING: Attendance below {LOW_ATTENDANCE}%")


def low_attendance_list():
    low = [s for s in students
           if attendance_percentage(s) is not None and attendance_percentage(s) < LOW_ATTENDANCE]
    if not low:
        print(f"No student below {LOW_ATTENDANCE}% attendance.")
        return
    for s in low:
        print(f"{s['roll_number']:<8}{s['name']:<20}{fmt_pct(attendance_percentage(s))}")


def attendance_menu():
    run_menu("ATTENDANCE", [
        ("Update Attendance", update_attendance),
        ("View Student Attendance", view_attendance),
        ("Low Attendance List", low_attendance_list),
    ])


# ------------------------------------------------------------------ exports
def stamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def export_text(lines, name):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{name}_{stamp()}.txt")
    with open(path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")
    return path


def export_pdf(lines, name):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"{name}_{stamp()}.pdf")
    write_simple_pdf(path, lines)
    return path


def write_simple_pdf(path, lines):
    """Tiny PDF writer (monospace text). Non-Latin characters become '?'."""
    def esc(text):
        text = text.encode("latin-1", "replace").decode("latin-1")
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    per_page = 55
    pages = [lines[i:i + per_page] for i in range(0, len(lines), per_page)] or [[]]
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(len(pages)))
    objects = ["<< /Type /Catalog /Pages 2 0 R >>",
               f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>",
               "<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>"]
    for i, page in enumerate(pages):
        body = "BT /F1 10 Tf 40 800 Td 14 TL\n"
        body += "\n".join(f"({esc(text)}) '" for text in page) + "\nET"
        data = body.encode("latin-1")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                       f"/Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>")
        objects.append(f"<< /Length {len(data)} >>\nstream\n{body}\nendstream")

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, obj in enumerate(objects, 1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode("latin-1") + obj.encode("latin-1") + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n").encode()
    with open(path, "wb") as file:
        file.write(out)


def export_csv():
    if not students:
        print("No student records to export!")
        return
    os.makedirs(EXPORT_DIR, exist_ok=True)
    path = os.path.join(EXPORT_DIR, f"students_{stamp()}.csv")
    header = (["Roll Number"] + [label for _, label, _ in FIELDS] + SUBJECTS +
              ["Total", "Percentage", "Grade", "Result", "Attendance %"])
    with open(path, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for s in students:
            pct = percentage(s)
            att = attendance_percentage(s)
            writer.writerow(
                [s["roll_number"]] + [s[key] for key, _, _ in FIELDS] +
                [s["marks"].get(sub, "") for sub in SUBJECTS] +
                [fmt_num(total_marks(s)) if pct is not None else "",
                 f"{pct:.2f}" if pct is not None else "", grade_for(pct), result_for(pct),
                 f"{att:.2f}" if att is not None else ""])
    print("CSV saved:", path)


def export_class_text():
    print("Saved:", export_text(class_report_lines(), "class_report"))


def export_class_pdf():
    print("Saved:", export_pdf(class_report_lines(), "class_report"))


def export_student_report():
    student = pick_student("Enter Roll Number for Report: ")
    if not student:
        return
    fmt = input("Format - 1. TXT  2. PDF: ").strip()
    name = f"student_{student['roll_number']}_report"
    if fmt == "1":
        print("Saved:", export_text(build_report(student), name))
    elif fmt == "2":
        print("Saved:", export_pdf(build_report(student), name))
    else:
        print("Invalid choice!")


def show_class_report():
    print()
    print("\n".join(class_report_lines()))


def show_department_report():
    department = get_text("Enter Department: ")
    print()
    print("\n".join(department_report_lines(department)))


def reports_menu():
    run_menu("REPORTS & EXPORT", [
        ("Class Report", show_class_report),
        ("Department Report", show_department_report),
        ("Export Students to CSV", export_csv),
        ("Export Class Report (TXT)", export_class_text),
        ("Export Class Report (PDF)", export_class_pdf),
        ("Export Student Report (TXT/PDF)", export_student_report),
    ])


# ------------------------------------------------------------------- backup
def create_backup():
    if not os.path.exists(FILE_NAME):
        return None
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        path = os.path.join(BACKUP_DIR, f"students_{stamp()}.json")
        shutil.copy2(FILE_NAME, path)
        return path
    except OSError as error:
        print("Backup failed:", error)
        return None


def list_backups():
    if not os.path.isdir(BACKUP_DIR):
        return []
    return sorted(f for f in os.listdir(BACKUP_DIR)
                  if f.startswith("students_") and f.endswith(".json"))


def backup_time(name):
    try:
        return datetime.strptime(name[9:24], "%Y%m%d_%H%M%S").strftime("%d-%m-%Y %H:%M:%S")
    except ValueError:
        return name


def manual_backup():
    path = create_backup()
    print("Backup created:" if path else "Nothing to back up yet.", path or "")


def show_backups():
    backups = list_backups()
    if not backups:
        print("No backups found!")
        return
    for number, name in enumerate(backups, 1):
        print(f"{number}. {name}  ({backup_time(name)})")


def restore_backup():
    if not require_admin():
        return
    backups = list_backups()
    if not backups:
        print("No backups found!")
        return
    show_backups()
    choice = get_number("Enter backup number to restore (0 to cancel): ", 0, len(backups))
    if choice == 0:
        return
    restored = read_students_file(os.path.join(BACKUP_DIR, backups[choice - 1]))
    if restored is None:
        print("This backup file is corrupted!")
        return
    if not ask_yes_no("Current data will be replaced. Continue? (y/n): "):
        return
    create_backup()
    students[:] = restored
    save_students()
    print("Backup restored successfully!")


def backup_menu():
    run_menu("BACKUP & RECOVERY", [
        ("Create Backup", manual_backup),
        ("Show Backups", show_backups),
        ("Restore Backup", restore_backup),
    ])


# --------------------------------------------------------------------- menus
def run_menu(title, options):
    while True:
        print(f"\n--- {title} ---")
        for number, (label, _) in enumerate(options, 1):
            print(f"{number}. {label}")
        print("0. Back")
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            return
        if choice.isdecimal() and 1 <= int(choice) <= len(options):
            options[int(choice) - 1][1]()
        else:
            print("Invalid choice! Please try again.")


def search_menu():
    run_menu("SEARCH & VIEW", [
        ("Search by Roll Number", search_by_roll),
        ("Search by Name", search_by_name),
        ("Search by Department", search_by_department),
        ("Display All Students", display_students),
        ("Sort Students", sort_students),
        ("Count Students", count_students),
    ])


MAIN_OPTIONS = [
    ("Add Student", add_student),
    ("Search & View Students", search_menu),
    ("Update Student", update_student),
    ("Delete Student", delete_student),
    ("Student Report", student_report),
    ("Academic Statistics", statistics_menu),
    ("Attendance", attendance_menu),
    ("Reports & Export", reports_menu),
    ("Backup & Recovery", backup_menu),
]


def print_main_menu():
    width = 38
    print("\n╔" + "═" * width + "╗")
    print("║" + "STUDENT MANAGEMENT SYSTEM".center(width) + "║")
    print("╠" + "═" * width + "╣")
    for number, (label, _) in enumerate(MAIN_OPTIONS, 1):
        print("║ " + f"{number}. {label}".ljust(width - 1) + "║")
    print("║ " + "0. Exit".ljust(width - 1) + "║")
    print("╚" + "═" * width + "╝")


def read_password(prompt="Password: "):
    """Hidden input only in a real terminal; otherwise normal input()."""
    if HIDE_PASSWORD and sys.stdin is not None and sys.stdin.isatty():
        try:
            return getpass.getpass(prompt)
        except (EOFError, OSError):
            pass
    return input(prompt)


def login():
    for attempt in range(1, MAX_LOGIN_ATTEMPTS + 1):
        username = input("Username: ").strip()
        password = read_password("Password: ")
        user = USERS.get(username)
        if user and hmac.compare_digest(user["password"], hash_password(password)):
            current_user.update(name=username, role=user["role"])
            print(f"Welcome, {username}! ({user['role']})")
            return True
        print(f"Wrong username or password! {MAX_LOGIN_ATTEMPTS - attempt} attempt(s) left.")
    print("Too many wrong attempts. Exiting.")
    return False


def main():
    if not login():
        return
    create_backup()  # automatic backup at start
    while True:
        print_main_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            create_backup()  # automatic backup at exit
            print("Thank you for using Student Management System!")
            return
        if choice.isdecimal() and 1 <= int(choice) <= len(MAIN_OPTIONS):
            MAIN_OPTIONS[int(choice) - 1][1]()
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")

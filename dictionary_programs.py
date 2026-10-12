# Dictionary Program 1: Student Record

student = {
    "roll_number": 101,
    "name": "Pawan Deshmukh",
    "department": "CSE AIML",
    "email": "pawan@example.com"
}

print("Student Record:")
print("Roll Number:", student["roll_number"])
print("Name:", student["name"])
print("Department:", student["department"])
print("Email:", student["email"])

# Dictionary Program 2: Add and Update Data

student = {
    "roll_number": 102,
    "name": "Rahul Patil",
    "department": "CSE AIML"
}

print("\nOriginal student:", student)

student["email"] = "rahul@example.com"
student["department"] = "CSE Cyber Security"

print("Updated student:", student)

# Dictionary Program 3: Student Marks

student_marks = {
    "Python": 85,
    "C Programming": 78,
    "Mathematics": 92,
    "Physics": 88
}

print("\nStudent Marks:", student_marks)

total = sum(student_marks.values())
average = total / len(student_marks)

print("Total Marks:", total)
print("Average Marks:", average)

# Dictionary Program 4: Delete Data

student = {
    "roll_number": 104,
    "name": "Sneha Kulkarni",
    "department": "CSE AIML",
    "email": "sneha@example.com"
}

print("\nOriginal student:", student)

del student["email"]

print("After deleting email:", student)
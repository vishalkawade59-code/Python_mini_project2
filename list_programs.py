# List Program 1: Student Subjects

subjects = ["Python", "C Programming", "Mathematics", "Physics"]

print("Subjects:", subjects)
print("First subject:", subjects[0])
print("Number of subjects:", len(subjects))

subjects.append("English")

print("After adding a subject:", subjects)

# List Program 2: Student Marks

marks = [78, 85, 92, 67, 88]

print("\nMarks:", marks)
print("Highest marks:", max(marks))
print("Lowest marks:", min(marks))
print("Total marks:", sum(marks))
print("Average marks:", sum(marks) / len(marks))

# List Program 3: Update Student Marks

marks = [78, 85, 92, 67, 88]

print("\nOriginal marks:", marks)

marks[3] = 75

print("Updated marks:", marks)

# List Program 4: Remove a Subject

subjects = ["Python", "C Programming", "Mathematics", "Physics"]

print("\nOriginal subjects:", subjects)

subjects.remove("Physics")

print("After removing Physics:", subjects)
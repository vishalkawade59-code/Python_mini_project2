# Set Program 1: Unique Departments

departments = {"CSE AIML", "CSE AIML", "Mechanical", "Civil", "Mechanical"}

print("Departments:", departments)
print("Number of unique departments:", len(departments))

# Set Program 2: Add a Department

departments = {"CSE AIML", "Mechanical", "Civil"}

print("\nOriginal departments:", departments)

departments.add("Electrical")

print("After adding Electrical:", departments)

# Set Program 3: Set Operations

cse_students = {"Pawan", "Rahul", "Amit"}
aiml_students = {"Pawan", "Sneha", "Amit"}

print("\nCSE Students:", cse_students)
print("AIML Students:", aiml_students)

print("Students in both groups:", cse_students.intersection(aiml_students))
print("All students:", cse_students.union(aiml_students))
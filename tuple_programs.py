# Tuple Program 1: Student Fixed Information

student_info = (101, "Pawan Deshmukh", "CSE AIML")

print("Student information:", student_info)
print("Roll Number:", student_info[0])
print("Name:", student_info[1])
print("Department:", student_info[2])

# Tuple Program 2: Tuple Unpacking

student_info = (102, "Rahul Patil", "CSE AIML")

roll_number, name, department = student_info

print("\nTuple:", student_info)
print("Roll Number:", roll_number)
print("Name:", name)
print("Department:", department)

# Tuple Program 3: Immutability

student_data = (103, "Amit Sharma", "CSE AIML")

print("\nOriginal tuple:", student_data)

# Tuples cannot be changed after creation.
print("Tuple cannot be modified after creation.")
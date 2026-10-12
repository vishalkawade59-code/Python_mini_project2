# String Program 1: Basic Student Information

student_name = "Pawan"
department = "CSE AIML"

print("Student Name:", student_name)
print("Department:", department)
print("Name in uppercase:", student_name.upper())
print("Name in lowercase:", student_name.lower())
print("Length of name:", len(student_name))

# String Program 2: Email Processing

email = "pawan@example.com"

print("\nEmail:", email)
print("Email in uppercase:", email.upper())
print("Contains @:", "@" in email)
print("Username:", email.split("@")[0])
print("Domain:", email.split("@")[1])

# String Program 3: Clean Student Name

student_name = "   Pawan Deshmukh   "

clean_name = student_name.strip()

print("\nOriginal name:", student_name)
print("Clean name:", clean_name)
print("Name length:", len(clean_name))
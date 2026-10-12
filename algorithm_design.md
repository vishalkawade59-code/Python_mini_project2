# Student Record and Academic Management System

## Algorithm Design

## 1. Add New Student

### Algorithm

1. Start the program.
2. Accept the student's details from the user.
3. Check whether the given roll number already exists.
4. If the roll number already exists, display a duplicate-record message.
5. If the roll number does not exist, create the student record.
6. Store the new student record in the student collection.
7. Display a message confirming that the student was added successfully.
8. Stop.

## 2. Search Student by Roll Number

### Algorithm

1. Start the program.
2. Accept the roll number to be searched.
3. Check each student record in the student collection.
4. Compare the entered roll number with the roll number of each student.
5. If a matching roll number is found, display the student's complete information.
6. If no matching roll number is found, display a "Student not found" message.
7. Stop.

## 3. Update Student Information

### Algorithm

1. Start the program.
2. Accept the roll number of the student whose information needs to be updated.
3. Search for the student record using the roll number.
4. If the student record is not found, display a "Student not found" message.
5. If the record is found, display the existing student information.
6. Accept the new information from the user.
7. Update the required fields in the student record.
8. Store the updated record in the student collection.
9. Display a message confirming that the record was updated successfully.
10. Stop.

## 4. Delete Student Record

### Algorithm

1. Start the program.
2. Accept the roll number of the student whose record needs to be deleted.
3. Search for the student record using the roll number.
4. If the student record is not found, display a "Student not found" message.
5. If the record is found, remove the student record from the student collection.
6. Display a message confirming that the record was deleted successfully.
7. Stop.

## 5. Calculate Average Marks

### Algorithm

1. Start the program.
2. Select the student whose average marks need to be calculated.
3. Retrieve the student's marks.
4. Add all the subject marks.
5. Count the number of subjects.
6. Divide the total marks by the number of subjects.
7. Display the calculated average marks.
8. Stop.

## 6. Find Highest Scorer

### Algorithm

1. Start the program.
2. Check whether the student collection contains any records.
3. If the collection is empty, display an appropriate message.
4. Select the first student's marks as the initial highest marks.
5. Compare the marks of each remaining student with the current highest marks.
6. If a student's marks are higher, update the highest marks and store that student's record.
7. Continue until all student records have been checked.
8. Display the student with the highest marks.
9. Stop.

## 7. List Students by Department

### Algorithm

1. Start the program.
2. Accept the department name from the user.
3. Check each student record in the student collection.
4. Compare the student's department with the entered department.
5. If the department matches, display that student's information.
6. Continue checking until all student records have been processed.
7. If no matching student is found, display an appropriate message.
8. Stop.

## 8. Count Students

### Algorithm

1. Start the program.
2. Check the student collection.
3. Count the number of student records in the collection.
4. Store the count.
5. Display the total number of students.
6. Stop.
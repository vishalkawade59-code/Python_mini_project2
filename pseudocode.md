# Student Record and Academic Management System

## Pseudocode

## 1. Add Student

START

READ student details

IF roll number already exists THEN
    DISPLAY "Student Already Exists"
ELSE
    CREATE student record
    STORE student record
    DISPLAY "Student Added Successfully"
END IF

STOP

## 2. Search Student

START

READ roll number

SET student_found = FALSE

FOR EACH student in student collection
    IF student roll number matches entered roll number THEN
        DISPLAY student details
        SET student_found = TRUE
        STOP SEARCH
    END IF
END FOR

IF student_found = FALSE THEN
    DISPLAY "Student Not Found"
END IF

STOP

## 3. Update Student

START

READ roll number

SEARCH for student using roll number

IF student is not found THEN
    DISPLAY "Student Not Found"
ELSE
    DISPLAY existing student details
    READ new student information
    UPDATE required fields
    DISPLAY "Record Updated Successfully"
END IF

STOP

## 4. Delete Student

START

READ roll number

SEARCH for student using roll number

IF student is not found THEN
    DISPLAY "Student Not Found"
ELSE
    DELETE student record
    DISPLAY "Record Deleted Successfully"
END IF

STOP

## 5. Calculate Average Marks

START

READ student record

GET student marks

SET total_marks = 0
SET subject_count = 0

FOR EACH mark in student marks
    ADD mark to total_marks
    INCREASE subject_count by 1
END FOR

IF subject_count > 0 THEN
    SET average = total_marks / subject_count
    DISPLAY average
ELSE
    DISPLAY "No Marks Available"
END IF

STOP

## 6. Find Highest Scorer

START

IF student collection is empty THEN
    DISPLAY "No Student Records"
ELSE
    SET highest_student = first student
    SET highest_marks = marks of highest_student

    FOR EACH student in student collection
        IF student marks > highest_marks THEN
            SET highest_marks = student marks
            SET highest_student = student
        END IF
    END FOR

    DISPLAY highest_student details
END IF

STOP

## 7. List Students by Department

START

READ department name

SET student_found = FALSE

FOR EACH student in student collection
    IF student department matches entered department THEN
        DISPLAY student details
        SET student_found = TRUE
    END IF
END FOR

IF student_found = FALSE THEN
    DISPLAY "No Students Found"
END IF

STOP

## 8. Count Students

START

SET student_count = 0

FOR EACH student in student collection
    INCREASE student_count by 1
END FOR

DISPLAY student_count

STOP
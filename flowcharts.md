# Student Record and Academic Management System

## Flowchart Collection

## 1. Add Student Flowchart

```text
START
  ↓
Read Student Details
  ↓
Check Roll Number
  ↓
Does Roll Number Already Exist?
  ├── YES → Display "Student Already Exists"
  │            ↓
  │           STOP
  │
  └── NO → Create Student Record
              ↓
          Store Student Record
              ↓
       Display "Student Added Successfully"
              ↓
             STOP
             
## 2. Search Student Flowchart

START
  ↓
Read Roll Number
  ↓
Search Student Collection
  ↓
Is Student Found?
  ├── YES → Display Student Details
  │            ↓
  │           STOP
  │
  └── NO → Display "Student Not Found"
              ↓
             STOP

## 3. Update Student Flowchart

START
  ↓
Read Roll Number
  ↓
Search Student Collection
  ↓
Is Student Found?
  ├── NO → Display "Student Not Found"
  │           ↓
  │          STOP
  │
  └── YES → Display Existing Details
               ↓
          Read New Information
               ↓
          Update Student Record
               ↓
       Display "Record Updated Successfully"
               ↓
              STOP

## 4. Delete Student Flowchart

START
  ↓
Read Roll Number
  ↓
Search Student Collection
  ↓
Is Student Found?
  ├── NO → Display "Student Not Found"
  │           ↓
  │          STOP
  │
  └── YES → Delete Student Record
               ↓
       Display "Record Deleted Successfully"
               ↓
              STOP

## 5. Calculate Average Marks Flowchart

START
  ↓
Select Student
  ↓
Read Student Marks
  ↓
Calculate Total Marks
  ↓
Count Number of Subjects
  ↓
Average = Total Marks / Number of Subjects
  ↓
Display Average Marks
  ↓
STOP

## 6. Highest Scorer Flowchart

START
  ↓
Check Student Collection
  ↓
Is Collection Empty?
  ├── YES → Display "No Student Records"
  │           ↓
  │          STOP
  │
  └── NO → Select First Student as Highest
               ↓
          Compare Remaining Students
               ↓
          Is Current Student's Marks Higher?
               ├── YES → Update Highest Student
               └── NO  → Continue
                         ↓
                 More Students?
                    ├── YES → Compare Next Student
                    └── NO  → Display Highest Scorer
                                  ↓
                                 STOP

## 7. Students by Department Flowchart

START
  ↓
Read Department Name
  ↓
Check Student Collection
  ↓
Compare Each Student's Department
  ↓
Does Department Match?
  ├── YES → Display Student Details
  └── NO  → Continue to Next Student
                 ↓
          More Students?
             ├── YES → Check Next Student
             └── NO  → Were Any Students Found?
                          ├── YES → STOP
                          └── NO  → Display "No Students Found"
                                      ↓
                                     STOP

## 8. Count Students Flowchart

START
  ↓
Check Student Collection
  ↓
Count Student Records
  ↓
Display Total Number of Students
  ↓
STOP


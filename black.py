# 4th example (only class example)
class phone:
  display=6.0
  charging_port="C_type"
  speakers=2
  mic="dual"
  body_shape="rectangular"

p=phone()
print(p.display)
print(p.mic)

# 3rd example (only class example)
class student:
    name="pawan"
    gender="male"
    age=18
    education="b_tech"
    department="AIML"
    div="b"
    prn=1175
    year="fy2026"
    phone_number =9322550181
    progress="good"

s2=student()
print(s2.prn)
print(s2.year)

# 2nd self tried Example 
class student:
  name=""
  gender=""
  age=""
  education=""
  department=""
  div=""
  prn=""
  year=""
  phone_number =""
  progress=""

  def data(self):
    self.name=input("enter name")
    self.gender=input("enter gender")
    self.age=float(input("enter age"))
    self.education=input("enter education")
    self.department=input("enter department")
    self.div=input("enter division")
    self.prn=int(input("enter prn"))
    self.year=int(input("enter year"))
    self.phone_number =int(input("enter phone number"))
    self.progress=input("enter progress")

  def show(self):
    print(self.name,self.gender,self.age, self.education, self.department, self.div, self.prn, self.year, self.phone_number, self.progress)

s1=student()

s1.data()

#1st example   
class car:
  model_name=""
  milage=""
  speed=""
  price=""
  year=""

  def data(self):
    self.model_name=input("name")
    self.milage=int(input("milage"))
    self.speed=int(input("speed"))
    self.price=float(input("price"))
    self.year=int(input("year"))

  def show(self):
    print(self.model_name,self.milage,self.speed, self.price, self.year)

c1=car()

c1.data()
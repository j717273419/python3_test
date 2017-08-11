#coding:UTF-8
class Employee:
    '所有基类员工'
    empCount = 0

    def __init__(self,name,salary):
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    def displayCount(self):
        print("Total Employee %d",Employee.empCount)

    def displayEmpoyee(self):
        print("Name:",self.name,"Salary:",self.salary)

emp1 = Employee("xm","2000")
emp2 = Employee("lm","50000")

emp1.displayEmpoyee()
emp2.displayEmpoyee()

print("Total Employee %d" %  Employee.empCount)
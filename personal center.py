import WaterModule,ExerciseModule,SleepModule
import os
import json

class PersonalCenter:
    def __init__(self, name, age, gender, height, weight):
        self.name = name
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.health_assessment = None
        self.water = WaterModule.WaterMoudle()
        self.exercise = ExerciseModule.ExerciseModule()
        self.sleep = SleepModule.SleepModule()

    def update_personal_info(self, name=None, age=None, gender=None, height=None, weight=None):
        if name:
            self.name = name
        if age:
            self.age = age
        if gender:
            self.gender = gender
        if height:
            self.height = height
        if weight:
            self.weight = weight

    def calculate_bmi(self):
        bmi = (self.weight / (self.height ** 2)) * 10000
        return bmi

    def assess_health(self):
        bmi = self.calculate_bmi()
        # Add more health assessment criteria here based on BMI, age, gender, etc.
        if bmi < 18.5:
            self.health_assessment = "Underweight"
        elif 18.5 <= bmi < 25:
            self.health_assessment = "Normal weight"
        elif 25 <= bmi < 30:
            self.health_assessment = "Overweight"
        else:
            self.health_assessment = "Obese"

    def display_personal_info(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Gender:", self.gender)
        print("Height (in cm):", self.height)
        print("Weight (in kg):", self.weight)
        if self.health_assessment:
            print("Health Assessment:", self.health_assessment)


# Example usage:
personal_info = PersonalCenter("Jamie", 20, "Male", 175, 55)
personal_info.assess_health()
personal_info.display_personal_info()

# Update personal information
personal_info.update_personal_info(age=21, weight=60)
personal_info.assess_health()
personal_info.display_personal_info()


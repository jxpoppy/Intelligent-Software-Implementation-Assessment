class PersonalCenter:
    def __init__(self, name, age, gender, height, weight):
        self.name = name
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.health_assessment = None

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


from datetime import datetime

class ExerciseModule:
    def __init__(self):
        self.exercise_records = []

    def record_exercise(self, exercise_name, duration_minutes):
        exercise_time = datetime.now()
        exercise_record = {"exercise_name": exercise_name, "duration_minutes": duration_minutes, "exercise_time": exercise_time}
        self.exercise_records.append(exercise_record)

    def display_exercise_records(self):
        if not self.exercise_records:
            print("No exercise records available.")
            return
        print("Exercise Records:")
        for i, record in enumerate(self.exercise_records, 1):
            print(f"{i}. Exercise: {record['exercise_name']}, Duration: {record['duration_minutes']} minutes, Time: {record['exercise_time']}")

    def get_total_exercise_duration(self):
        total_duration = sum(record['duration_minutes'] for record in self.exercise_records)
        return total_duration

    def exercise_reminder(self, target_duration):
        total_duration = self.get_total_exercise_duration()
        if total_duration < target_duration:
            remaining_duration = target_duration - total_duration
            print(f"You have {remaining_duration} minutes remaining to reach your exercise goal.")

    def display_historical_statistics(self):
        if not self.exercise_records:
            print("No exercise records available for statistics.")
            return
        total_duration = self.get_total_exercise_duration()
        print(f"Total Exercise Duration: {total_duration} minutes")

    def plan_exercise(self, target_duration):
        self.exercise_reminder(target_duration)
        self.display_historical_statistics()


# Example usage:
exercise_module = ExerciseModule()

# Record exercise
exercise_module.record_exercise("Running", 30)
exercise_module.record_exercise("Dancing", 45)
exercise_module.display_exercise_records()

# Exercise reminder
exercise_module.exercise_reminder(target_duration=60)

# Historical statistics
exercise_module.display_historical_statistics()

# Exercise planning
exercise_module.plan_exercise(target_duration=120)

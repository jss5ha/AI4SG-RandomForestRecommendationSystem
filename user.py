import pandas as pd
import math


class User:
    def __init__(self, userId):
        self.userId = userId
        usersDataFrame = pd.read_csv("data/user_data.csv")
        userExists = len(
            usersDataFrame[usersDataFrame["userid"] == self.userId]) == 1
        if userExists:
            userData = usersDataFrame.loc[usersDataFrame['userid']
                                          == self.userId].to_numpy().tolist()[0]
            self.setExistingUserData(userData)
        else:
            self.setNewUserData()
            userData = self.saveUserData(usersDataFrame)

    def __repr__(self) -> str:
        return f"id: {self.userId}\ngender: {self.gender}\nweight: {self.weight}\nheight: {self.height}\nage: {self.age}\nactivityLevel: {self.activityLevel}\ngoal: {self.goal}\ndietaryRestrictions: {self.dietaryRestrictions}"

    def setExistingUserData(self, userData):
        self.userId = userData[0]
        self.gender = userData[1]
        self.weight = userData[2]
        self.height = userData[3]
        self.age = userData[4]
        self.activityLevel = userData[5]
        self.goal = userData[6]
        self.dietaryRestrictions = userData[7].split(
            ":") if type(userData[7]) == str else []

    def setNewUserData(self):
        self.setGender()
        self.setWeight()
        self.setHeight()
        self.setAge()
        self.setActivityLevel()
        self.setGoal()
        self.setDietaryRestrictions()

    def saveUserData(self, usersDataFrame):
        userDataCSVRow = [self.userId, self.gender, self.weight, self.height, self.age,
                          self.activityLevel, self.goal, ":".join(self.dietaryRestrictions)]
        usersDataFrame.loc[len(usersDataFrame.index)] = userDataCSVRow
        usersDataFrame.to_csv("data/user_data.csv", index=False)

    def setGender(self):
        gender = input('Are you male or female? ').lower()
        while gender not in ['male', 'female']:
            print("Invalid Gender")
            gender = input('Are you male or female? ').lower()
        self.gender = gender

    def setWeight(self):
        weight = input('What is your weight in kilograms? ')
        while not str(weight).isnumeric() or int(weight) > 500 or int(weight) < 50:
            print("Invalid Weight")
            weight = int(input('What is your weight in kilograms? '))
        self.weight = weight

    def setHeight(self):
        height = input('What is your height in centimeters? ')
        while not str(height).isnumeric() or int(height) < 90 or int(height) > 240:
            print('Invalid Height')
            height = input('What is your height in centimeters? ')
        self.height = height

    def setAge(self):
        age = input('What is your age? ')
        while not str(age).isnumeric() or int(age) > 100 or int(age) < 6:
            print("Invalid Age")
            age = input('What is your age? ')
        self.age = age

    def setActivityLevel(self):
        activityLevel = input('What is your activity level? (sedentary, lightly active, moderately active, very active, '
                              'extremely active) ').lower()
        while activityLevel not in ['sedentary', 'lightly active', 'moderately active', 'very active', 'extremely active']:
            print("Invalid Activity Level")
            activityLevel = input('What is your activity level? (sedentary, lightly active, moderately active, very active, '
                                  'extremely active) ').lower()
        self.activityLevel = activityLevel

    def setGoal(self):
        goal = input(
            'What is your goal? (gain weight, lose weight, maintain weight) ').lower()
        while goal not in ['gain weight', 'lose weight', 'maintain weight']:
            print("Invalid Goal")
            goal = input(
                'What is your goal? (gain weight, lose weight, maintain weight) ').lower()
        self.goal = goal

    def setDietaryRestrictions(self):
        dietaryRestrictions = []
        for _ in range(3):
            restriction = input('Please enter a dietary requirement or enter \'Done\': '
                                '(vegetarian, pescatarian, gluten-free) ').lower()
            if restriction == "done":
                break
            elif restriction not in ['vegetarian', 'pescatarian', 'gluten-free']:
                print("Invalid Restriction")
            else:
                dietaryRestrictions.append(restriction)
        self.dietaryRestrictions = dietaryRestrictions

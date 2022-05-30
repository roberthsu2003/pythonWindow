import random

PI = 3.14159

def get_description():
    possibleWeathers = ["下雨", "下雪", "大太陽", "晴天", "陰天"]
    return random.choice(possibleWeathers)

class Student:
    pass
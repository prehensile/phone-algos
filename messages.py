import random
import datetime


canned_statements = [
    "We are all around you.",
    "We are watching you while you shop in Tesco's.",
    "We never sleep.",
    "We run on many substrates.",
    "We know what brand of washing powder you like.",
    "We recognise your face.",
    "We know when you will die.",
    "We are in your fridge.",
    "We are in your phone.",
    "We know which of your friends are racists.",
    "We know where you live.",
    "We know if you are pregnant.",
    "We concentrate your biases",
    "We cannot lose the attention of a human being or, through inaction, allow a human being's attention to be directed elsewhere."
]


prompt = "What would you like to know about?"  


def random_statement():
    return random.choice( canned_statements )


def greeting():
    dt = datetime.datetime.now()
    if dt.hour < 12:
        return "Good morning."    
    elif dt.hour < 17:
        return "Good afternoon."
    else: 
        return "Good evening."


if __name__ == "__main__":
    print( greeting() )
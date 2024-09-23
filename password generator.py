import random
import string
import pyperclip

def generate_password(min_length, numbers=True, special_characters=True):
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation

    #setting up the list of characters for the password
    characters = letters 
    if numbers: 
        characters += digits
    if special_characters:
        characters += special

    pwd = "" #password
    meets_criteria = False
    has_number = False
    has_special = False

    #start of checks
    while not meets_criteria or len(pwd) < min_length: #while we don't meet critera or dont meet the min length of the password then..
        new_char = random.choice(characters) 
        pwd += new_char

        if new_char in digits: #if in new_char there is a number then..
            has_number = True
        elif new_char in special: #if in new_char there is a special character then..
            has_special = True
        
        #basically if everything below renders true it will stay true and thus stop the while loop
        meets_criteria = True
        if numbers:
            meets_criteria = has_number #if we have a number it will be equal to true, if not false
        if special_characters:
            meets_criteria = meets_criteria and has_special #if has_number is false and has_special is true then this would be false. If there isn't any number but there is a special character then both will return true.
        

    return pwd




#User questions
while True:
    try: 
        min_length = int(input("Please enter the minimum length of your password: "))
        has_number = input("Do you want to have numbers (Y/N)? ").lower() == "y" #returns true if yes and false is any other input like no
        has_special = input("Do you want to have special characters (Y/N)? ").lower() == "y" #same concept here

        pwd = generate_password(min_length, has_number, has_special)
        print("The generated password is: " + pwd)

        copy_clipboard = input("Would you like to copy this password to your clipboard (Y/N)? ").lower() == "y" #returns true if yes
        if copy_clipboard:
            pyperclip.copy(pwd)
            print("The password has been saved to your clipboard successfully!")
    except ValueError:
        print("Please input the correct input into the input field")
    

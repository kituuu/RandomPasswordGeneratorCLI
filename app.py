import click
import random
import string


# Declaring Constants
symbols = ['~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/']

replacement = {
    "i":'!',
    "a":"@",
    "h":"#",
    "s":'$',
    "o":'0',
    'e':"3",
}

# function to remove vowel 
def removeVowel(s:list):
    vowels = "aeiou"
    temp = ""
    l = len(s)
    for i in range(1,l-1):
        if s[i] in vowels:
            s[i] = 0    
    for char in s:
        if char!=0:
            temp+=char
    return temp

def fixPassword(oldPass):
    for i in range(len(oldPass)):
        if i==0:
            oldPass[i] = oldPass[i].capitalize()
        elif oldPass[i].lower() in replacement.keys():
            oldPass[i] = replacement[oldPass[i].lower()]
    temp = ""
    for i in range(len(oldPass)):
        temp+=oldPass[i]
    return temp

# Adding this function as a command using click
@click.command()

# Creating option for length input
@click.option("-l","--length",help="This is the length of password generated", required=0)

# Creating option for special character check
@click.option("-s","--special",default='Y', help="Whether you want special character in your password or not\nY for yes,N for no",required=0)

# Creating option for alphabet case
@click.option("-c","--case",default='B', help="Whether you want your password to be in special case\nU for uppercase\nL for lowercase\nB for both",required=0)

# Creating option for digits
@click.option("-n","--number",default='Y', help="Whether you want your password to contain numbers (Y/N)",required=0)

# Creating option to generate password based on user input
@click.option('-i',"--input_based",help="Will generate password based on this input")

# Creating a function to repair a non accepting password
@click.option('-f',"--fix_password",help="This command will fix a poor password", required=0, default="")

# Creating a function which will create a password based on a password hint
# password generate function (command)
def gen_pass(length, special, case, number, input_based,fix_password):

    # Dummy variable to store generated password
    pwd = ""

    # List to hold set of all possible values aur password can take
    charlist = list()

    # Defining list containing different set of characters
    upper = list(string.ascii_uppercase)
    lower = list(string.ascii_lowercase)
    digits = list(string.digits)
    fix_password = list(fix_password)
    
    
    # Setting up our character list based on different inputs provided by the user
    if str(special).lower().strip() == "y":
        charlist.extend(symbols)
    if str(case).lower().strip() == "u":
        print("ME WAS HERE")
        charlist.extend(upper)
    if str(case).lower().strip() == "l":
        charlist.extend(lower)
    if str(case).lower().strip() == "b":
        charlist.extend(lower)
        charlist.extend(upper)
    if str(number).lower().strip() == "y":
        charlist.extend(digits)
    
    # Extracting character from given user input
    if input_based is not None:
        inpass = list(input_based)
        inpass = removeVowel(inpass)
    # print(inpass)
    
    if length is not None:
        while len(pwd)<int(length):
            random.shuffle(charlist)
            pwd+=random.choice(charlist)
        print(pwd)
    if fix_password is not None:
        fix_password = fixPassword(fix_password)
    print(fix_password)
    


if __name__ == "__main__" :
    gen_pass()
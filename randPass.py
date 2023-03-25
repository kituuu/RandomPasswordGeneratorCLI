import click
import random
import string
import nltk


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
    temp = ""
    for i in range(len(oldPass)):
        if i==0:
            temp += oldPass[i].capitalize()
        elif oldPass[i].lower() in replacement.keys():
            temp += replacement[oldPass[i].lower()]
        else:
            temp+= oldPass[i]
    # temp = ""
    # for i in range(len(oldPass)):
    #     temp+=oldPass[i]
    return temp
def generateword(text) :
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    # Build a Markov chain model
    model = {}
    for i in range(len(tokens) - 1):
        current_word = tokens[i]
        next_word = tokens[i + 1]
        if current_word not in model:
            model[current_word] = {}
        if next_word not in model[current_word]:
            model[current_word][next_word] = 0
        model[current_word][next_word] += 1

    # Generate a random word
    current_word = random.choice(tokens)
    while current_word not in model:
        current_word = random.choice(tokens)
    next_word_distribution = model[current_word]
    next_word = random.choices(list(next_word_distribution.keys()), weights=list(next_word_distribution.values()))[0]
    while not next_word.isalpha():
        current_word = next_word
        next_word_distribution = model[current_word]
        next_word = random.choices(list(next_word_distribution.keys()), weights=list(next_word_distribution.values()))[0]
    return next_word

def getHintPassword(inputtext):
    hintPassword = ""

    while len(hintPassword) < 12:
        temp = generateword(inputtext)
        if temp not in hintPassword:
            hintPassword+= temp

    return hintPassword

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
@click.option('-h',"--hint_based",help="This command will generate a random password based on your given hint sentece of more than 6 words.",required=0,default="")

# password generate function (command)
def gen_pass(length, special, case, number, input_based,fix_password, hint_based):

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
    hint_based = str(hint_based)
    if len(hint_based) > 0:
        generated = getHintPassword(str(hint_based))
        generated = fixPassword(generated)
        print(generated)


if __name__ == "__main__" :
    gen_pass()
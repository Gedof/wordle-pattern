import random

#This module contains the actual "game" and its functions

#Checks a guess with a password and returns the result. Ex.: [0,1,0,2,1]
# 0 is gray (wrong letter)
# 1 is yellow (wrong position)
# 2 is green (correct)
def make_guess(password:str, guess:str) -> list:
    #Changes the strings into lists of strings
    guess = list(guess)
    password = list(password)
    letters = list(password)
    
    result = [0,0,0,0,0]

    #Checks all the green letters
    for idx,val in enumerate(guess):
        if val == password[idx]:
            result[idx] = 2
            #Removes the green letters from the possible pool, so it doesn't count twice when yellow
            if val in letters: letters.remove(val)

    #Chacks all the yellow letters
    for idx,val in enumerate(guess):
        if result[idx] == 0 and val in letters:
            result[idx] = 1
            #Also removes from the pool so it's not counted twice
            letters.remove(val)

    return result

#Tries to match a pattern to a given password
def play(password:str, game:list, words:list[str]) -> list:
    
    #Sorts the lines from most to least points (sum of the letters). It is easier to try more restrictive patterns first (the ones that are more correct).
    sorted_game = sorted(game, key=lambda li: sum(li[1]), reverse=True)

    #Shuffles the possible words and copies it. (One of them will be altered, but we still need the original)
    random.shuffle(words)
    filtered_words = words.copy()

    all_banned = [] #All banned letters (These are letters that have been gray already)
    results = []

    for li in sorted_game:
        #Tries to find a word that gives the desired pattern without using banned letters
        guess = next((x for x in filtered_words if make_guess(password, x) == li[1]), None)

        #If it fails, tries the original pool even if it uses invalid letters
        if guess == None:
            guess = next((x for x in words if make_guess(password, x) == li[1]), None)
            if guess == None: return None #If it still fails, we give up on this password
        else:
            filtered_words.remove(guess)

        #Removes the guess so it doesn't try it again on this game
        words.remove(guess)

        #Ban gray letters in guess (letters that are not in the password)
        banned = [x for x in list(guess) if x not in list(password)]

        results.append([li[0],guess])
        all_banned.extend(banned)

        #Filter words that have banned letters
        filtered_words = list(filter(lambda w: not [l for l in list(w) if l in all_banned], words))
    
    #Sort the result to go back to its original order
    return sorted(results, key=lambda li: li[0])

#Plays a game for each possible password
def playMultiple(passwords:list[str], game:list, words:list[str]):
    results = []
    for pswd in passwords:
        result = play(pswd, game, words)
        if result != None:
            results.append([pswd,result])
    return results
import random


def make_guess(password:str, guess:str):
    guess = list(guess)
    password = list(password)
    letters = list(password)
    result = [0,0,0,0,0]

    for idx,val in enumerate(guess):
        if val == password[idx]:
            result[idx] = 2
            if val in letters: letters.remove(val)

    for idx,val in enumerate(guess):
        if result[idx] == 0 and val in letters:
            result[idx] = 1
            letters.remove(val)

    return result

def play(password:str, game:list, words:list[str]):
    sorted_game = sorted(game, key=lambda li: sum(li[1]), reverse=True)
    random.shuffle(words)
    filtered_words = words.copy()
    all_banned = []
    results = []
    for li in sorted_game:
        guess = next((x for x in filtered_words if make_guess(password, x) == li[1]), None)
        if guess == None:
            guess = next((x for x in words if make_guess(password, x) == li[1]), None)
            if guess == None: return None
        banned = [x for x in list(guess) if x not in list(password)]
        results.append([li[0],guess])
        all_banned.extend(banned)
        random.shuffle(words)
        filtered_words = list(filter(lambda w: not [l for l in list(w) if l in all_banned], words))
    return sorted(results, key=lambda li: li[0])

def playMultiple(passwords:list[str], game:list, words:list[str]):
    random.shuffle(passwords)
    results = []
    for pswd in passwords:
        result = play(pswd, game, words)
        if result != None:
            results.append([pswd,result])
    return results
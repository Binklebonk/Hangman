# Hangman project
# By Noah Dodgshun
# 32/01/2026

import json
import random
import string

def difficulty():
    print(
        'What difficulty do you want to play?\n'
        'Easy (5-6 letter words, type e)\n'
        'Medium (7-9 letter words, type m)\n'
        'Hard (10-13 letter words, type h)'
    )
    while True: # Loop until correct input is recognised
        user_difficulty = input('').lower().strip() # Setting user input to lowercase and removing extra spaces
        if user_difficulty in ['e', 'm', 'h']:
            break # Breaking loop for correct input
        else:
            print('Input not recognised. Make sure you typed everything correctly.\n')
    return choose_word(user_difficulty) # Sending a random word from the json list

def choose_word(user_difficulty):
    try: # Opening the json file with word lists
        with open('words.json', 'r') as f:
            data = json.load(f)
    except:
        print(
            'There was an error with the json word file.\n'
            'Make sure it is in the correct directory.'
        )
    # Returning random word from corresponding list depending on chosen difficulty
    if user_difficulty == 'e':
        return random.choice(data["easy_words"])
    elif user_difficulty == 'm':
        return random.choice(data["medium_words"])
    elif user_difficulty == 'h':
        return random.choice(data["hard_words"])

def game(word_to_guess):
    # Setting up the display of what letters you have guessed
    guessed_word = ['_'] * len(word_to_guess)
    all_letters = string.ascii_lowercase
    win = False

    tries = len(word_to_guess)
    if len(word_to_guess) > 10:
        tries = 10

    while True: # Repeating this for the amount of tries you have
        # Printing out turn info
        print(f'You have {tries} tries left.')
        print(f'Letters you can guess: {all_letters}')
        print(f'{''.join(guessed_word)}\n')
        guess = input('Enter a letter to guess: ').lower()

        if len(guess) > 1: # Making sure you can't accidentally type more than one letter
            print('Make sure your answer is only one letter.')
        else:
            if guess not in all_letters: # Making sure you can't guess the same letter twice
                print('You already guessed that.')
            else:
                all_letters = all_letters.replace(guess, '_') # Removing letter from letter list

                # Loop to replace the guessed letter as many times as it appears in the word
                if guess not in word_to_guess:
                    print('That letter is not in this word.')
                    tries -= 1
                else:
                    digit = 0
                    for i in word_to_guess:
                        if word_to_guess[digit] == guess:
                            guessed_word[digit] = guessed_word[digit].replace('_', i)
                        digit +=1

                # Win condition
                if '_' not in guessed_word:
                    print(f'{''.join(guessed_word)}\nYou win!')
                    win = True
                    break
        if tries == 0:
            break

    # Lose
    if win == False:
        print(f'You lose! The word was {word_to_guess}.')

if __name__ == '__main__':
    word_to_guess = difficulty()
    game(word_to_guess=word_to_guess)
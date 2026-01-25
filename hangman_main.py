# Hangman project
# By Noah Dodgshun
# 32/01/2026

import json
import random
import string
import os

try: # Installing easygui
    from easygui import *
except:
    print('Easygui library not found. Installing...')
    os.system('pip install easygui') # Using pip to load library

def get_word():
    user_difficulty = buttonbox(
        'What difficulty do you want to play?\n',
        'Difficulty', ['Easy (5-6 letter words)', 'Medium (7-9 letter words)', 'Hard (10-13 letter words)']).lower().strip() # Setting user input to lowercase and removing extra spaces
    try: # Opening the json file with word lists
        with open('words.json', 'r') as f:
            data = json.load(f)
        # Returning random word from corresponding list depending on chosen difficulty
        if user_difficulty == 'easy (5-6 letter words)':
            return random.choice(data["easy_words"])
        elif user_difficulty == 'medium (7-9 letter words)':
            return random.choice(data["medium_words"])
        elif user_difficulty == 'hard (10-13 letter words)':
            return random.choice(data["hard_words"])
    except:
        print(
            'There was an error with the json word file.\n'
            'Make sure it is in the correct directory.'
        )
        exit() # Closing program to prevent further errors

def game(word_to_guess):
    # Setting up the display of what letters you have guessed
    guessed_word = ['_ '] * len(word_to_guess)
    all_letters = string.ascii_lowercase
    win = False
    turn_message = 'Good luck!'

    # Calculate number of tries the user has depending on word length
    tries = len(word_to_guess)
    if len(word_to_guess) > 10: # No more than 10 tries max
        tries = 10

    while True: # Repeating this for the amount of tries you have
        # Displaying turn info
        guess = enterbox(
            f'{turn_message}\n'
            f'You have {tries} tries left.\n'
            f'Letters you can guess: {all_letters}\n'
            f'{''.join(guessed_word)}\n'
            'Enter a letter to guess:',
            'Guess'
        ).lower().strip()

        if len(guess) > 1: # Making sure you can't accidentally type more than one letter
            turn_message = 'Make sure your answer is only one letter.'
        else:
            if guess not in all_letters: # Making sure you can't guess the same letter twice
                turn_message = 'You already guessed that.'
            else:
                all_letters = all_letters.replace(guess, '_ ') # Removing letter from letter list

                # Loop to replace the guessed letter as many times as it appears in the word
                if guess not in word_to_guess:
                    turn_message = 'That letter is not in this word.'
                    tries -= 1
                else:
                    turn_message = 'Good guess!'
                    digit = 0
                    for i in word_to_guess:
                        if word_to_guess[digit] == guess:
                            guessed_word[digit] = guessed_word[digit].replace('_ ', i)
                        digit +=1

                # Win condition
                if '_ ' not in guessed_word:
                    msgbox('You win! Good job.', 'Win')
                    win = True
                    break

        if tries == 0:
            break

    # Lose
    if win == False:
        msgbox(f'You lose!\nThe word was {word_to_guess}.')

def main(word_to_guess):
    word_to_guess = get_word()
    game(word_to_guess=word_to_guess)

if __name__ == '__main__':
    main(word_to_guess=None)
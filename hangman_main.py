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
    while True:
        user_difficulty = buttonbox(
            'What difficulty do you want to play?\n',
            'Difficulty', ['Easy (5-6 letter words)', 'Medium (7-9 letter words)', 'Hard (10-13 letter words)']
        ) # Setting user input to lowercase and removing extra spaces
        if user_difficulty == None: # If x button clicked
            confirm_exit = ynbox('Are you sure you want to exit?', 'Exit confirmation')
            if confirm_exit:
                exit()
        else: break # Continue in loop if no

    try: # Opening the json file with word lists
        with open('words.json', 'r') as f:
            data = json.load(f)
        # Returning random word from corresponding list depending on chosen difficulty
        if user_difficulty == 'Easy (5-6 letter words)':
            return random.choice(data["easy_words"])
        elif user_difficulty == 'Medium (7-9 letter words)':
            return random.choice(data["medium_words"])
        elif user_difficulty == 'Hard (10-13 letter words)':
            return random.choice(data["hard_words"])
    except:
        print(
            'There was an error with the json word file.\n'
            'Make sure it is in the correct directory.'
        )
        exit() # Closing program to prevent further errors

def game(word_to_guess):
    guessed_word = ['_ '] * len(word_to_guess) # Setting up display of letters guessed
    all_letters = string.ascii_lowercase # All letters string to show what letters haven't been guessed
    win = False # Win condition to exit loop
    turn_message = 'Good luck!' # Setting up turn message

    # Calculate number of tries the user has depending on word length
    tries = len(word_to_guess)
    if len(word_to_guess) > 10: # No more than 10 tries max
        tries = 10

    while True: # Repeating this for the amount of tries you have
        # Displaying turn info
        while True:
            guess = enterbox(
                f'{turn_message}\n'
                f'You have {tries} tries left.\n'
                f'Letters you can guess: {all_letters}\n'
                f'{''.join(guessed_word)}\n'
                'Enter a letter to guess:',
                'Guess'
            ) # Guess input box with all needed info
            if guess == '': # Handling for pretting enter without typing anything
                msgbox('Make sure you enter a letter.', 'error')
            elif guess == None: # Handling for cancel button or x button
                confirm_exit = ynbox('Are you sure you want to exit?', 'Exit confirmation')
                if confirm_exit: # Exiting logic
                    exit()
            else:
                guess = guess.lower().strip() # lower and strip here to stop nonetype errors
                break

        if len(guess) > 1: # Making sure you can't accidentally type more than one letter
            turn_message = 'Make sure your answer is only one letter.'
        else:
            if guess not in all_letters: # Making sure you can't guess the same letter twice
                if guess not in string.ascii_letters:
                    turn_message = 'Please enter a letter.'
                else:
                    turn_message = 'You already guessed that.'
            else:
                all_letters = all_letters.replace(guess, '_ ') # Removing letter from letter list

                # Loop to replace the guessed letter as many times as it appears in the word
                if guess not in word_to_guess:
                    turn_message = 'That letter is not in this word.'
                    tries -= 1
                else:
                    turn_message = 'Good guess!' # Correct guess logic
                    digit = 0
                    for i in word_to_guess: # Checking each letter for the guess, handles multiple intances of the same letter
                        if word_to_guess[digit] == guess:
                            guessed_word[digit] = guessed_word[digit].replace('_ ', i)
                        digit +=1

                # Win condition
                if '_ ' not in guessed_word:
                    msgbox('You win! Good job.', 'Win')
                    win = True
                    break

        if tries == 0:
            break # Exit loop when you run out of triess

    # Lose
    if win == False:
        msgbox(f'You lose!\nThe word was {word_to_guess}.')

def main(word_to_guess):
    msgbox(
        'WELCOME TO HANGMAN!\n'
        'You will be able to select a difficulty, which will change the amount of letters in the word.\n\n'
        'To guess, type a letter in the input box. You will be able to see what letters you have guessed,'
        'and the amount of correct letters you already have. It is not case sensitive.\n\n'
        'The amount of tries you have is matched to the length of the word up to 10 tries.'
        'Tries will only go down for guessing incorrectly.\n\n'
        'If you manage to guess your word, you win!\nGood luck!',
        'Welcome to Hangman'
    ) # Information message box
    word_to_guess =  get_word()
    game(word_to_guess=word_to_guess)

if __name__ == '__main__':
    main(word_to_guess=None)
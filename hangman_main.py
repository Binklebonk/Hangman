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
    os.system('pip install easygui') # Using pip to install library

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

def leaderboard(write, difficulty, tries): # Leaderboard program
    cancel = False
    if write == True: # If user has chosen to add their score to the leaderboard
        score = tries
        if difficulty == 'Medium':
            score *= 1.5
        elif difficulty == 'Hard':
            score *= 2
        message = ''
        while True: # Looping until correct username length
            username = enterbox(f'{message}What is your username? No more than 12 characters.', 'Enter username')
            if username == None:
                confirm_exit = ynbox('Are you sure you want to exit?', 'Exit confirmation')
                if confirm_exit: # Exiting logic
                    cancel = True
                    break
            elif username == '':
                message = 'Please enter a username. Try again.\n'
            elif len(username) > 12:
                message = 'Username too long. Try again.\n'
            else: break
        if cancel == False:
            with open('leaderboard.json') as f: # Getting data from json file
                data = json.load(f)
            # Adding data to lists
            data["username"].append(username)
            data["difficulty"].append(difficulty)
            data["score"].append(str(score))
            with open('leaderboard.json', 'w') as f:
                json.dump(data, f, indent = 4) # Writing data

    if cancel == False:
        display = 'Username        Difficulty   Score\n'
        '-------------------------------------\n' # Formatting for display
        digit = 0
        with open('leaderboard.json') as f: # Getting leaderboard data
                data = json.load(f)
        for i in data["username"]: # Repeating for amount of users
            display += data["username"][digit] # Adding username
            for i in range(16 - len(data["username"][digit])):
                display += ' '
            display += data["difficulty"][digit] # Adding difficulty
            for i in range(13 - len(data["difficulty"][digit])):
                display += ' '
            display += data["score"][digit] # Adding tries remaining
            for i in range (3 - len(data["score"][digit])):
                display += ' '
            display += '\n'
            digit += 1
        textbox('LEADERBOARD\nRead only, edits are ignored', 'Leaderboard', display) # Textbox to print out data

def game(word_to_guess):
    guessed_word = ['_ '] * len(word_to_guess) # Setting up display of letters guessed
    all_letters = list(string.ascii_lowercase) # All letters string to show what letters haven't been guessed
    all_letters.append('Guess word')
    win = False # Win condition to exit loop
    bad_guess = False
    turn_message = 'Good luck!' # Setting up turn message

    # Calculate number of tries the user has depending on word length
    tries = len(word_to_guess) + 1
    if len(word_to_guess) > 10: # No more than 12 tries max
        tries = 10

    while True: # Repeating this for the amount of tries you have
        # Displaying turn info
        while True:
            guess = buttonbox(
                f'{turn_message}\n'
                f'You have {tries} tries left.\n'
                f'{''.join(guessed_word)}\n'
                'Select a letter to guess:',
                'Guess', all_letters
            ) # Guess input box with all needed info
            if guess == None: # Handling for cancel button or x button
                confirm_exit = ynbox('Are you sure you want to exit?', 'Exit confirmation')
                if confirm_exit: # Exiting logic
                    exit()
            else:
                break
        all_letters.remove(guess) # Removing guess from letter list

        if guess == 'Guess word': # Making sure you can't accidentally type more than one letter
            guess = enterbox('Guess the word', 'Guess')
            if guess == word_to_guess: # If the user guesses the whole word
                win = True
                add_to_leaderboard = ynbox(
                    'You guessed the word! Good job.\n'
                    'Do you want to add your score to the leaderboard?',
                    'Win'
                )
                if not add_to_leaderboard:
                    break
                if add_to_leaderboard:
                    # Setting difficulty, as it is not stored at any point
                    if len(word_to_guess) < 7:
                        difficulty = 'Easy'
                    elif len(word_to_guess) >= 7 and len(word_to_guess) < 10:
                        difficulty = 'Medium'
                    else:
                        difficulty = 'Hard'
                    leaderboard(write = True, difficulty = difficulty, tries = tries)
                    break
            else: # Lose
                tries == 0
                break

        else: # Handling for guessing letter
            if guess in list(word_to_guess):
                turn_message = 'Good guess!' # Correct guess logic
                digit = 0
                for i in word_to_guess: # Checking each letter for the guess, handles multiple intances of the same letter
                    if word_to_guess[digit] == guess:
                        guessed_word[digit] = guessed_word[digit].replace('_ ', i)
                    digit +=1
            else: # Incorrect
                turn_message = 'That letter is not in this word.'
                tries -=1

        # Win condition
        if '_ ' not in guessed_word:
            win = True
            add_to_leaderboard = ynbox(
                'You win! Good job.\n'
                'Do you want to add your score to the leaderboard?',
                'Win'
            ) # Option to write to leader board
            if not add_to_leaderboard:
                break
            if add_to_leaderboard:
                # Setting difficulty, as it is not stored at any point
                if len(word_to_guess) < 7:
                    difficulty = 'Easy'
                elif len(word_to_guess) >= 7 and len(word_to_guess) < 10:
                    difficulty = 'Medium'
                else:
                    difficulty = 'Hard'
                leaderboard(write = True, difficulty = difficulty, tries = tries)
                break

        if tries == 0: break # Exit loop when you run out of tries

    # Lose
    if win == False and bad_guess == False:
        msgbox(f'You lose!\nThe word was {word_to_guess}.')
    elif win == False and bad_guess == True:
        msgbox(f'You guessed the word incorrect. Better luck next time!\nThe word was {word_to_guess}.')

def main(word_to_guess):
    while True: # Loop to repeat back to this box once leaderboard is closed
        welcome_box = buttonbox(
            'WELCOME TO HANGMAN!\n'
            'You can select a difficulty, which will change the amount of letters in the word.\n\n'
            'To guess, type a letter in the input box. You will see what letters you have guessed, '
            'and the amount of correct letters you already have. It is not case sensitive.\n\n'
            'If you think you know what the finished word is, then type it in and guess.'
            'But be careful, you only have one try! If you guess a word and it\'s wrong, game over.\n\n'
            'The number of tries you have is matched to the length of the word, up to 10 tries.\n\n'
            'If you manage to guess your word, you win!\nGood luck!',
            'Welcome to Hangman', ['Play', 'Leaderboard', 'Exit']
        ) # Information and rules message box
        if welcome_box == 'Leaderboard':
            leaderboard(write = False, difficulty = None, tries = None)
        elif welcome_box == 'Play':
            word_to_guess = get_word()
            print(word_to_guess)
            game(word_to_guess = word_to_guess)
        else:
            confirm_exit = ynbox('Are you sure you want to exit?', 'Exit confirmation')
            if confirm_exit: # Exiting logic
                exit()

if __name__ == '__main__':
    print('This program doesn\'t work on python version 3.11.9 because of an f string error. It was written using python 3.13.9.')
    main(word_to_guess = None)
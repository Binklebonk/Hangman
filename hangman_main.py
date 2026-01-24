# Hangman project
# By Noah Dodgshun
# 32/01/2026

# Set word to guess and amount of guesses
word_to_guess = 'hello'
turns = 5

def game(word_to_guess, turns):
    # Setting up the display of what letters you have guessed
    guessed_word = ['_'] * len(word_to_guess)
    guessed_letters = []
    win = False

    for i in range(turns): # Repeating this for the amount of turns you have
        # Printing out turn info
        print(f'You have {turns - i} turns left.')
        print(f'{''.join(guessed_word)}\n')
        guess = input('Enter a letter to guess: ').lower()

        if guess in guessed_letters: # Making sure you can't guess the same letter twice
            print('You already guessed that.')
        else:
            guessed_letters.append(guess) # Adding letter to guessed letter list

            # Loop to replace the guessed letter as many times as it appears in the word
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

    # Lose
    if win == False:
        print(f'You lose! The word was {word_to_guess}.')

if __name__ == '__main__':
    game(word_to_guess=word_to_guess, turns=turns)
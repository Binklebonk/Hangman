# Hangman project
# By Noah Dodgshun
# 32/01/2026

word_to_guess = 'hello'
turns = 5

def game(word_to_guess, turns):
    guessed_word = ['_'] * len(word_to_guess)
    guessed_letters = []
    for i in range(turns):
        print(f'\nYou have {turns} turns left.')
        print(''.join(guessed_word))
        guess = input('Enter a letter to guess: ')

        if guess in guessed_letters:
            print('You already guessed that.')
        else:
            guessed_letters.append(guess)

            digit = 0
            for i in word_to_guess:
                if word_to_guess[digit] == guess:
                    guessed_word[digit] = guessed_word[digit].replace('_', i)
                digit +=1

            if guessed_word == word_to_guess:
                print(f'{guessed_word}\nYou win!')

if __name__ == '__main__':
    game(word_to_guess=word_to_guess, turns=turns)
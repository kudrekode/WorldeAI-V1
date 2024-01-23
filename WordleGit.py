import random 

#AI Init:
    
class AI:
    def __init__(self, word_list):
        self.word_list = word_list
        self.guesses = []
        self.ai_position_correct = [None] * 5
        self.correct_letters = set()  # Letters known to be in the word
        self.incorrect_letters = set()  # Letters known not to be in the word
        self.ai_guess = "crane"

    def update_with_feedback(self, game_word):
        for i in range(5):
            if self.ai_guess[i] == game_word[i]:
                self.ai_position_correct[i] = self.ai_guess[i]
                self.correct_letters.add(self.ai_guess[i])
                print(f"Correct position for character {self.ai_guess[i]} at index {i}")
            elif self.ai_guess[i] in game_word:
                self.correct_letters.add(self.ai_guess[i])
                print(f"Correct letter but wrong position for {self.ai_guess[i]}")
            else:
                self.incorrect_letters.add(self.ai_guess[i])
        
        self.guesses.append(self.ai_guess)
        self.refine_word_list()

    def refine_word_list(self):
        
        # Filter based on correct letters
        self.word_list = [word for word in self.word_list if all(
            ch in word for ch in self.correct_letters)]
        print(f"After letter inclusion filter: {len(self.word_list)} words")

        # Filter based on correct positions
        self.word_list = [word for word in self.word_list if all(
            word[i] == ch or ch is None for i, ch in enumerate(self.ai_position_correct))]
        print(f"After position filter: {len(self.word_list)} words")

        # Filter out words with incorrect letters
        self.word_list = [word for word in self.word_list if not any(
            ch in word for ch in self.incorrect_letters)]
        print(f"After incorrect letter filter: {len(self.word_list)} words")


        # Choose next guess
        if self.word_list:
            self.ai_guess = random.choice(self.word_list)
        else:
            print("No words left to guess. Check the word list or logic.")

    def generate_clue_and_update(self, game_word):
        clue = []
        local_game_word = game_word  # Local copy to mark used letters

        for i in range(5):
            if self.ai_guess[i] == local_game_word[i]:
                clue.append(f"[{self.ai_guess[i]}]")  # Correct position
                self.ai_position_correct[i] = self.ai_guess[i]
                self.correct_letters.add(self.ai_guess[i])
            elif self.ai_guess[i] in local_game_word:
                clue.append(f"({self.ai_guess[i]})")  # Correct letter, wrong position
                self.correct_letters.add(self.ai_guess[i])
                local_game_word = local_game_word.replace(self.ai_guess[i], '-', 1)
            else:
                clue.append("-")  # Incorrect letter
                self.incorrect_letters.add(self.ai_guess[i])
        
        self.guesses.append(self.ai_guess)
        print("Clue: ", "".join(clue))
        self.refine_word_list()

#Player Init:

def is_word_correct(user_inp, game_word):
    clue = []
    
    for i in range(len(user_inp)):
        if user_inp[i] == game_word[i]:

            clue.append(f"[{user_inp[i]}]")  # Letter is in the correct position

        elif user_inp[i] in game_word and user_inp[i] != game_word[i]:
            clue.append(f"({user_inp[i]})")  # Letter is correct but in the wrong position

        # Mark the letter as used in the game word
            game_word = game_word.replace(user_inp[i], '-', 1)
        else:
            clue.append("-")  # Letter is incorrect
            
    return "".join(clue)


while True: 
    with open('fiveletterwords.txt', 'r') as file:
        # Read the words and store them in a list
        content = file.read()
        words = content.split()
    random_word = random.choice(words)

    #print("Random word:", random_word)

    game_word = random_word

    guess_no = 0

    alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

#Player Game

    print("In this game you must guess the five letter word. You have six tries") 

    while True:

        while True:
            user_inp = input("Please guess a five letter word: ").lower()

            if user_inp not in words:
                print(F"This is not a valid word")

            else: 
                break

        guess_no += 1

        for char in user_inp:
            if char in alphabet_list:
                alphabet_list.remove(char)
        print(f"Remaining letters are : {alphabet_list}")

        if guess_no > 5:
            print("You have lost")
            print(f"The word was {game_word}")
            break
    
        if len(user_inp) != 5 or not user_inp.isalpha():
            print("Input should be exactly 5 alphabetic characters.")
            continue

        result = is_word_correct(user_inp, game_word)
        print("Clue:", result)

        if user_inp == game_word:
            print(f"You won in {guess_no} guess's ")
            break

#AI Game:

    ai = AI(words)

    guess_no = 0
    while ai.ai_guess != game_word and guess_no < 6:
        ai_guess = ai.ai_guess
        print(f"AI guesses: {ai_guess}")
        ai.generate_clue_and_update(game_word)
        guess_no += 1
        print(F"Guess no is: {guess_no}")
        if guess_no >= 6:
            print("The AI couldn't guess in 6 attempts.")
            break
    
    ai_guess = ai.ai_guess

    print(F"AI guess is now: {ai_guess}")    
    if ai_guess == game_word:
        print(f"The AI won in {guess_no} guesses!")
 
    play_again = input(F"Would you like to play again? (Y/N)").capitalize()
    if play_again == "N" or play_again == "No":
        break 


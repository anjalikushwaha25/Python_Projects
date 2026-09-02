import random
import time
import threading

def show_menu():
    print("-----------HANGMAN GAME-----------")
    print("1.Start Game➡️")
    print("2.View Instructions🎯")
    print("3.Exit❌")

def show_instructions():
    print("INSTRUCTIONS: ")
    print("o- Try to guess one letter at a time🤔")
    print("o- You can only guess Alphabets(a-z)🅰️")
    print("o- Each wrong guess draws part of Hangman🙅‍♂️")
    print("o- If the Hangman is complete, YOU-LOSE!😔")
    print("o- Guess before it's too late💀")
time.sleep(2)

def load_words_by_difficulty():
    with open("Game/words.txt","r") as file:
        text = file.read()
        all_words = [word.strip().lower() for word in text.split(",")]

    easy = [w for w in all_words if 4<= len(w)<= 6]
    medium = [w for w in all_words if 6<= len(w)<= 8]
    hard = [w for w in all_words if len(w)> 8]

    return easy, medium, hard


hangman_art =  {0: ("   ",
                    "   ",
                    "   "),
                1: (" o  ",
                    "   ",
                    "   "),
                2: (" o  ",
                    " | ",
                    "   "),
                3: ("  o ",
                    " /| ",
                    "   "),
                4: (" o  ",
                    "/|\\ ",
                    "   "),
                5: (" o  ",
                    "/|\\  ",
                    "/ "),
                6: (" o  ",
                    "/|\\  ",
                    "/ \\ "),}

def display_man(wrong_guesses):
    for line in hangman_art[wrong_guesses]:
        print(line)

def display_hint(hint):
    print(" ".join(hint))
def display_answer(answer):
    print(" ".join(answer))
def timed_input(prompt, timeout):
    result = [None]

    def ask():
        result[0] = input(prompt)
    thread = threading.Thread(target = ask)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return None
    return result[0]
    
def main():
    easy, medium, hard = load_words_by_difficulty()

    print("Select Difficulty level:")
    print("1.Easy\n2.Medium\n3.Hard")
    choice = input("Enter choice(1/2/3):")

    if choice == "1":
        word_list = easy
    elif choice == "2":
        word_list = medium
    elif choice == "3":
        word_list = hard
    else:
        print("Invalid Choice.\.Defaulting to Easy.")
        word_list = easy
    word = random.choice(word_list)

    answer = random.choice(word_list)
    hint = ["_"]* len(answer)
    wrong_guesses = 0
    guessed_letters = set()
    is_running = True
    
    time_limit = 30
    start_time = time.time()

    while is_running:
        elapsed_time = time.time()-start_time
        remaining_time = int(time_limit-elapsed_time)

        if remaining_time<=0:
            print("Times up!!")
            display_answer(answer)
            break
        print(f"Time Left: {remaining_time}sec")

        display_man(wrong_guesses)
        display_hint(hint)

        guess = input("Enter a letter : ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid Input")
            continue
        if guess in guessed_letters:
            print(f"{guess} is already guessed🙅‍♂️")
            continue
        guessed_letters.add(guess)

        if guess in answer:
            for i in range(len(answer)):
                if answer[i] == guess:
                    hint[i] = guess
        else:
            wrong_guesses +=1
        if "_" not in hint:
            display_man(wrong_guesses)
            display_answer(answer)
            print("Congratulations!!\nYOU WIN😁")
            is_running = False
        elif wrong_guesses >= len(hangman_art) - 1:
            display_man(wrong_guesses)
            display_answer(answer)
            print("YOU LOSE😔")
            is_running = False
if __name__ == "__main__":
    while True:
        show_menu()
        choice = input("Enter choice(1/2/3):🤔 ")

        if choice == '1':
            main()
        elif choice == '2':
            show_instructions()
        elif choice == '3':
            print("Thanks for playing😊")
            print("Good Bye🙋‍♀️")
            break
        else:
            print("Invalid Choice❌")
            print("Plz Enter 1/2/3: ")
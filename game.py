import random

# input_list = ["Rock", "Paper", "Scissor"]
while True:


    possible_action = ["rock", "paper", "scissor"]
    computer_action = random.choice(possible_action)

    print(f"\nyou chose :{gesture},computer chose :{computer_action}.\n")

    # hear starts the real technique
    if gesture == computer_action:
        print(f"both player selected {gesture}.hence its a tie!")
    elif gesture == "rock":
        if computer_action == "scissor":
            print("rock smashes scissor! you win")
        else:
            print("paper covers the rock! you lose")

    elif gesture == "paper":
        if computer_action == "rock":
            print("paper covers the rock! you win")
        else:
            print("scissor cuts the paper! you lose")

    elif gesture == "scissor":
        if computer_action == "rock":
            print("rock smashes scissor! you win")
        else:
            print("rock smashes the scissor! you lose")

    play_again = input("play again enter y/n  :")
    if play_again.lower() != "y":
        break

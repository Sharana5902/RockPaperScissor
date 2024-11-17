# Import necessary modules
import random
import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Initialize global variables
user_score = 0
computer_score = 0
rounds_played = 0
total_rounds = 0

choices = ["rock", "paper", "scissors"]

# initializing mixer
pygame.mixer.init()
     

click_sound = pygame.mixer.Sound("sounds/click.wav")  # Replace with your sound file
win_sound = pygame.mixer.Sound("sounds/win.wav")
lose_sound = pygame.mixer.Sound("sounds/lose.wav")
game_overr = pygame.mixer.Sound("sounds/game_over.wav")
bg_sound = pygame.mixer.Sound("sounds/game_bg.wav")

#set sound volume
click_sound.set_volume(1.0)
win_sound.set_volume(0.5)
lose_sound.set_volume(0.5)
game_overr.set_volume(0.7)
bg_sound.set_volume(0.4)


# Sound effects
def play_sound(sound):
    pygame.mixer.Sound.play(sound)

# Function to reset the game
def reset_game():
    global user_score, computer_score, rounds_played, total_rounds
    user_score = 0
    computer_score = 0
    rounds_played = 0
    total_rounds = 0
    result_label.config(text="Make your choice!", style="Default.TLabel")
    score_label.config(text="Score - You: 0 | Computer: 0")
    round_label.config(text="Round: 0 / 0")
    user_image_label.config(image="")
    computer_image_label.config(image="")
    start_screen()

# Function to start the game after selecting difficulty and rounds
def start_game():
    play_sound(click_sound)
    global total_rounds
    try:
        total_rounds = int(rounds_var.get())
        if total_rounds <= 0:
            raise ValueError
        difficulty_frame.pack_forget()
        game_frame.pack(fill="both", expand=True)
        round_label.config(text=f"Round: {rounds_played + 1} / {total_rounds}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number of rounds.")

# Function for computer choice based on difficulty
def get_computer_choice(difficulty, user_choice=None):
    if difficulty == "easy":
        return random.choice(choices)
    elif difficulty == "medium":
        if user_choice:
            if user_choice == "rock":
                return random.choices(["paper", "scissors", "rock"], weights=[0.5, 0.25, 0.25])[0]
            elif user_choice == "paper":
                return random.choices(["scissors", "rock", "paper"], weights=[0.5, 0.25, 0.25])[0]
            else:
                return random.choices(["rock", "paper", "scissors"], weights=[0.5, 0.25, 0.25])[0]
    elif difficulty == "hard":
        if user_choice == "rock":
            return "paper"
        elif user_choice == "paper":
            return "scissors"
        else:
            return "rock"

# Function to handle the game logic
def play_game(user_choice):
    global user_score, computer_score, rounds_played

    if rounds_played >= total_rounds:
        return  # Ignore clicks after all rounds are played
    
    play_sound(click_sound)

    # Get computer's choice
    computer_choice = get_computer_choice(difficulty.get(), user_choice)

    # Update images
    user_image_label.config(image=images[user_choice])
    computer_image_label.config(image=images[computer_choice])

    # Determine winner
    if user_choice == computer_choice:
        result = "It's a tie!"
        result_label.config(text=result, style="Tie.TLabel")
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        result = "You win this round!"
        user_score += 1
        play_sound(win_sound)
        result_label.config(text=result, style="Win.TLabel")
    else:
        result = "Computer wins this round!"
        play_sound(lose_sound)
        computer_score += 1
        result_label.config(text=result, style="Lose.TLabel")

    # Update score and round
    rounds_played += 1
    score_label.config(text=f"Score - You: {user_score} | Computer: {computer_score}")
    round_label.config(text=f"Round: {rounds_played} / {total_rounds}")

    # End game after the specified rounds
    if rounds_played == total_rounds:
        game_over()
        play_sound(click_sound)
# Function to handle game over
def game_over():
    if user_score > computer_score:
        play_sound(win_sound)
        messagebox.showinfo("Game Over", "Congratulations! You win the game!")
        
    elif user_score < computer_score:
        play_sound(game_overr)
        messagebox.showinfo("Game Over", "Better luck next time!")
        
    else:
        messagebox.showinfo("Game Over", "It's a tie!")
    reset_game()

# Function to display the start screen
def start_screen():
    game_frame.pack_forget()
    difficulty_frame.pack(fill="both", expand=True)

# Main window
window = tk.Tk()
window.title("Rock Paper Scissors")
window.geometry("800x600")
window.configure(bg="#f0f8ff")

# Center root frame
root_frame = ttk.Frame(window, padding=50, relief="solid", borderwidth=2)
root_frame.pack(fill="both", expand=True)

# Configure styles for result_label
style = ttk.Style()
style.configure("Default.TLabel", font=("Helvetica", 14, "bold"), foreground="black")
style.configure("Win.TLabel", font=("Helvetica", 14, "bold"), foreground="green")
style.configure("Lose.TLabel", font=("Helvetica", 14, "bold"), foreground="red")
style.configure("Tie.TLabel", font=("Helvetica", 14, "bold"), foreground="blue")

# Load images
images = {
    "rock": ImageTk.PhotoImage(Image.open("icons/rock.jpg").resize((100, 100))),
    "paper": ImageTk.PhotoImage(Image.open("icons/paper.jpg").resize((100, 100))),
    "scissors": ImageTk.PhotoImage(Image.open("icons/scissors.jpg").resize((100, 100))),
}
user_icon = ImageTk.PhotoImage(Image.open("icons/user.png").resize((50, 50)))
computer_icon = ImageTk.PhotoImage(Image.open("icons/computer.png").resize((50, 50)))

# Difficulty selection frame
difficulty_frame = ttk.Frame(root_frame, padding=20, relief="solid", borderwidth=2)
ttk.Label(difficulty_frame, text="Choose Difficulty:", font=("Helvetica", 16, "bold")).pack(pady=10)
difficulty = tk.StringVar(value="easy")
ttk.Radiobutton(difficulty_frame, text="Easy", variable=difficulty, value="easy").pack()
ttk.Radiobutton(difficulty_frame, text="Medium", variable=difficulty, value="medium").pack()
ttk.Radiobutton(difficulty_frame, text="Hard", variable=difficulty, value="hard").pack()

# Number of rounds input
ttk.Label(difficulty_frame, text="Enter Number of Rounds:", font=("Helvetica", 14)).pack(pady=10)
rounds_var = tk.StringVar(value="3")
ttk.Entry(difficulty_frame, textvariable=rounds_var).pack()

# Start button
ttk.Button(difficulty_frame, text="Start Game", command=start_game).pack(pady=20)


# Game frame
game_frame = ttk.Frame(root_frame, padding=20, relief="solid", borderwidth=2)

# User and computer icons
ttk.Label(game_frame, image=user_icon).pack(side="left", padx=20)
ttk.Label(game_frame, image=computer_icon).pack(side="right", padx=20)

# Display user and computer choices with images
user_image_label = ttk.Label(game_frame)
user_image_label.pack(side="left", padx=20)
computer_image_label = ttk.Label(game_frame)
computer_image_label.pack(side="right", padx=20)

# Current round display
round_label = ttk.Label(game_frame, text="Round: 0 / 0", font=("Helvetica", 12, "bold"))
round_label.pack()

# Result label
result_label = ttk.Label(game_frame, text="Make your choice!", style="Default.TLabel")
result_label.pack(pady=20)

# Score display
score_label = ttk.Label(game_frame, text="Score - You: 0 | Computer: 0", font=("Helvetica", 12, "bold"))
score_label.pack()

# Buttons for choices
button_frame = ttk.Frame(game_frame, relief="solid", borderwidth=2, padding=10)
button_frame.pack()
for choice in choices:
    ttk.Button(button_frame, text=choice.capitalize(), image=images[choice],
               compound="top", command=lambda c=choice: play_game(c)).pack(side="left", padx=10)

# Show start screen initially
start_screen()
play_sound(bg_sound)

# Run the application
window.mainloop()

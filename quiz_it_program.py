import tkinter as tk
from tkinter import simpledialog, messagebox
import random

# Variables to store questions and categorized by level and category
questions_data = {"Easy": {"Food and Drinks": [], "Science": [], "Geography": [], "Movies": [], "Pop Culture": [], "Literature": [], "History": []},
                  "Medium": {"Food and Drinks": [], "Science": [], "Geography": [], "Movies": [], "Pop Culture": [], "Literature": [], "History": []},
                  "Hard": {"Food and Drinks": [], "Science": [], "Geography": [], "Movies": [], "Pop Culture": [], "Literature": [], "History": []}}

# Function to handle the "Start Game" button click
def start_game():
    # Show a loading message before going to the main event
    loading_label = tk.Label(window, text="Loading Game...", font=("Comic Sans MS", 30, "bold"), fg="#FF6347", bg="#FCE0D6")
    loading_label.pack(pady=50)

    # Simulate loading time 
    window.after(2000, show_game_screen)

# Make a function after clicking "Start Game"
def show_game_screen():
    # Hide the loading label and the main screen
    for widget in window.winfo_children():
        widget.pack_forget() # It removes all widget from the window

    # Make a function that ask user to choose difficulty
    game_label = tk.Label(window, text="Choose Difficulty", font=("Comic Sans MS", 40, "bold"), fg="#F88379", bg="#FCE0D6")
    game_label.pack(pady=50)

    # Make the Difficulty Buttons
    easy_button = tk.Button(window, text="Easy", font=("Comic Sans MS", 20, "bold"), bg="#90EE90", fg="#FF6347", relief="raised", bd=5, command=lambda: set_difficulty("Easy"))
    easy_button.pack(pady=10)

    medium_button = tk.Button(window, text="Medium", font=("Comic Sans MS", 20, "bold"), bg="#FFFB8F", fg="#FF6347", relief="raised", bd=5, command=lambda: set_difficulty("Medium"))
    medium_button.pack(pady=10)

    hard_button = tk.Button(window, text="Hard", font=("Comic Sans MS", 20, "bold"), bg="#FF6347", fg="white", relief="raised", bd=5, command=lambda: set_difficulty("Hard"))
    hard_button.pack(pady=10)

    # Add an exit button to the top right corner
    exit_button = tk.Button(window, text="Exit", font=("Comic Sans MS", 15, "bold"), bg="#FF6347", fg="white", bd=5, command=exit_game)
    exit_button.place(x=window.winfo_width() - 80, y=10) # At the right top corner

def set_difficulty(difficulty):
    # This function is triggered when the user selects a difficulty
    print(f"Difficulty Selected: {difficulty}")

    # After a difficulty selection, show a random category
    show_random_category(difficulty)

    #List of all possible category
def show_random_category(difficulty):
    categories = ["Food and Drinks", "Science", "Geography", "Movies", "Pop Culture", "Literature", "History"]

    # Hide all existing widgets
    for widget in window.winfo_children():
        widget.pack_forget()

    # Make a text for randomizing categories
    randomizing_label = tk.Label(window, text="Randomizing Category...", font=("Comic Sans MS", 30, "bold"), fg="#FF6347", bg="#FFD8B1")
    randomizing_label.pack(pady=50)

    # Make a box for category display
    category_box = tk.Label(window, text="...", font=("Comic Sans MS", 50, "bold"), fg="#F88379", bg="#FCE0D6", width=20, height=2, relief="solid")
    category_box.pack(pady=50)

    randomize_category(category_box, categories, difficulty)

def randomize_category(category_box, categories, difficulty):
    global randomizing_active
    randomizing_active = True # Start the randomization process

    # Function to simulate randomizing through categories
    def update_category():
        if randomizing_active:
            selected_category = random.choice(categories)
            category_box.config(text=selected_category)

        # Randomize the background color for added effect
            random_color = random.choice(["#FF6347", "#90EE90", "#FFFB8F", "#FCE0D6", "#F88379"])
            window.config(bg=random_color)

    # Repeat the randomization process every 100ms if still active
    window.after(100, update_category)

    # stop the randomization

    window.after(2000, stop_randomizing, category_box, categories, difficulty)

def stop_randomizing(category_box, categories, difficulty):
    global randomizing_active
    randomizing_active = False # Stop further category updates

    # Use the last shown category as the final category
    final_category = category_box.cget("text")

    # Set the final category color and text
    category_box.config(fg="#FFFFFF", bg="#FFFB8F")
    category_box.config(text=final_category)

    # Add a message to show the category is finalized
    category_label = tk.Label(window, text=f"Final Category: {final_category}", font=("Comic Sans MS", 40, "bold"), fg="#FF6347", bg="#FCE0D6")
    category_label.pack(pady=50)
    
    # Add a delay before input questions
    window.after(2000, start_question_input, difficulty, final_category)

def start_question_input(difficulty, category):
    # Ask user to input a question
    question = simpledialog.askstring("Input", "Enter your question:", parent=window)
    if question:
        choices = []
        labels = ['a', 'b', 'c', 'd']
        for i in range (4):
            choice = simpledialog.askstring("Input", f"Enter choices {labels[i]} =", parent=window)
            choices.append(f"{labels[i]} = {choice}") 
        
        # Ask for the correct answer as either a, b, c, d
        choice_summary = "\n".join(choices)
        correct_answer = simpledialog.askstring("Input", f"Choices:\n{choice_summary}\n\nEnter the correct answer (a, b, c, d):", parent=window)

        # Validate the correct answer input
        if correct_answer not in ['a', 'b', 'c', 'd']:
            messagebox.showerror("Invalid Input", "Correct answer must be 'a', 'b', 'c', or 'd'.")
            return
        
        # Store the question, choices, and correct answer
        questions_data[difficulty][category].append({"question": question, "choices": choices, "correct_answer": correct_answer})

        # Confirm the input and show a message
        messagebox.showinfo("Question Added", f"Question: {question}\nChoice: {', '.join(choices)}\Correct_answer: {correct_answer}")
        
        # Ask if the user wants to add another question or end 
        response = messagebox.askyesno("Continue", "Do you want to add another question?")
        if response:
            show_game_screen() # Go back to difficulty selection
        else:
            save_quiz_to_file(difficulty) # End the quiz maker

                
def save_quiz_to_file(difficulty):
    # Save all questions to a text file
    with open("quiz_data.txt", "w") as file:
        for difficulty, categories in questions_data.items():
            file.write(f"Difficulty Level: {difficulty}\n")
            for category, questions in categories.items():
                if questions:  # Only write categories that have questions
                    file.write(f"  Category: {category}\n")
                    for q in questions:
                        file.write(f"    Question: {q['question']}\n")
                        file.write(f"    Choices:\n")
                        for choice in q['choices']:
                            file.write(f"    {choice}\n")
                        file.write(f"    Correct Answer: {q['correct_answer']}\n\n")

    messagebox.showinfo("Quiz Saved", "Your quiz has been saved to quiz_data.txt.")  # Shows a message that the questions have been saved
    window.after(2000, show_game_screen)

# Function to handle the "Exit" button
def exit_game():
    # Ask for confirmation before quiiting the game
    confirm_exit = messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit the game?")
    if confirm_exit:
        window.destroy()

# Set up the main screen window
window = tk.Tk()
window.title("QuizIt")
window.geometry("800x600")
window.config(bg="#FCE0D6")

# Create the window texts
title_label = tk.Label(window, text="Welcome to QuizIt!", font=("Comic Sans MS", 50, "bold"), fg="#F88379", bg="#FCE0D6")
title_label.pack(pady=50)

# Create the window text for "Start Game"
start_button = tk.Button(window, text="Start Making a Quiz", font=("Comic Sans MS", 20, "bold"), bg="#FFFB8F", fg="#FF6347", relief="raised", bd=5, command=start_game)
start_button.pack(pady=20)

# Create the window text for "Exit"
exit_button = tk.Button(window, text="Exit", font=("Comic Sans MS", 20, "bold"), bg="#90EE90", fg="#FF6347", relief="raised", bd=5, command=exit_game)
exit_button.pack(pady=20)

window.mainloop()
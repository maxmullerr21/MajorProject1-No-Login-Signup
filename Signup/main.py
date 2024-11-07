import os
import json
from tkinter import *


# Load users from the file if it exists
def load_users():
    if os.path.exists("users.txt"):
        with open("users.txt", "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}


# Save users to the file
def save_users(users):
    with open("users.txt", "w") as file:
        json.dump(users, file)


# Display a message
def show_message(message):
    for widget in body.winfo_children():
        widget.destroy()
    message_label = Label(body, text=message, font=("Helvetica", 14), anchor="center")
    message_label.pack(pady=20)
    back_button = Button(body, text="Back", command=show_main_menu, font=("Helvetica", 12))
    back_button.pack(pady=10)


# Collect user info
def collect_user_info():
    for widget in body.winfo_children():
        widget.destroy()

    Label(body, text="New User Information", font=("Helvetica", 16)).pack(pady=10)

    fields = [
        ("First Name", Entry), ("Last Name", Entry), ("Age", Entry),
        ("Gender (M/F)", Entry), ("Personality (Introvert/Extrovert)", Entry),
        ("Hobbies (comma separated)", Entry), ("Adventure Lover (True/False)", Entry),
        ("Stay In or Go Out (In/Out)", Entry), ("Likes Pets (True/False)", Entry),
        ("Morning Person (True/False)", Entry)
    ]

    entries = {}
    for field, widget in fields:
        label = Label(body, text=field)
        label.pack()
        entry = widget(body)
        entry.pack()
        entries[field] = entry

    def save_user():
        user_data = {field: entries[field].get() for field in entries}
        username = user_data["First Name"]

        # Load current users and save new user
        users = load_users()
        if username not in users:
            users[username] = user_data
            save_users(users)
            show_message("User data saved successfully!")
        else:
            show_message("Username already exists!")

    submit_button = Button(body, text="Submit", command=save_user, font=("Helvetica", 12))
    submit_button.pack(pady=10)


# Matching algorithm to generate matches based on similarity score
def generate_matches():
    users = load_users()
    if not users:
        show_message("No users found. Please add users first.")
        return

    matches = {}
    for user1 in users:
        matches[user1] = []
        user1_data = users[user1]
        for user2 in users:
            if user1 == user2:
                continue
            user2_data = users[user2]

            # Calculate similarity score based on common answers
            score = sum(
                1 for key in user1_data if key in user2_data and user1_data[key] == user2_data[key]
            )

            matches[user1].append((user2, score))

    # Sort matches by score and display them
    match_display = ""
    for user in matches:
        sorted_matches = sorted(matches[user], key=lambda x: x[1], reverse=True)
        match_display += f"{user}:\n"
        for other_user, score in sorted_matches:
            match_display += f"    {other_user}: {score} points\n"
        match_display += "\n"

    show_message(f"Matchmaking results:\n{match_display}")


# Main menu to select options
def show_main_menu():
    for widget in body.winfo_children():
        widget.destroy()

    Label(body, text="Haunted Hearts Matchmaking", font=("Helvetica", 16)).pack(pady=20)

    Button(body, text="Collect New User Input", font=("Helvetica", 12), width=20, command=collect_user_info).pack(
        pady=10)
    Button(body, text="Generate Matches", font=("Helvetica", 12), width=20, command=generate_matches).pack(pady=10)
    Button(body, text="Quit", font=("Helvetica", 12), width=20, command=window.quit).pack(pady=10)


# Main application window setup
window = Tk()
window.title("Haunted Hearts Matchmaking")
window.geometry("500x500")

body = Frame(window)
body.pack(fill=BOTH, expand=True)

# Start with the main menu
show_main_menu()

window.mainloop()
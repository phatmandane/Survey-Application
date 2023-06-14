#!/usr/bin/env python3

#By Phathu Mandane
import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry

# Create the database connection
conn = sqlite3.connect("survey_data.db")
cursor = conn.cursor()

# Create the survey_data table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS survey_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        first_name TEXT,
        last_name TEXT,
        age INTEGER,
        food TEXT,
        rating INTEGER
    )
""")

# Create the main window
root = tk.Tk()
root.title("Survey App")

# Create a frame to hold the content
content_frame = tk.Frame(root)
content_frame.pack(expand=True, fill=tk.BOTH)

# Global variables
entry_date = None
entry_first_name = None
entry_last_name = None
entry_age = None
var_food = None
rating_table = []

# Styling constants
BG_COLOR = "#F7F7F7"
FONT_FAMILY = "Arial"
FONT_SIZE = 12
BUTTON_WIDTH = 20
BUTTON_HEIGHT = 2

# Set the background color
root.config(bg=BG_COLOR)
content_frame.config(bg=BG_COLOR)
#------------------------------------------------------------------------------------------------------------------

def apply_styles():
    # Style for labels
    label_style = {"font": (FONT_FAMILY, FONT_SIZE), "bg": BG_COLOR}

    # Style for buttons
    button_style = {
        "font": (FONT_FAMILY, FONT_SIZE),
        "bg": "#4CAF50",
        "fg": "white",
        "relief": tk.RAISED,
        "width": BUTTON_WIDTH,
        "height": BUTTON_HEIGHT,
    }

    # Apply styles to labels
    for label in content_frame.winfo_children():
        if isinstance(label, tk.Label):
            label.config(label_style)

    # Apply styles to buttons
    for button in content_frame.winfo_children():
        if isinstance(button, tk.Button):
            button.config(button_style)
#-----------------------------------------------------------------------------------------------------------------

def create_data_entry_screen():
    # Clear the content frame
    clear_content_frame()

    # Create Fill out survey button
    button_fill_survey = tk.Button(
        content_frame,
        text="Fill out survey",
        command=fill_out_survey,
    )
    button_fill_survey.pack()

    # Create View survey results button
    button_view_results = tk.Button(
        content_frame,
        text="View survey results",
        command=view_survey_results,
    )
    button_view_results.pack()

    # Apply styles
    apply_styles()
#-----------------------------------------------------------------------------------------------------------------

def fill_out_survey():
    # Clear the content frame
    clear_content_frame()

    # Create labels and entry fields
    label_date = tk.Label(content_frame, text="Date:")
    label_date.pack()
    global entry_date
    entry_date = DateEntry(content_frame, date_pattern="yyyy-mm-dd")
    entry_date.pack()

    label_first_name = tk.Label(content_frame, text="First Name:")
    label_first_name.pack()
    global entry_first_name
    entry_first_name = tk.Entry(content_frame)
    entry_first_name.pack()

    label_last_name = tk.Label(content_frame, text="Last Name:")
    label_last_name.pack()
    global entry_last_name
    entry_last_name = tk.Entry(content_frame)
    entry_last_name.pack()

    label_age = tk.Label(content_frame, text="Age:")
    label_age.pack()
    global entry_age
    entry_age = tk.Entry(content_frame)
    entry_age.pack()

    label_food = tk.Label(content_frame, text="What is your favorite food?")
    label_food.pack()

    global var_food
    var_food = tk.StringVar()
    food_options = [
        ("Pizza", "Pizza"),
        ("Pasta", "Pasta"),
        ("Pap and Wors", "Pap and Wors"),
        ("Chicken stir fry", "Chicken stir fry"),
        ("Beef stir fry", "Beef stir fry"),
        ("Other", "Other")
    ]
    food_frame = tk.Frame(content_frame)
    food_frame.pack()

    for i, (text, value) in enumerate(food_options):
        radio_button = tk.Radiobutton(
            food_frame, text=text, variable=var_food, value=value)
        radio_button.pack(anchor="w")

    # Create the table
    label_table_title = tk.Label(
        content_frame, text="On a scale of 1 to 5, indicate whether you strongly agree to strongly disagree:")
    label_table_title.pack()

    table_frame = tk.Frame(content_frame)
    table_frame.pack()

    # Table headers
    headers = ["Strongly Disagree(1)", "Disagree(2)",
               "Neutral(3)", "Agree(4)", "Strongly Agree(5)"]

    for col, header in enumerate(headers):
        label_header = tk.Label(table_frame, text=header, padx=10, pady=5)
        label_header.grid(row=0, column=col+1)

    # Table rows
    statements = [
        "I like to eat out",
        "I like to watch movies",
        "I like to watch TV",
        "I like to listen to the radio",
    ]
    global rating_table
    rating_table = []
    for row, statement in enumerate(statements):
        label_statement = tk.Label(
            table_frame, text=statement, padx=10, pady=5)
        label_statement.grid(row=row+1, column=0, sticky="w")

        row_ratings = []
        for col in range(len(headers)):
            rating = tk.IntVar()
            check_button = tk.Checkbutton(
                table_frame, variable=rating, onvalue=col+1, offvalue=0)
            check_button.grid(row=row+1, column=col+1)
            row_ratings.append(rating)

        rating_table.append(row_ratings)

    # Create the Save button
    button_save = tk.Button(content_frame, text="Save", command=submit_survey)
    button_save.pack()

    apply_styles()
#---------------------------------------------------------------------------------------------------------------

def submit_survey():
    # Validate fields
    if not validate_fields():
        return

    # Get the selected ratings
    ratings = [int(rating.get()) for row in rating_table for rating in row]

    # Insert the survey data into the database
    cursor.execute(
        "INSERT INTO survey_data (date, first_name, last_name, age, food, rating) VALUES (?, ?, ?, ?, ?, ?)",
        (
            entry_date.get(),
            entry_first_name.get(),
            entry_last_name.get(),
            int(entry_age.get()),
            var_food.get(),
            sum(ratings) / len(ratings),
        ),
    )
    conn.commit()

    # Show success message
    messagebox.showinfo("Success", "Survey submitted successfully.")

    # Clear the fields
    clear_fields()

#---------------------------------------------------------------------------------------------------------------

def validate_fields():
    if not entry_date.get() or not entry_first_name.get() or not entry_last_name.get() or not entry_age.get():
        messagebox.showerror("Error", "Please fill out all fields.")
        return False

    if int(entry_age.get()) < 5 or int(entry_age.get()) > 120:
        messagebox.showerror("Error", "Please enter a valid age (5-120).")
        return False

    if var_food.get() == "":
        messagebox.showerror("Error", "Please select your favorite food.")
        return False

    for row_ratings in rating_table:
        if sum(rating.get() != 0 for rating in row_ratings) != 1:
            messagebox.showerror("Error", "Please rate one statement in the table.")
            return False

    return True

#---------------------------------------------------------------------------------------------------------------------

def view_survey_results():
    # Clear the content frame
    clear_content_frame()

    # Fetch survey data from the database
    cursor.execute("SELECT * FROM survey_data")
    survey_data = cursor.fetchall()

    if not survey_data:
        messagebox.showinfo("No Data", "No survey data available.")
        create_data_entry_screen()  # Return to the main menu
        return

    # Calculate the statistics
    total_surveys = len(survey_data)
    average_age = sum(data[4] for data in survey_data) / total_surveys
    oldest_age = max(data[4] for data in survey_data)
    youngest_age = min(data[4] for data in survey_data)
    pizza_lovers = sum(data[5] == "Pizza" for data in survey_data)
    pizza_percentage = (pizza_lovers / total_surveys) * 100
    like_to_eat_out_rating = sum(data[6] for data in survey_data) / total_surveys

    # Display the statistics
    text = f"Total Surveys: {total_surveys}\n"
    text += f"Average Age: {average_age:.1f}\n"
    text += f"Oldest Person: {oldest_age}\n"
    text += f"Youngest Person: {youngest_age}\n"
    text += f"Percentage of People who like Pizza: {pizza_percentage:.1f}%\n"
    text += f"People who like to eat out: {like_to_eat_out_rating:.1f}\n"

    # Create a text box to display the statistics
    text_box = tk.Text(content_frame, bg="white", width=60, height=20)
    text_box.insert(tk.END, text)
    text_box.pack()

    # Create the OK button to return to the main menu
    button_ok = tk.Button(content_frame, text="OK", command=create_data_entry_screen)
    button_ok.pack()

    # Apply styles
    apply_styles()

#-------------------------------------------------------------------------------------------------------------
def clear_content_frame():
    # Clear the content frame
    for child in content_frame.winfo_children():
        child.destroy()

#-------------------------------------------------------------------------------------------------------------
def clear_fields():
    # Clear the entry fields
    entry_date.delete(0, tk.END)
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    var_food.set("")


# Create the initial data entry screen
create_data_entry_screen()

# Start the main event loop
root.mainloop()

# Close the database connection
conn.close()

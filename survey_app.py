#!/usr/bin/env python3

import tkinter as tk
import sqlite3

# Create the database connection
conn = sqlite3.connect("survey.db")
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
root.title("Survey App by Phathu Mandane")

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

# Functions


def create_data_entry_screen():
    # Clear the content frame
    clear_content_frame()

    # Create Fill out survey button
    button_fill_survey = tk.Button(
        content_frame, text="Fill out survey", command=fill_out_survey)
    button_fill_survey.pack()

    # Create View survey results button
    button_view_results = tk.Button(
        content_frame, text="View survey results", command=view_survey_results)
    button_view_results.pack()


def clear_content_frame():
    for widget in content_frame.winfo_children():
        widget.pack_forget()


def fill_out_survey():
    # Clear the content frame
    clear_content_frame()

    # Create labels and entry fields
    label_date = tk.Label(content_frame, text="Date:")
    label_date.pack()
    global entry_date
    entry_date = tk.Entry(content_frame)
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

    for index, (text, value) in enumerate(food_options):
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
    button_save = tk.Button(content_frame, text="Save", command=save_data)
    button_save.pack()


def save_data():
    # Get the entered data
    date = entry_date.get()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    age = entry_age.get()
    food = var_food.get()

    # Get the selected ratings
    ratings = []
    for row in rating_table:
        row_ratings = [rating.get() for rating in row]
        ratings.append(row_ratings)

    # Save the data to the database
    cursor.execute("INSERT INTO survey_data (date, first_name, last_name, age, food, rating_1, rating_2, rating_3, rating_4, rating_5) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (date, first_name, last_name, age, food, *ratings))
    conn.commit()

    # Clear the entry fields
    entry_date.delete(0, tk.END)
    entry_first_name.delete(0, tk.END)
    entry_last_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    var_food.set("")  # Unselect the food option
    for row in rating_table:
        for rating in row:
            rating.set(0)  # Unselect the ratings

    # Redirect to the "View Survey Results" screen
    view_survey_results()



    


def view_survey_results():
    # Clear the content frame
    clear_content_frame()

    # Execute SQL queries to calculate results
    cursor.execute("SELECT COUNT(*) FROM survey_data")
    total_surveys = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(age) FROM survey_data")
    avg_age = cursor.fetchone()[0]

    cursor.execute("SELECT MAX(age) FROM survey_data")
    oldest_age = cursor.fetchone()[0]

    cursor.execute("SELECT MIN(age) FROM survey_data")
    youngest_age = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM survey_data WHERE food = 'Pizza'")
    pizza_count = cursor.fetchone()[0]
    percentage_pizza = (pizza_count / total_surveys) * 100

    cursor.execute("SELECT AVG(rating) FROM survey_data")
    avg_rating = cursor.fetchone()[0]

    # Display the calculated results
    label_total_surveys = tk.Label(
        content_frame, text="Total Surveys: {}".format(total_surveys))
    label_total_surveys.pack()

    label_avg_age = tk.Label(
        content_frame, text="Average Age: {:.1f}".format(avg_age))
    label_avg_age.pack()

    label_oldest_age = tk.Label(
        content_frame, text="Oldest Age: {}".format(oldest_age))
    label_oldest_age.pack()

    label_youngest_age = tk.Label(
        content_frame, text="Youngest Age: {}".format(youngest_age))
    label_youngest_age.pack()

    label_percentage_pizza = tk.Label(
        content_frame, text="Percentage of People Who Like Pizza: {:.1f}%".format(percentage_pizza))
    label_percentage_pizza.pack()

    label_avg_rating = tk.Label(
        content_frame, text="Average Rating: {:.1f}".format(avg_rating))
    label_avg_rating.pack()

    # Create the OK button to return to the main menu
    button_ok = tk.Button(content_frame, text="OK",
                          command=create_data_entry_screen)
    button_ok.pack()


# Initial UI setup
create_data_entry_screen()

# Configure window to adapt with resolution
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Start the Tkinter event loop
root.mainloop()

# Close the database connection
conn.close()

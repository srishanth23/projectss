# Graphical BMI Calculator using Tkinter

import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL)''')
conn.commit()

def get_user_input():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        if weight > 0 and height > 0:
            return weight, height
        else:
            raise ValueError("Weight and height must be positive values.")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
        return None

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_record(name, weight, height, bmi, category):
    c.execute("INSERT INTO bmi_records (name, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
              (name, weight, height, bmi, category))
    conn.commit()

def calculate_and_display_bmi():
    name = entry_name.get()
    user_input = get_user_input()
    if user_input:
        weight, height = user_input
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        save_record(name, weight, height, bmi, category)
        lbl_result.config(text=f"Your BMI is {bmi:.2f}, which is classified as {category}.")

def view_records():
    c.execute("SELECT * FROM bmi_records")
    records = c.fetchall()
    for record in records:
        print(record)

def plot_bmi_trends():
    c.execute("SELECT id, bmi FROM bmi_records")
    data = c.fetchall()
    if data:
        ids, bmis = zip(*data)
        plt.plot(ids, bmis, marker='o')
        plt.xlabel('Record ID')
        plt.ylabel('BMI')
        plt.title('BMI Trends')
        plt.show()
    else:
        messagebox.showinfo("No Data", "No BMI records found to plot.")

# Tkinter GUI setup
root = tk.Tk()
root.title("BMI Calculator")

lbl_name = tk.Label(root, text="Name:")
lbl_name.grid(row=0, column=0)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1)

lbl_weight = tk.Label(root, text="Weight (kg):")
lbl_weight.grid(row=1, column=0)
entry_weight = tk.Entry(root)
entry_weight.grid(row=1, column=1)

lbl_height = tk.Label(root, text="Height (m):")
lbl_height.grid(row=2, column=0)
entry_height = tk.Entry(root)
entry_height.grid(row=2, column=1)

btn_calculate = tk.Button(root, text="Calculate BMI", command=calculate_and_display_bmi)
btn_calculate.grid(row=3, column=0, columnspan=2)

lbl_result = tk.Label(root, text="")
lbl_result.grid(row=4, column=0, columnspan=2)

btn_view = tk.Button(root, text="View Records", command=view_records)
btn_view.grid(row=5, column=0, columnspan=2)

btn_plot = tk.Button(root, text="Plot BMI Trends", command=plot_bmi_trends)
btn_plot.grid(row=6, column=0, columnspan=2)

root.mainloop()

# Close the database connection
conn.close()

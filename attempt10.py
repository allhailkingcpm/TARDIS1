import tkinter as tk
from math import *
from PIL import Image, ImageTk
from docx import Document
from tkinter import filedialog

# Dictionary to store user-defined variables
user_variables = {}

def update_formatted_output():
    try:
        # Retrieve the equation from the input text widget
        input_text = input_text_widget.get("1.0", tk.END).strip()

        # Replace variable names with their values
        for var_name, var_value in user_variables.items():
            input_text = input_text.replace(var_name, str(var_value))

        # Calculate the result of highlighted numbers
        try:
            selected_text = input_text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            result = eval(selected_text)
            input_text = input_text.replace(selected_text, str(result))
        except Exception:
            pass

        # Display the formatted output on the right side
        formatted_output = format_equation(input_text)
        output_label.config(text=formatted_output)
    except Exception as e:
        # Display error in the output label
        output_label.config(text=f"Error: {str(e)}")

def format_equation(equation):
    # Custom formatting for certain expressions
    equation = equation.replace("sqrt", "√")
    return equation

def calculate_selected_equation():
    try:
        # Retrieve the equation from the input text widget
        selected_text = input_text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        result = eval(selected_text, {"__builtins__": None}, {"sqrt": sqrt, "log": log, "sin": sin, "cos": cos, "tan": tan, "pi": pi})
        output_label.config(text=f"Result: {result}")
    except Exception as e:
        # Display error in the output label
        output_label.config(text=f"Error: {str(e)}")

def clear_text_widgets():
    input_text_widget.delete("1.0", tk.END)
    output_label.config(text="")

def set_variable():
    variable_name = entry_variable_name.get()
    variable_value = entry_variable_value.get()

    try:
        # Attempt to evaluate the variable value
        evaluated_value = eval(variable_value, {"__builtins__": None}, {"sqrt": sqrt, "log": log, "sin": sin, "cos": cos, "tan": tan, "pi": pi})
        user_variables[variable_name] = evaluated_value
        update_variable_list()
    except Exception as e:
        # Handle invalid expressions
        output_label.config(text=f"Error: {str(e)}")

def update_variable_list():
    # Update the list of variables in the UI
    variable_list_label.config(text=f"User Variables: {', '.join(user_variables.keys())}")

def save_as_word():
    # Ask the user for the file path to save the Word document
    file_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")])

    if file_path:
        # Create a Word document
        document = Document()
        # Add the formatted output to the document
        document.add_paragraph(output_label.cget("text"))
        # Save the document
        document.save(file_path)

# Create the main application window
root = tk.Tk()
root.title("TARDIS")
root.geometry("1080x720")  # Set initial window size
root.resizable(True, True)  # Allow window resizing

# Use Pillow to open and resize the icon
icon_path = 'C:/Users/Owner/Desktop/Program/TARDISicon.ico'  # Replace with the actual path to your icon
icon = Image.open(icon_path)
icon = icon.resize((32, 48))  # Resize as needed
icon = ImageTk.PhotoImage(icon)

# Set the icon for the window title bar
root.iconphoto(False, icon)

# Set the icon for the taskbar using root.tk.call (this might work on some systems)
root.tk.call('wm', 'iconphoto', root._w, icon)

# Create a canvas to simulate a border
border_canvas = tk.Canvas(root, bd=0, highlightthickness=0, bg='#1E4E79')  # Use the color code for a darker blue
border_canvas.pack(expand=True, fill="both", padx=10, pady=10)
border_canvas.pack_propagate(0)  # Prevent the canvas from affecting the size of its children

# Create an input text widget for equation input on the left side
input_text_widget = tk.Text(border_canvas, wrap=tk.WORD, font=('Arial', 12), height=10, width=40)  # Change font and size
input_text_widget.pack(side=tk.LEFT, padx=10, pady=10)  # Add padding

# Create a label on the right side to display the formatted output
output_label = tk.Label(border_canvas, text="", font=('Arial', 12), height=10, width=40, anchor='w', justify='left')  # Change font and size
output_label.pack(side=tk.RIGHT, padx=10, pady=10, fill='both')  # Add padding

# Create a button to calculate the selected equation
calculate_button = tk.Button(border_canvas, text="Calculate", command=calculate_selected_equation, bg='#007BFF', fg='white', font=('Arial', 12))  # Change button style
calculate_button.pack(pady=10)  # Add padding

# Create a button to update the formatted output
update_button = tk.Button(border_canvas, text="Update", command=update_formatted_output, bg='#007BFF', fg='white', font=('Arial', 12))  # Change button style
update_button.pack(pady=10)  # Add padding

# Create a button to clear the text widgets and result label
clear_button = tk.Button(border_canvas, text="Clear", command=clear_text_widgets, bg='red', fg='white', font=('Arial', 12))  # Change button style
clear_button.pack(pady=10)  # Add padding

# Create a button to save as Word
save_as_word_button = tk.Button(border_canvas, text="Save as Word", command=save_as_word, bg='#007BFF', fg='white', font=('Arial', 12))  # Change button style
save_as_word_button.pack(pady=10)  # Add padding

# Create widgets for setting variables
entry_variable_name_label = tk.Label(border_canvas, text="Variable Name:")
entry_variable_name_label.pack()

entry_variable_name = tk.Entry(border_canvas)
entry_variable_name.pack()

entry_variable_value_label = tk.Label(border_canvas, text="Variable Value:")
entry_variable_value_label.pack()

entry_variable_value = tk.Entry(border_canvas)
entry_variable_value.pack()

set_variable_button = tk.Button(border_canvas, text="Set Variable", command=set_variable, bg='#007BFF', fg='white', font=('Arial', 12))
set_variable_button.pack(pady=10)

# Label to display the list of user variables
variable_list_label = tk.Label(border_canvas, text="User Variables:")
variable_list_label.pack()

# Run the application
root.mainloop()

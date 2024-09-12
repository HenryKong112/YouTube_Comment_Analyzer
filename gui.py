from tkinter import *
from tkinter import filedialog
from pathlib import Path
import vader as v
from tkinter import messagebox
import BERTopic_analysis as ba

def browsefunc(filepath_entry):
    """
    Opens a file dialog to select a file and updates the entry widget with the file path.
    
    Args:
        filepath_entry (Entry): The Entry widget to update with the selected file path.
    """
    try:
        # Open file dialog to select a file with .xlsx or .csv extension
        filename = filedialog.askopenfilename(filetypes=[("Excel/CSV files", "*.xlsx; *.csv")])
        if filename:
            filepath_entry.delete(0, "end")  # Clear the entry field
            filepath_entry.insert(0, filename)  # Insert the selected file path
            global get_name
            get_name = Path(filename).stem  # Store the file name without extension
    except Exception as e:
        # Show error message if file selection fails
        messagebox.showerror("ERROR", f"Failed to open the file. Error: {e}")

def main():
    """
    Creates the main window for the text analysis application and sets up the GUI components.
    """
    # Initialize the main window
    window = Tk()
    window.title("Text Analysis")
    window.geometry('600x200')

    # Entry widget for displaying and entering the file path
    filepath_entry = Entry(window)
    
    # Button to open the file dialog
    browse_btn = Button(window, text="Browse", command=lambda: browsefunc(filepath_entry))
    
    # Buttons for different analysis functions
    vader_btn = Button(window, text="Sentiment Analysis (VADER)", command=lambda: v.vader(filepath_entry.get(), get_name))
    BERTopic_btn = Button(window, text="Topic Modelling (BERTopic)", command=lambda: ba.bert_visual(filepath_entry.get()))
    
    # Label for the entry widget
    select_file_label = Label(window, text="Select csv / excel file: ")

    # Layout the widgets using grid geometry
    select_file_label.grid(row=0, column=0)
    filepath_entry.grid(row=0, column=1, columnspan=4)
    browse_btn.grid(row=0, column=5)
    vader_btn.grid(row=1, column=1, pady=10)
    BERTopic_btn.grid(row=2, column=1, pady=10)
    
    # Start the main event loop
    window.mainloop()

# Run the main function to start the application
main()

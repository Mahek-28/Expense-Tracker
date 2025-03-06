from tkinter import *
from tkinter import ttk, messagebox
from mydb import Database
import datetime as dt
import matplotlib.pyplot as plt

# Initialize database
db = Database("myexpense.db")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

# Global variables
selected_rowid = 0

def save_record():
    """Save a new record to the database."""
    if item_name.get() and item_amt.get() and transaction_date.get():
        db.insertRecord(item_name.get(), float(item_amt.get()), transaction_date.get())
        refresh_data()
        clear_entries()
        messagebox.showinfo("Success", "Record saved successfully!")
    else:
        messagebox.showwarning("Input Error", "Please fill all fields before saving.")

def set_current_date():
    """Set the current date in the date entry field."""
    current_date = dt.datetime.now().strftime("%Y-%m-%d")
    transaction_date.set(current_date)

def clear_entries():
    """Clear all input fields."""
    item_name.set("")
    item_amt.set("")
    transaction_date.set("")

def refresh_data():
    """Refresh the data in the table view."""
    for item in tv.get_children():
        tv.delete(item)
    records = db.fetchRecord("SELECT rowid, item_name, item_price, purchase_date FROM expense_record")
    for record in records:
        tv.insert("", "end", values=record)

def select_record(event):
    """Select a record from the table view."""
    global selected_rowid
    selected = tv.focus()
    values = tv.item(selected, "values")

    if values:
        selected_rowid = values[0]
        item_name.set(values[1])
        item_amt.set(values[2])
        transaction_date.set(values[3])

def update_record():
    """Update the selected record in the database."""
    if selected_rowid:
        db.updateRecord(item_name.get(), float(item_amt.get()), transaction_date.get(), selected_rowid)
        refresh_data()
        clear_entries()
        messagebox.showinfo("Update", "Record updated successfully!")
    else:
        messagebox.showwarning("Update", "No record selected to update.")

def delete_record():
    """Delete the selected record from the database."""
    if selected_rowid:
        db.removeRecord(selected_rowid)
        refresh_data()
        clear_entries()
        messagebox.showinfo("Delete", "Record deleted successfully!")
    else:
        messagebox.showwarning("Delete", "No record selected to delete.")

def export_data():
    """Export records to a CSV file."""
    db.export_to_csv("expenses.csv")
    messagebox.showinfo("Export", "Data exported successfully to expenses.csv")

def import_data():
    """Import records from a CSV file."""
    db.import_from_csv("expenses.csv")
    refresh_data()
    messagebox.showinfo("Import", "Data imported successfully from expenses.csv")

def plot_expense_trends():
    """Plot expense trends over time using matplotlib."""
    db.plot_expense_trends()

def get_total_expense():
    """Calculate and display total expense."""
    try:
        records = db.fetchRecord("SELECT rowid, item_name, item_price, purchase_date FROM expense_record")
        total = 0.0
        for record in records:
            try:
                total += float(record[2])  # Convert to float before summing
            except ValueError:
                print(f"Skipping invalid entry: {record}")  # Log invalid records
        
        messagebox.showinfo("Total Expense", f"Total Expense: ${total:.2f}")
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")

def show_expense_pie_chart():
    """Show expenses in a pie chart by month."""
    try:
        monthly_expenses = db.analyze_monthly_expenses()
        
        if not monthly_expenses:
            messagebox.showwarning("No Data", "No expense data available for chart.")
            return
        
        months = list(monthly_expenses.keys())
        amounts = list(monthly_expenses.values())

        plt.figure(figsize=(8, 6))
        plt.pie(amounts, labels=months, autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
        plt.title("Expense Distribution by Month")
        plt.axis("equal")  # Equal aspect ratio ensures pie is drawn as a circle
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Unexpected error: {e}")



# GUI Initialization
ws = Tk()
ws.title("Expense Manager")
ws.geometry("900x600")
ws.configure(bg="#f0f8ff")

# Fonts and styles
label_font = ("Arial", 14)
button_font = ("Arial", 12, "bold")
button_bg = "#4682b4"
button_fg = "white"

# Input variables
item_name = StringVar()
item_amt = StringVar()
transaction_date = StringVar()

# Layout setup
Label(ws, text="Expense Manager", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)

frame_top = Frame(ws, bg="#f0f8ff")
frame_top.pack(pady=10)

frame_buttons = Frame(ws, bg="#f0f8ff")
frame_buttons.pack(pady=10)

frame_table = Frame(ws, bg="#f0f8ff")
frame_table.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Top Frame Inputs
Label(frame_top, text="Item Name:", font=label_font, bg="#f0f8ff").grid(row=0, column=0, padx=10, pady=5, sticky=E)
Entry(frame_top, textvariable=item_name, font=label_font).grid(row=0, column=1, padx=10, pady=5)

Label(frame_top, text="Item Price:", font=label_font, bg="#f0f8ff").grid(row=1, column=0, padx=10, pady=5, sticky=E)
Entry(frame_top, textvariable=item_amt, font=label_font).grid(row=1, column=1, padx=10, pady=5)

Label(frame_top, text="Date (YYYY-MM-DD):", font=label_font, bg="#f0f8ff").grid(row=2, column=0, padx=10, pady=5, sticky=E)
Entry(frame_top, textvariable=transaction_date, font=label_font).grid(row=2, column=1, padx=10, pady=5)
Button(frame_top, text="Set Current Date", font=button_font, bg=button_bg, fg=button_fg, command=set_current_date).grid(row=2, column=2, padx=10, pady=5)

# Button Frame
Button(frame_buttons, text="Save Record", font=button_font, bg=button_bg, fg=button_fg, command=save_record).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Update Record", font=button_font, bg=button_bg, fg=button_fg, command=update_record).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Delete Record", font=button_font, bg=button_bg, fg=button_fg, command=delete_record).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Clear Fields", font=button_font, bg=button_bg, fg=button_fg, command=clear_entries).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Export to CSV", font=button_font, bg=button_bg, fg=button_fg, command=export_data).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Import from CSV", font=button_font, bg=button_bg, fg=button_fg, command=import_data).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Show Trends", font=button_font, bg=button_bg, fg=button_fg, command=plot_expense_trends).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Show Total Expense", font=button_font, bg=button_bg, fg=button_fg, command=get_total_expense).pack(side=LEFT, padx=10)
Button(frame_buttons, text="Show Expense Chart", font=button_font, bg=button_bg, fg=button_fg, command=show_expense_pie_chart).pack(side=LEFT, padx=10)


# Table Frame
columns = ("ID", "Item Name", "Item Price", "Purchase Date")
tv = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)
for col in columns:
    tv.heading(col, text=col)
    tv.column(col, anchor="center")

tv.pack(fill=BOTH, expand=True)
tv.bind("<ButtonRelease-1>", select_record)

# Populate Data
refresh_data()

ws.mainloop()



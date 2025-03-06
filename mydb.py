import sqlite3
import csv
import datetime as dt
from collections import defaultdict
import matplotlib.pyplot as plt


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS expense_record (item_name TEXT, item_price FLOAT, purchase_date DATE)"
        )
        self.conn.commit()

    def fetchRecord(self, query, params=None):
        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error fetching records: {e}")
            return []

    def insertRecord(self, item_name, item_price, purchase_date):
        try:
            self.cur.execute(
                "INSERT INTO expense_record (item_name, item_price, purchase_date) VALUES (?, ?, ?)",
                (item_name, item_price, purchase_date),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting record: {e}")

    def removeRecord(self, rowid):
        try:
            self.cur.execute("DELETE FROM expense_record WHERE rowid = ?", (rowid,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting record: {e}")

    def updateRecord(self, item_name, item_price, purchase_date, rid):
        try:
            self.cur.execute(
                "UPDATE expense_record SET item_name = ?, item_price = ?, purchase_date = ? WHERE rowid = ?",
                (item_name, item_price, purchase_date, rid),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating record: {e}")

    def export_to_csv(self, filename):
        try:
            data = self.fetchRecord("SELECT rowid, item_name, item_price FROM expense_record")
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["RowID", "Item Name", "Item Price"])
                writer.writerows(data)
            print(f"Data successfully exported to {filename}")
        except Exception as e:
            print(f"Error exporting data to CSV: {e}")

    # def import_from_csv(self, filename):
    #     try:
    #         with open(filename, mode="r") as file:
    #             reader = csv.DictReader(file)
    #             for row in reader:
    #                 self.insertRecord(row["Item Name"], float(row["Item Price"]), row["Purchase Date"])
    #         print(f"Data successfully imported from {filename}")
    #     except Exception as e:
    #         print(f"Error importing data from CSV: {e}")

    def import_from_csv(self, filename):
        try:
            with open(filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    item_name = row["Item Name"]
                    item_price = float(row["Item Price"])
                    purchase_date = row["Purchase Date"].strip() if "Purchase Date" in row and row["Purchase Date"].strip() else dt.datetime.now().strftime("%Y-%m-%d")

                    self.insertRecord(item_name, item_price, purchase_date)
            print(f"Data successfully imported from {filename}")
        except Exception as e:
            print(f"Error importing data from CSV: {e}")


    def analyze_monthly_expenses(self):
        try:
            data = self.fetchRecord("SELECT item_price, purchase_date FROM expense_record")
            monthly_totals = defaultdict(float)
            for price, date in data:
                month_year = dt.datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")
                monthly_totals[month_year] += price

            return monthly_totals
        except Exception as e:
            print(f"Error analyzing monthly expenses: {e}")
            return {}

    def plot_expense_trends(self):
        try:
            data = self.fetchRecord("SELECT purchase_date, SUM(item_price) FROM expense_record GROUP BY purchase_date")
            dates = [dt.datetime.strptime(row[0], "%Y-%m-%d") for row in data]
            amounts = [row[1] for row in data]

            plt.figure(figsize=(10, 6))
            plt.bar(dates, amounts, color="skyblue")
            plt.title("Daily Expense Trends", fontsize=16)
            plt.xlabel("Date", fontsize=14)
            plt.ylabel("Total Expenses", fontsize=14)
            plt.xticks(rotation=45, fontsize=10)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"Error plotting expense trends: {e}")

    def analyze_monthly_expenses(self):
        """Fetch total expense per month."""
        try:
            self.cur.execute("SELECT item_price, purchase_date FROM expense_record")
            data = self.cur.fetchall()
            monthly_totals = defaultdict(float)

            for price, date in data:
                month_year = dt.datetime.strptime(date, "%Y-%m-%d").strftime("%B %Y")
                monthly_totals[month_year] += float(price)

            return monthly_totals
        except Exception as e:
           print(f"Error analyzing monthly expenses: {e}")
           return {}  

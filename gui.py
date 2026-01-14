import sys
import os
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deta.team_member import process_member_shifts, load_days, skill_file

class OverworkSelector(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Overwork Selector")
        self.pack(fill="both", expand=True)

        self.create_widgets()

    def create_widgets(self):
        # --- Input Frame ---
        input_frame = ttk.LabelFrame(self, text="Input")
        input_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(input_frame, text="Year:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.year_entry = ttk.Entry(input_frame, width=10)
        self.year_entry.grid(row=0, column=1, padx=5, pady=5)
        self.year_entry.insert(0, "2026")

        ttk.Label(input_frame, text="Month:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.month_entry = ttk.Entry(input_frame, width=5)
        self.month_entry.grid(row=0, column=3, padx=5, pady=5)
        self.month_entry.insert(0, "3")

        ttk.Label(input_frame, text="Start Date:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.start_date_entry = ttk.Entry(input_frame, width=12)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_date_entry.insert(0, "2026-03-01")

        ttk.Label(input_frame, text="End Date:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.end_date_entry = ttk.Entry(input_frame, width=12)
        self.end_date_entry.grid(row=1, column=3, padx=5, pady=5)
        self.end_date_entry.insert(0, "2026-03-31")

        # --- Teams Frame ---
        teams_frame = ttk.LabelFrame(self, text="Teams")
        teams_frame.pack(padx=10, pady=5, fill="x")

        self.team_vars = {}
        for i, team in enumerate(["A", "B", "C", "D"]):
            var = tk.StringVar(value=team)
            cb = ttk.Checkbutton(teams_frame, text=team, variable=var, onvalue=team, offvalue="")
            cb.grid(row=0, column=i, padx=5, pady=5)
            self.team_vars[team] = var
            cb.invoke() # Select all by default

        # --- Action Button ---
        self.load_button = ttk.Button(self, text="Load Data and Calculate Workdays", command=self.load_and_calculate)
        self.load_button.pack(padx=10, pady=10)

        # --- Results Frame ---
        results_frame = ttk.LabelFrame(self, text="Member Workdays")
        results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.member_listbox = tk.Listbox(results_frame, selectmode="extended")
        self.member_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.member_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.member_listbox.config(yscrollcommand=scrollbar.set)

    def load_and_calculate(self):
        self.member_listbox.delete(0, tk.END)

        try:
            year = int(self.year_entry.get())
            month = int(self.month_entry.get())
            start_date = self.start_date_entry.get()
            end_date = self.end_date_entry.get()
            selected_teams = [var.get() for var in self.team_vars.values() if var.get()]
        except ValueError:
            self.member_listbox.insert(tk.END, "Error: Year and Month must be numbers.")
            return

        if not selected_teams:
            self.member_listbox.insert(tk.END, "Error: Please select at least one team.")
            return
            
        daily_data = process_member_shifts(year, month, start_date, end_date, selected_teams)

        if not daily_data:
            self.member_listbox.insert(tk.END, f"No data found for the specified period.")
            return

        # Calculate workdays
        workday_counts = defaultdict(int)
        all_members_by_team = load_days("", skill_file)
        
        for date, team_info in daily_data.items():
            for team_code, data in team_info.items():
                if team_code in selected_teams:
                    for member in data.get("attendance", set()):
                        workday_counts[member] += 1
        
        # Sort members by workdays
        sorted_members = sorted(workday_counts.items(), key=lambda item: item[1], reverse=True)

        # Populate listbox
        if not sorted_members:
            self.member_listbox.insert(tk.END, "No attendance data found for the selected teams.")
            return

        for member, count in sorted_members:
            self.member_listbox.insert(tk.END, f"{member}: {count} days")

if __name__ == "__main__":
    root = tk.Tk()
    app = OverworkSelector(master=root)
    root.geometry("400x500")
    app.mainloop()

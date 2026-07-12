import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import pandas as pd

# ==========================================
# 1. CORE FUNCTIONS (Excel, Sheets, & Search)
# ==========================================

# Mock data for demonstration
COMMANDS = {
    "Write Excel": "Generates a local Excel file with your data.",
    "Sync Google Sheets": "Uploads and syncs your local data to the cloud.",
    "Automate Backup": "Runs the spreadsheet writer automatically on a timer."
}

def write_to_excel():
    """Simulates writing to a local Excel file"""
    data = {"Item": ["Apples", "Bananas"], "Quantity": [10, 20]}
    df = pd.DataFrame(data)
    df.to_excel("inventory.xlsx", index=False)
    return "Successfully saved to inventory.xlsx!"

def write_to_google_sheet():
    """Placeholder for Google Sheets API logic"""
    # In a real app, your gspread code would go here
    time.sleep(1) # Simulating network delay
    return "Successfully synced with Google Sheets cloud!"


# ==========================================
# 2. AUTOMATION BACKGROUND WORKER
# ==========================================
class AutomationWorker:
    def __init__(self):
        self.is_running = False
        self.thread = None

    def start(self, interval_seconds, task_function, log_callback):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(
                target=self._loop, 
                args=(interval_seconds, task_function, log_callback), 
                daemon=True
            )
            self.thread.start()

    def stop(self):
        self.is_running = False

    def _loop(self, interval, task, log_callback):
        while self.is_running:
            log_callback("Automation triggered: Running task...")
            result = task()
            log_callback(f"Result: {result}")
            
            # Sleep in small increments so it responds quickly if stopped
            for _ in range(interval):
                if not self.is_running:
                    break
                time.sleep(1)

automation_worker = AutomationWorker()

# ==========================================
# 3. USER INTERFACE (Tkinter)
# ==========================================
class SpreadsheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spreadsheet Automation Tool")
        self.root.geometry("500x450")
        
        # --- Section 1: Command Search ---
        lbl_search = tk.Label(root, text="Search Tool Commands:", font=("Arial", 10, "bold"))
        lbl_search.pack(pady=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.update_search)
        self.search_bar = tk.Entry(root, textvariable=self.search_var, width=40)
        self.search_bar.pack(pady=2)
        
        self.search_results = tk.Listbox(root, height=3, width=50)
        self.search_results.pack(pady=5)
        self.update_search() # Populate list initially
        
        # --- Section 2: Manual Tasks ---
        lbl_tasks = tk.Label(root, text="Manual Actions:", font=("Arial", 10, "bold"))
        lbl_tasks.pack(pady=10)
        
        btn_excel = tk.Button(root, text="Run: Write Local Excel", command=self.run_excel, bg="#4CAF50", fg="white")
        btn_excel.pack(pady=2)
        
        btn_sheets = tk.Button(root, text="Run: Sync Google Sheets", command=self.run_sheets, bg="#2196F3", fg="white")
        btn_sheets.pack(pady=2)
        
        # --- Section 3: Automation Scheduler ---
        lbl_auto = tk.Label(root, text="Automation Settings:", font=("Arial", 10, "bold"))
        lbl_auto.pack(pady=10)
        
        frame_auto = tk.Frame(root)
        frame_auto.pack()
        
        tk.Label(frame_auto, text="Interval (seconds):").grid(row=0, column=0, padx=5)
        self.entry_interval = tk.Entry(frame_auto, width=5)
        self.entry_interval.insert(0, "10") # Default to 10 seconds
        self.entry_interval.grid(row=0, column=1, padx=5)
        
        self.btn_toggle_auto = tk.Button(frame_auto, text="Start Automation", command=self.toggle_automation, bg="orange")
        self.btn_toggle_auto.grid(row=0, column=2, padx=5)
        
        # --- Section 4: Output Log ---
        self.log_box = tk.Text(root, height=6, width=55, state="disabled", bg="#f0f0f0")
        self.log_box.pack(pady=15)
        self.log("System initialized. Ready.")

    def log(self, message):
        """Helper to print timestamps and logs inside the GUI text box"""
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

    def update_search(self, *args):
        """Filters the command listbox based on search input"""
        query = self.search_var.get().lower()
        self.search_results.delete(0, tk.END)
        for cmd, desc in COMMANDS.items():
            if query in cmd.lower() or query in desc.lower():
                self.search_results.insert(tk.END, f"{cmd} - {desc}")

    def run_excel(self):
        msg = write_to_excel()
        self.log(msg)
        messagebox.showinfo("Success", msg)

    def run_sheets(self):
        self.log("Starting cloud sync...")
        msg = write_to_google_sheet()
        self.log(msg)
        messagebox.showinfo("Success", msg)

    def toggle_automation(self):
        if automation_worker.is_running:
            automation_worker.stop()
            self.log("Automation stopped.")
            self.btn_toggle_auto.config(text="Start Automation", bg="orange")
        else:
            try:
                seconds = int(self.entry_interval.get())
                # Using write_to_excel as the target automation task
                automation_worker.start(seconds, write_to_excel, self.log)
                self.log(f"Automation started! Running every {seconds} seconds.")
                self.btn_toggle_auto.config(text="Stop Automation", bg="red", fg="white")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of seconds.")

# --- Application Entry Point ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SpreadsheetApp(root)
    root.mainloop()

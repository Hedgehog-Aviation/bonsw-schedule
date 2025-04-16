from datetime import datetime, timedelta
from fpdf import FPDF
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def generate_bus_schedule(start_time_str):
    start_time = datetime.strptime(start_time_str, "%H:%M")
    stops = [
        "Depot",
        "Southern Terminal Stand A",
        "Shopping Centre Stand B",
        "Wallaby Dr after Eucalyptus Dr",
        "Wallaby Dr at Dharug St",
        "Cockatoo St at Ironbark Rd",
        "Telapea Cres before Kaartdijin Rd",
        "Bowling Club, Stand A"
    ]
    intervals = [3, 3, 1, 1, 1, 1, 1, 1]
    schedule = []

    current_time = start_time
    for i, stop in enumerate(stops):
        if i > 0:
            current_time += timedelta(minutes=intervals[i-1])
        schedule.append((stop, current_time.strftime("%H:%M")))

    return schedule

def create_pdf(schedule, route_number, filename="Route702_Schedule.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Route {route_number} Bus Schedule", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Courier", size=12)
    page_width = pdf.w - 2 * pdf.l_margin

    for stop, time in schedule:
        stop_name_width = len(stop) * 5
        pdf.set_x(pdf.l_margin)
        pdf.cell(stop_name_width, 10, stop)
        pdf.set_x(page_width - 40)
        pdf.cell(40, 10, time, align='R')
        pdf.ln(10)

    pdf.output(filename)
    print(f"✅ PDF saved as {filename}")

    try:
        if os.name == 'nt':
            subprocess.run(["start", filename], shell=True)
        elif os.name == 'posix':
            subprocess.run(["open", filename])
        else:
            print("❌ Unsupported OS for opening PDF automatically.")
    except Exception as e:
        print(f"❌ Failed to open the PDF: {e}")

def on_submit(entry, window):
    start_time = entry.get()
    try:
        datetime.strptime(start_time, "%H:%M")
        schedule = generate_bus_schedule(start_time)
        create_pdf(schedule, route_number="702")
        window.destroy()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter the time in HH:MM format (24hr).")

def main():
    root = tk.Tk()
    root.title("BONSW Schedule Maker")

    tk.Label(root, text="Enter Start Time (HH:MM, 24hr):", font=("Arial", 12)).pack(pady=10)
    time_entry = tk.Entry(root, font=("Arial", 12), justify='center')
    time_entry.pack(pady=5)
    time_entry.insert(0)  # default value

    submit_button = tk.Button(root, text="Generate Schedule", font=("Arial", 12),
                              command=lambda: on_submit(time_entry, root))
    submit_button.pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()

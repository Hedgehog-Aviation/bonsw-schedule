from datetime import datetime, timedelta
from fpdf import FPDF
import os
import subprocess
import tkinter as tk
from tkinter import messagebox, StringVar

def generate_bus_schedule(start_time_str, route_number):
    start_time = datetime.strptime(start_time_str, "%H:%M")

    dummy_routes = {
        "700": (["A", "B", "C", "D", "E"], [0, 1, 1, 1, 1]),
        "701": (["A", "B", "C", "D", "E"], [0, 1, 1, 1, 1]),
        "702": (["Depot", "Southern Terminal Stand A", "Shopping Centre Stand B",
                  "Wallaby Dr after Eucalyptus Dr", "Wallaby Dr at Dharug St",
                  "Cockatoo St at Ironbark Rd", "Telapea Cres before Kaartdijin Rd",
                  "Bowling Club, Stand A"], [3, 3, 1, 1, 1, 1, 1, 1]),
        "702S": (["A", "B", "C", "D", "E"], [0, 1, 1, 1, 1]),
        "703a": (["A", "B", "C", "D", "E"], [0, 1, 1, 1, 1]),
        "703c": (["A", "B", "C", "D", "E"], [0, 1, 1, 1, 1]),
        "704": (["A", "B", "C", "D", "E"], [0, 1, 1, 1, 1]),
        "630": (["A", "B", "C", "D", "E"], [0, 1, 1, 1, 1])
    }

    stops, intervals = dummy_routes.get(route_number, ([], []))
    schedule = []
    current_time = start_time

    for i, stop in enumerate(stops):
        if i > 0:
            current_time += timedelta(minutes=intervals[i])
        schedule.append((stop, current_time.strftime("%H:%M")))

    return schedule

def create_pdf(schedule, route_number, filename=None):
    if filename is None:
        filename = f"Route{route_number}_Schedule.pdf"

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
    print(f"\u2705 PDF saved as {filename}")

    try:
        if os.name == 'nt':
            subprocess.run(["start", filename], shell=True)
        elif os.name == 'posix':
            subprocess.run(["open", filename])
        else:
            print("\u274C Unsupported OS for opening PDF automatically.")
    except Exception as e:
        print(f"\u274C Failed to open the PDF: {e}")

def on_submit(time_entry, route_var, window):
    start_time = time_entry.get()
    route_number = route_var.get()
    try:
        datetime.strptime(start_time, "%H:%M")
        schedule = generate_bus_schedule(start_time, route_number)
        create_pdf(schedule, route_number)
        window.destroy()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter the time in HH:MM format (24hr).")

def main():
    root = tk.Tk()
    root.title("NSW Roblox Bus Schedule Maker")

    tk.Label(root, text="Select Route:", font=("Arial", 12)).pack(pady=5)

    route_var = StringVar(root)
    route_var.set("702")  # default route
    route_options = ["700", "701", "702", "702S", "703a", "703c", "704", "630"]
    route_dropdown = tk.OptionMenu(root, route_var, *route_options)
    route_dropdown.config(font=("Arial", 12))
    route_dropdown.pack(pady=5)

    tk.Label(root, text="Enter Start Time (HH:MM, 24hr):", font=("Arial", 12)).pack(pady=10)
    time_entry = tk.Entry(root, font=("Arial", 12), justify='center')
    time_entry.pack(pady=5)
    time_entry.insert(0, "07:00")

    submit_button = tk.Button(root, text="Generate Schedule", font=("Arial", 12),
                              command=lambda: on_submit(time_entry, route_var, root))
    submit_button.pack(pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()

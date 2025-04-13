from datetime import datetime, timedelta
from fpdf import FPDF
import os
import subprocess
import tkinter as tk
from tkinter import simpledialog

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
    # Updated time intervals between each stop
    intervals = [1, 3, 1, 1, 1, 1, 1]  # intervals in minutes for each pair of stops
    schedule = []
    
    current_time = start_time
    for i, stop in enumerate(stops):
        if i > 0:  # Skip the first stop (Depot) since it has no interval
            current_time += timedelta(minutes=intervals[i-1])  # Add interval for the current stop
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

    # Get the width of the page to calculate the position of the times on the right
    page_width = pdf.w - 2 * pdf.l_margin
    
    for stop, time in schedule:
        # Calculate the space for the stop name
        stop_name_width = len(stop) * 5  # Approximate width of stop name in Courier font
        
        # Position the stop name on the left side and the time on the right side
        pdf.set_x(pdf.l_margin)
        pdf.cell(stop_name_width, 10, stop)  # Write the stop name
        
        # Position the time on the right side
        pdf.set_x(page_width - 40)  # Adjust 40 for a gap between the time and stop name
        pdf.cell(40, 10, time, align='R')  # Write the time aligned to the right
        
        pdf.ln(10)  # Move to the next line

    # Save the PDF in the current working directory
    pdf.output(filename)
    print(f"✅ PDF saved as {filename}")

    # Open the generated PDF file using the default PDF viewer
    try:
        if os.name == 'nt':  # For Windows
            subprocess.run(["start", filename], shell=True)
        elif os.name == 'posix':  # For MacOS or Linux
            subprocess.run(["open", filename])
        else:
            print("❌ Unsupported OS for opening PDF automatically.")
    except Exception as e:
        print(f"❌ Failed to open the PDF: {e}")

def get_start_time_from_gui():
    # Set up the GUI window
    root = tk.Tk()
    root.withdraw()  # Hide the root window (we only want the input dialog)

    # Prompt the user to enter the start time in HH:MM format
    start_time = simpledialog.askstring("Start Time", "Enter the start time (HH:MM, 24hr format):", parent=root)

    if start_time:
        try:
            # Check if the input time is in the correct format
            datetime.strptime(start_time, "%H:%M")
            return start_time
        except ValueError:
            print("❌ Invalid time format. Please use HH:MM (24hr).")
            return None
    else:
        print("❌ No time entered. Please try again.")
        return None

def main():
    print("🚌 NSW Roblox Bus Schedule Maker")
    route_number = "702"

    start_time = get_start_time_from_gui()
    
    if start_time:
        schedule = generate_bus_schedule(start_time)
        create_pdf(schedule, route_number)

if __name__ == "__main__":
    main()


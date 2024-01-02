import tkinter as tk
from tkinter import ttk
import subprocess
import threading

def run_ping_command():
    process = subprocess.Popen(
        'ping google.com -t',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )

    while True:
        line = process.stdout.readline()
        if not line:
            break

        # Update text widget without deleting previous content
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, line)
        text_widget.config(state=tk.DISABLED)
        text_widget.see(tk.END)  # Auto-scroll to the end

        # Print to the console
        print(line, end='')

    process.wait()

def check_for_output():
    # Check for new output after 100 milliseconds
    text_widget.after(100, check_for_output)

root = tk.Tk()
root.title("Tkinter App with Ping Output")

button = tk.Button(root, text="Start Ping", command=lambda: threading.Thread(target=run_ping_command, daemon=True).start())
button.pack(pady=20)

# Create a text widget with a scroll bar
text_widget = tk.Text(root, height=25, width=160, state=tk.DISABLED)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(root, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the text widget to use the scroll bar
text_widget.config(yscrollcommand=scrollbar.set)

# Start the periodic check for new output
check_for_output()

root.mainloop()

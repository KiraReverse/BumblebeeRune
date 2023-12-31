


import tkinter as tk
from tkinter import ttk
import subprocess

class UVicornApp:
    def __init__(self, master):
        self.master = master
        master.title("Run UVicorn FastAPI Server")

        # Create a text widget for displaying logs
        self.log_text = tk.Text(master, height=10, width=60)
        self.log_text.pack(pady=10)
        self.log_text.config(state=tk.DISABLED)  # Disable text widget for writing

        # Create a button to start the UVicorn server
        self.start_button = ttk.Button(master, text="Start UVicorn Server", command=self.start_uvicorn_server)
        self.start_button.pack(pady=10)

    def start_uvicorn_server(self):
        # Replace 'your_fastapi_module:app' with the appropriate module and app instance
        # command = 'uvicorn your_fastapi_module:app --reload'
        command = 'uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001'

        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # Read and display output in real-time
            while True:
                line = process.stdout.readline()
                if not line:
                    break

                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, line)
                self.log_text.config(state=tk.DISABLED)
                self.log_text.yview(tk.END)

            process.wait()

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UVicornApp(root)
    root.mainloop()

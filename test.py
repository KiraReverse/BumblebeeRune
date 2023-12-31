import tkinter as tk
from tkinter import ttk
import subprocess
import threading

class UVicornApp:
    def __init__(self, master):
        self.master = master
        master.title("Run UVicorn FastAPI Server")

        self.log_text = tk.Text(master, height=10, width=60)
        self.log_text.pack(pady=10)
        self.log_text.config(state=tk.DISABLED)

        self.start_button = ttk.Button(master, text="Start UVicorn Server", command=self.start_uvicorn_server)
        self.start_button.pack(pady=10)

        # Bind the closing event to the stop_uvicorn_server method
        master.protocol("WM_DELETE_WINDOW", self.stop_uvicorn_server)

    def start_uvicorn_server(self):
        command = 'uvicorn your_fastapi_module:app --reload'

        # Disable the button after it's pressed
        self.start_button.config(state=tk.DISABLED)

        # Run the command in a separate thread
        self.process_thread = threading.Thread(target=self.run_command, args=(command,), daemon=True)
        self.process_thread.start()

    def run_command(self, command):
        try:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            while True:
                line = self.process.stdout.readline()
                if not line:
                    break

                self.master.after(10, self.update_log, line)

            self.process.wait()

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Enable the button after the process/thread finishes
            self.start_button.config(state=tk.NORMAL)

    def update_log(self, line):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, line)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.yview(tk.END)

    def stop_uvicorn_server(self):
        # Stop the uvicorn server and wait for the process to finish
        if hasattr(self, 'process') and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()

        # Wait for the thread to finish
        if hasattr(self, 'process_thread') and self.process_thread.is_alive():
            self.process_thread.join()

        # Close the Tkinter window
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UVicornApp(root)
    root.mainloop()

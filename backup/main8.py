import tkinter as tk
from tkinter import messagebox
import requests
import threading
import uvicorn


from PyInstaller.utils.hooks import collect_submodules

hiddenimports = collect_submodules('uvicorn')
from PyInstaller.utils.hooks import get_package_paths

datas = [(get_package_paths('uvicorn')[1], 'uvicorn')]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FastAPI Tkinter GUI")

        self.label = tk.Label(root, text="Counter:")
        self.label.pack()

        self.counter_label = tk.Label(root, text="0")
        self.counter_label.pack()

        self.increment_button = tk.Button(root, text="Increment", command=self.increment_counter)
        self.increment_button.pack()

        self.start_server_button = tk.Button(root, text="Start Server", command=self.start_fastapi_server)
        self.start_server_button.pack()

        self.stop_server_button = tk.Button(root, text="Stop Server", command=self.stop_fastapi_server, state=tk.DISABLED)
        self.stop_server_button.pack()

        self.fastapi_thread = None

    def increment_counter(self):
        try:
            response = requests.post("http://127.0.0.1:8000/increment")
            data = response.json()
            counter_value = data.get("counter", "Error")
            self.counter_label.config(text=counter_value)
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Failed to increment counter: {e}")

    def start_fastapi_server(self):
        if not self.fastapi_thread or not self.fastapi_thread.is_alive():
            self.fastapi_thread = threading.Thread(target=self.run_fastapi)
            self.fastapi_thread.start()
            self.start_server_button.config(state=tk.DISABLED)
            self.stop_server_button.config(state=tk.NORMAL)
            messagebox.showinfo("Info", "FastAPI server started.")
        else:
            messagebox.showwarning("Warning", "FastAPI server is already running.")

    def stop_fastapi_server(self):
        if self.fastapi_thread and self.fastapi_thread.is_alive():
            self.fastapi_thread.join(timeout=1)  # Wait for the thread to finish
            self.start_server_button.config(state=tk.NORMAL)
            self.stop_server_button.config(state=tk.DISABLED)
            messagebox.showinfo("Info", "FastAPI server stopped.")
        else:
            messagebox.showwarning("Warning", "FastAPI server is not running.")

    def run_fastapi(self):
        try:
            # uvicorn.run("fastapi_server:app", host="127.0.0.1", port=8000, log_level="info")
            uvicorn.run("fastapi_server:app", host="127.0.0.1", port=8000)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start FastAPI server: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

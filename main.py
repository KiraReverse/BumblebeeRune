import tkinter as tk
import subprocess
import threading
import queue
import msvcrt
from PIL import Image, ImageTk
import signal
import os
import psutil

class PollingThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify")
        
        photo=ImageTk.PhotoImage(file='icon.ico')
        root.iconphoto(False,photo)

        self.ping_process = None
        self.is_ping_running = False
        self.polling_thread = None
        self.queue = queue.Queue()

        # Create a single button
        self.toggle_button = tk.Button(root, text="Start", command=self.toggle_ping,
                                       bg="#8aff8a", width=12, height=3)
        self.toggle_button.pack(pady=20, padx=10)

        # Create a text widget with a scroll bar
        self.text_widget = tk.Text(root, height=25, width=160, state=tk.DISABLED)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(root, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the text widget to use the scroll bar
        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.terminated=False
        
        self.root.protocol("WM_DELETE_WINDOW", self.execute_on_exit)

    def run_ping_command(self):        
        command = [
            # sys.executable,  # Path to the Python interpreter
            # '-m', 'uvicorn',
            "C:\\Users\\Screwdriver\\AppData\\Local\\Programs\\Python\\Python38\\Scripts\\uvicorn.exe",
            'pytorch_solver:app',
            '--host', '192.168.0.130',  # Adjust the host and port as needed
            '--port', '8001',
        ]
        CREATE_NEW_PROCESS_GROUP = 0x00000200  # note: could get it from subprocess
        DETACHED_PROCESS = 0x00000008          # 0x8 | 0x200 == 0x208
        self.ping_process = subprocess.Popen(
            # 'ping google.com -t',
            # *command,
            # 'uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001',
            'uvicorn pytorch_solver:app --host 127.0.0.1 --port 8001',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,  # Line buffering
            # creationflags=DETACHED_PROCESS,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )

        while not self.polling_thread.stopped():
            try:
                line = self.ping_process.stdout.readline()
                print(f'{line}', end='')
                if not line:
                    break

                if 'Uvicorn' in line:
                    line = '\nLoading finished ..\n'
                elif 'INFO' in line:
                    line = '\n'
                # Update text widget without deleting previous content
                self.text_widget.config(state=tk.NORMAL)
                self.text_widget.insert(tk.END, line)
                self.text_widget.config(state=tk.DISABLED)
                self.text_widget.see(tk.END)  # Auto-scroll to the end

                # Print to the console
                # print(line, end='')
            except msvcrt.Kernel32Error:
                # Ignore errors when there's no data to read
                print(f'Kernel32Error?')
                pass
            finally:
                # print(f'finally polling_thread stopped?')
                pass

        self.ping_process.terminate()  # Terminate the ping process

    def check_for_output(self):
        while not self.queue.empty():
            message = self.queue.get()
            if message == "Stop":
                self.polling_thread.stop()

        if self.is_ping_running and not self.polling_thread.is_alive():
            self.queue.put("Stop")  # Send a message to the thread to stop
            self.polling_thread.join()  # Wait for the thread to finish
            self.is_ping_running = False
            self.toggle_button.config(text="Start", bg="#8aff8a")  # Light green

        self.root.after(100, self.check_for_output)

    def toggle_ping(self):
        if not self.is_ping_running:
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.insert(tk.END, 'Rune Solver Model is launching. Please wait .. ')
            self.is_ping_running = True
            self.polling_thread = PollingThread(target=self.run_ping_command)
            self.polling_thread.start()
            self.toggle_button.config(text="Stop", bg="#ff8a8a")  # Light red
        else:
            self.is_ping_running = False
            self.queue.put("Stop")  # Send a message to the thread to stop
            self.toggle_button.config(state=tk.DISABLED, text="Stopped", bg="grey")
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.insert(tk.END, '\nProcess is terminated. Please restart to use again. Thank you. ')
            self.text_widget.config(state=tk.DISABLED)
            self.text_widget.see(tk.END)  # Auto-scroll to the end
            # self.polling_thread.stop()  # Wait for the thread to finish            
            # self.ping_process.send_signal(signal.CTRL_C_EVENT)
            parent = psutil.Process(self.ping_process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
            self.terminated=True
            # self.ping_process.terminate()
            # self.ping_process.kill()
            # self.toggle_button.config(text="Start", bg="#8aff8a")  # Light green
            # self.root.after(100, lambda: self.toggle_button.config(state=tk.NORMAL,text="Start", bg="#8aff8a"))  # Re-enable after 100ms

    def execute_on_exit(self):
        try:
            if not self.terminated:
                parent = psutil.Process(self.ping_process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
        finally:
            self.root.destroy()

        # try:
        #     parent = psutil.Process(self.ping_process.pid)
        #     for child in parent.children(recursive=True):
        #         child.terminate()
        #     parent.terminate()
        #     self.root.destroy()
        # except:
        #     print(f'no pid. ')
        #     parent.terminate()
        #     self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PingApp(root)
    root.after(100, app.check_for_output)  # Start the periodic check for new output
    root.mainloop()

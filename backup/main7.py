from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk
import subprocess
import threading
# import queue
# import select
# import signal
# import os
import asyncio
import sys
import asyncio.subprocess
from PIL import Image, ImageTk

class TkinterAsyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Runesolver")
        photo=ImageTk.PhotoImage(file='icon.ico')
        root.iconphoto(False,photo)
        self.log_text = tk.Text(root, wrap=tk.WORD, width=90, height=20)
        self.log_text.grid(row=0, column=0, sticky="nsew")  # Expand in all directions
        self.log_text.config(state=tk.DISABLED)
        scrollbar = tk.Scrollbar(root, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        # # Create a Text widget to display the ping results
        # self.text_widget = tk.Text(root, wrap=tk.WORD, width=80, height=30)
        # self.text_widget.grid(row=0, column=0, sticky="nsew")

        # Create a button to start and stop the ping process
        self.button = tk.Button(root, text="Start Ping", command=self.toggle_ping)
        self.button.grid(row=1, column=0, pady=10)

        # Event loop for handling async tasks
        self.loop = asyncio.new_event_loop()

        # Executor for running coroutines in a separate thread
        self.executor = ThreadPoolExecutor(max_workers=1)

        # Task object to manage the async task
        self.ping_task = None

        # Variable to track the ping state
        self.ping_running = False
        
        
        # self.root.protocol("WM_DELETE_WINDOW", self.stop_uvicorn_server)
        # self.output_queue = queue.Queue()
        self.task = None
        self.process_run_uvicorn = None
        self.show = True
        # self.blacklist = [b'conv', b'route', b'upsample', b'max', b'detection', b'shortcut', b'layer']
        self.blacklist = [b'com']

    def toggle_ping(self):
        if not self.ping_running:
            self.start_ping()
        else:
            self.stop_ping()

    def start_ping(self):
        self.ping_running = True
        self.button.config(text="Stop Ping")
        self.ping_task = asyncio.run_coroutine_threadsafe(self.run_ping(), self.loop)

    def stop_ping(self):
        self.ping_running = False
        self.button.config(text="Start Ping")
        if self.ping_task:
            self.ping_task.cancel()

    async def ping_google(self):
        try:
            DETACHED_PROCESS = 0x00000008
            # process = await asyncio.create_subprocess_exec(
            #     "ping", "google.com", "-t",
            #     stdout=asyncio.subprocess.PIPE,
            #     stderr=asyncio.subprocess.PIPE,
            #     creationflags=DETACHED_PROCESS,
            # )
            command = [
                # sys.executable,  # Path to the Python interpreter
                # '-m', 'uvicorn',
                "C:\\Users\\Screwdriver\\AppData\\Local\\Programs\\Python\\Python38\\Scripts\\uvicorn.exe",
                'pytorch_solver:app',
                '--host', '192.168.0.130',  # Adjust the host and port as needed
                '--port', '8001',
            ]

            process = await asyncio.create_subprocess_exec(
            #     "ping", "google.com", "-t",
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=DETACHED_PROCESS,
            )
            

            # while True:
            #     if not self.ping_running:
            #         break
            #     line = await process.stdout.readline()
            #     if not line:
            #         break
            #     # Update the Text widget with the ping results
            #     self.text_widget.insert(tk.END, line.decode())
            #     self.text_widget.see(tk.END)
            
            
            self.update_label_text(f"Welcome to BumbleBee Runesolver .. \n")
            self.update_label_text(f"Loading model .. This may take up to 10 seconds.  \n")
            
            async def read_stream(stream, name):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    if self.show:
                        # if b'conv' in line.strip():
                        if any(x in line.strip() for x in self.blacklist):
                            pass
                        else:
                            # print(f"{line.strip()}")
                            # self.update_label_text(f"{line.strip()}\n")
                            self.update_label_text(f"{line.decode()}")
                    if name == 'stderr':
                        if b'Uvicorn running' in line.strip():
                            self.show=True
                            self.update_label_text(f"Finished loading .. \n")
                            self.update_label_text(f"Bumblebee Runesolver successfully launched .. \n")
            
            stdout_task = asyncio.create_task(read_stream(process.stdout, 'stdout'))
            stderr_task = asyncio.create_task(read_stream(process.stderr, 'stderr'))
            await process.wait()        
            await asyncio.gather(stdout_task, stderr_task)

        except asyncio.CancelledError:
            pass

        finally:
            if process.returncode is None:
                process.terminate()

    
    def update_label_text(self, line):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, line)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.yview(tk.END)

    async def run_ping(self):
        while self.ping_running:
            await self.ping_google()
    
    def run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

def main():
    root = tk.Tk()
    app = TkinterAsyncApp(root)    
    # Start the event loop in a separate thread
    threading.Thread(target=app.loop.run_forever, daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()

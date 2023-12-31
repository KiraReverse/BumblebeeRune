import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import queue
import select
import signal
import os
import asyncio
import sys
import asyncio.subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageTk   

class UVicornApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Runesolver")
        photo=ImageTk.PhotoImage(file='icon.ico')
        root.iconphoto(False,photo)
        self.log_text = tk.Text(root, wrap=tk.WORD, width=90, height=20)
        self.log_text.grid(row=0, column=0, sticky="nsew")  # Expand in all directions
        scrollbar = tk.Scrollbar(root, command=self.log_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_text.config(yscrollcommand=scrollbar.set)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        # self.log_text = tk.Text(root, height=20, width=90)
        # self.log_text.pack(pady=10)
        # self.log_text.config(state=tk.DISABLED)
        # self.start_button = ttk.Button(root, text="Start Runesolver", command=self.start_async_task)
        # self.start_button.pack(pady=10)
        # self.stop_button = tk.Button(root, text="Stop", command=self.stop_async_task)
        # self.stop_button.pack(pady=10)
        self.root.protocol("WM_DELETE_WINDOW", self.stop_uvicorn_server)        
        self.output_queue = queue.Queue()
        self.loop = asyncio.new_event_loop()
        # self.executor = ThreadPoolExecutor(max_workers=1)
        self.task = None
        self.process_run_uvicorn = None
        self.show = False
        
        self.task = asyncio.run_coroutine_threadsafe(self.async_task(), self.loop)

    def start_async_task(self):
        self.task = asyncio.run_coroutine_threadsafe(self.async_task(), self.loop)

    def stop_async_task(self):
        if self.task:
            self.task.cancel()
        if self.process_run_uvicorn.returncode is None:
            self.process_run_uvicorn.terminate()

    async def async_task(self):
        try:
            uvicorn_task = asyncio.create_task(self.run_uvicorn())
            await uvicorn_task
            # await asyncio.sleep(20)
            self.update_label_text("Runesolver started. ")
            return "Async task"
        except asyncio.CancelledError:
            self.update_label_text("Runesolver stopped. ")
            print(f'cancel .. Runesolver stopped. ')

    def update_label_text(self, line):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, line)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.yview(tk.END)
    
    def stop_uvicorn_server(self):
        print(f'close button pressed')        
        if self.task:
            self.task.cancel()
        # if self.process_run_uvicorn is not None:
        if self.process_run_uvicorn.returncode is None:
            self.process_run_uvicorn.terminate()
        self.root.destroy()    
            
    async def run_uvicorn(self):
        # command = 'uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001'
        command = [
            sys.executable,  # Path to the Python interpreter
            '-m', 'uvicorn',
            'pytorch_solver:app',
            '--host', '192.168.0.130',  # Adjust the host and port as needed
            '--port', '8001',
        ]

        self.process_run_uvicorn = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        self.update_label_text(f"Welcome to BumbleBee Runesolver .. \n")
        self.update_label_text(f"Loading model .. This may take up to 10 seconds.  \n")
        
        async def read_stream(stream, name):
            while True:
                line = await stream.readline()
                if not line:
                    break
                if self.show:
                    if b'conv' in line.strip():
                        pass
                    else:
                        # print(f"{line.strip()}")
                        self.update_label_text(f"{line.strip()}\n")
                if name == 'stderr':
                    if b'Uvicorn running' in line.strip():
                        self.show=True
                        self.update_label_text(f"Finished loading .. \n")
                        self.update_label_text(f"Bumblebee Runesolver successfully launched .. \n")
        
        stdout_task = asyncio.create_task(read_stream(self.process_run_uvicorn.stdout, 'stdout'))
        stderr_task = asyncio.create_task(read_stream(self.process_run_uvicorn.stderr, 'stderr'))
        await self.process_run_uvicorn.wait()        
        await asyncio.gather(stdout_task, stderr_task)

    def run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

async def main():
    root = tk.Tk()
    app = UVicornApp(root)
    threading.Thread(target=app.run_event_loop, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    asyncio.run(main())

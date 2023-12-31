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


class UVicornApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Run UVicorn FastAPI Server")
        master.title("Run UVicorn FastAPI Server2")

        self.log_text = tk.Text(master, height=50, width=180)
        self.log_text.pack(pady=10)
        self.log_text.config(state=tk.DISABLED)

        self.start_button = ttk.Button(master, text="Start UVicorn Server", command=self.start_uvicorn_server)
        self.start_button.pack(pady=10)
        
        # Create a button to stop the async task
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_async_task)
        self.stop_button.pack(pady=10)

        
        self.master.protocol("WM_DELETE_WINDOW", self.stop_uvicorn_server)
        
        self.output_queue = queue.Queue()  # Queue to collect lines from the subprocess
        self.queue = queue.Queue()  # Queue to collect lines from the subprocess

        self.process = None
        self.t = None
        
        # Event loop for handling async tasks
        self.loop = asyncio.new_event_loop()

        # Executor for running coroutines in a separate thread
        self.executor = ThreadPoolExecutor(max_workers=1)

        self.task = None



    def run_async_task(self):
        print(f'running async task')
        # task = asyncio.create_task(self.async_task())
        # task.add_done_callback(lambda future: self.update_label_text(future.result()))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            result = loop.run_until_complete(self.async_task())
            loop.call_soon_threadsafe(lambda: self.update_label_text(result))
            print(f'{result =}')
        finally:
            # loop.close()
            print(f'running async task finished. ')
        print(f'running async task finished2. ')

    async def async_task(self):
        try:
            # Simulate an asynchronous task
            # command = 'uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001'
            # self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            uvicorn_task = asyncio.create_task(self.run_uvicorn())
            print(f'awaiting uvicorn task. ')
            await uvicorn_task
            print(f'awaiting uvicorn task2. ')
            await asyncio.sleep(22)
            print(f'uvicorn task sleep2 finished. ')
            # Run uvicorn in the background
            # uvicorn_task = asyncio.create_task(self.run_uvicorn())
            # # Wait for uvicorn to complete (you can set a timeout if desired)
            # await uvicorn_task
            self.update_label_text("Async task completed!")
            return "Async task completed!"
        except asyncio.CancelledError:
            # Handle cancellation
            self.update_label_text("Async task cancelled!")
            print(f'no cancel!')

    def start_uvicorn_server(self):
        # command = 'uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001'
        # self.start_button.config(state=tk.DISABLED)
        # # # Run the command in a separate thread
        # self.process_thread = threading.Thread(target=self.run_command, args=(command,), daemon=True)
        # self.process_thread.start()
        # # Start a separate thread to read lines from the output queue and update the log
        # threading.Thread(target=self.read_from_queue, daemon=True).start()


        print(f'a button is pressed. ')
        # threading.Thread(target=self.run_async_task).start()
        # Run the async task in the asyncio event loop
        self.task = asyncio.run_coroutine_threadsafe(self.async_task(), self.loop)
        print(f'a button is pressed2. ')


    def stop_async_task(self):
        # Cancel the ongoing async task if it exists
        if self.task:
            self.task.cancel()


    def run_command(self, command):
        try:
            self.process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

            # # while True:
            # while self.process.poll() is None:
            #     print(f'self process poll? ..')
            #     line = self.process.stdout.readline()
            #     # if not line:
            #     if line == '':
            #         print(f'no line ..')
            #         # break
            #     # Use after to update the GUI on the main thread
            #     self.master.after(10, self.update_log, line)
            
            # for line in iter(self.process.stdout.readline, ''):
            #     if not line:
            #         break
            #     self.output_queue.put(line)
            

            # self.t = threading.Thread(target=self.enqueue_output, args=(self.process.stdout, self.output_queue, ), daemon=True)
            # self.t.start()

            print(f'what r we waiting here ..')
            # self.process.wait()
            print(f'what r we waiting here2? ..')

        except Exception as e:
            print(f"Error: {e}")
        finally:
            print(f'everything ended? ..')
            # Enable the button after the process/thread finishes
            # self.start_button.config(state=tk.NORMAL)

    def update_label_text(self, line):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, line)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.yview(tk.END)

    def update_log(self, line):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, line)
        self.log_text.config(state=tk.DISABLED)
        self.log_text.yview(tk.END)
    
    
    def stop_uvicorn_server(self):
        print(f'close button pressed')

        if self.process is not None:
            # Stop the uvicorn server and wait for the process to finish
            if hasattr(self, 'process') and self.process.poll() is None:
                print(f'if has process ..')
                self.process.terminate()
                self.process.wait()
                self.process.send_signal(signal.SIGTERM)
                print(f'if has process finished..')

            # Wait for the thread to finish
            if hasattr(self, 'process_thread') and self.process_thread.is_alive():
                print(f'if has process_thread ..')
                self.process_thread.join()
                print(f'if has process_thread finished ..')

            if self.t is not None:
                if hasattr(self, 't') and self.t.is_alive():
                    print(f'if has t ..')
                    # self.t.join()
                    print(f'if has t finished..')
        
        if self.process_run_uvicorn is not None:
            if hasattr(self, 'process_run_uvicorn'):
                print(f'if has process_run_uvicorn ..')
                self.process_run_uvicorn.terminate()
                # self.process_run_uvicorn.wait()
                self.process_run_uvicorn.send_signal(signal.SIGTERM)
                print(f'if has process_run_uvicorn finished..')

        # Close the Tkinter window
        self.master.destroy()
    
    def read_from_queue(self):
        # Read lines from the output queue and update the log
        while True:
            try:
                line = self.output_queue.get_nowait()
                self.master.after(10, self.update_log, line)
            except queue.Empty:
                pass

            # Check if the process has finished and the queue is empty
            if self.process is not None and self.process.poll() is not None and self.output_queue.empty():
                break
        
    def enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

        

    
    async def run_uvicorn(self):
        # command = 'uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001'
        command = [
            sys.executable,  # Path to the Python interpreter
            '-m', 'uvicorn',
            'pytorch_solver:app',
            '--host', '192.168.0.130',  # Adjust the host and port as needed
            '--port', '8001',
            # '--reload',  # Enable auto-reload for development
        ]

        print('creating process ..')
        self.process_run_uvicorn = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        async def read_stream(stream, name):
            while True:
                line = await stream.readline()
                if not line:
                    break
                print(f"{name}: {line.strip()}")
                self.update_label_text(f"{name}: {line.strip()}\n")
        
        print('creating stdout task ..')
        # Start tasks to read stdout and stderr concurrently
        stdout_task = asyncio.create_task(read_stream(self.process_run_uvicorn.stdout, 'stdout'))
        stderr_task = asyncio.create_task(read_stream(self.process_run_uvicorn.stderr, 'stderr'))



        # Wait for the process to complete
        print(f'does this loop forever?')
        await self.process_run_uvicorn.wait()
        print(f'does this loop forever2?')
        

        # Wait for the reading tasks to complete
        await asyncio.gather(stdout_task, stderr_task)
        print(f'does this loop forever3?')


    def run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()


    # def process_queue(self):
    #     try:
    #         print(f'process queue for what')
    #         # while True:
    #         #     message = self.loop.call_soon_threadsafe(self.queue.get_nowait)
    #         #     if message[0] == "update_label":
    #         #         self.update_label_text(message[1])
    #     except queue.Empty:
    #         self.root.after(100, self.process_queue)



# if __name__ == "__main__":
#     root = tk.Tk()
#     app = UVicornApp(root)
#     root.mainloop()



async def main():


    
    # Continue with other asynchronous tasks if needed
    
    root = tk.Tk()
    app = UVicornApp(root)


    # Start the event loop in a separate thread
    threading.Thread(target=app.run_event_loop, daemon=True).start()
    # root.after(100, app.process_queue)  # Check the queue periodically
  

    root.mainloop()

if __name__ == "__main__":
    asyncio.run(main())

import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import threading
import queue
import select




class PingThread(threading.Thread):
    def __init__(self, command, output_text):
        super().__init__()
        self.command = command
        self.output_text = output_text
        self.process = None
        self.stop_event = threading.Event()

    def run(self):
        try:
            # self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, text=True)
            self.process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)


            while not self.stop_event.is_set():
                    line = self.process.stdout.readline()
                    if not line:
                        break
                    print(line)
                    self.output_text.config(state=tk.NORMAL)
                    self.output_text.insert(tk.END, line)
                    self.output_text.config(state=tk.DISABLED)
                    self.output_text.yview(tk.END)
                    # self.stop_event.wait(.01)
            
            # for line in iter(self.process.stdout.readline, ''):
            #     if self.stop_event.is_set():
            #         break
            #     self.output_text.config(state=tk.NORMAL)
            #     self.output_text.insert(tk.END, line)
            #     self.output_text.config(state=tk.DISABLED)
            #     self.output_text.yview(tk.END)

            print(f'run loop is_set()')

        except Exception as e:
            print("Error:", e)

    def stop(self):
        print(f'self stop_event setting stop ..')
        self.stop_event.set()
        print(f'self stop_event setting stop ok ..')

        # Terminate the subprocess
        print(f'{self.process.poll() =}, {self.process =}')
        if self.process and self.process.poll() is None:
            print(f'terminating self.processs. ')
            self.process.terminate()
            print(f'terminated self.processs. ')
            self.process.wait()
            print(f'wait self.processs. ')




if __name__ == "__main__":
    print(f'main start ..')

    started=False
    result=0

    def on_tab_change(event):
        selected_tab = notebook.index(notebook.select())
        print("Selected Tab:", selected_tab)

    def start_runesolver():
        global started
        global result
        cmd_command = "uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001"  # Example: "dir" to list files in the current directory
        thread = threading.Thread(target=execute_command, args=(cmd_command,))
        if started:
            started=False
            # print(f'Runesolver already started ..')
            # button.config(text='Start Runesolver', bg='lime')
            result.terminate()
            result.wait()
            print(f'result is teriminated. ')
            print(result.stdout)
            if thread.is_alive():
                print(f'thread is alive. ')
                thread.terminate()
                print(f'thread is teriminated. ')
        else:
            started=True
            # button.config(text='Stop Runesolver', bg='tomato')
        #     cmd_command = "uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001"  # Example: "dir" to list files in the current directory
        #     try:
        #         result = subprocess.run(cmd_command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
        #         print("Command Output:")
        #         print(result.stdout)
        #     except subprocess.CalledProcessError as e:
        #         print("Error:", e)
        
            # Get the command from the entry widget
            # cmd_command = command_entry.get()        

            # Disable the button while the command is running
            # button.config(state=tk.DISABLED)

            # Run the command in a separate thread
            thread.start()
        
    def execute_command(cmd_command):
        global result
        try:
            # Run the command
            result = subprocess.run(cmd_command, shell=True, check=True, stdout=subprocess.PIPE, text=True)

            print("Command Output:")
            print(result.stdout)
            # Display the command output in a text widget
            output_text.config(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result.stdout)
            output_text.config(state=tk.DISABLED)

        except subprocess.CalledProcessError as e:
            print("Error:", e)

        finally:
            # Enable the button after the command is complete
            # button.config(state=tk.NORMAL)
            pass

    def start_ping_thread():
        global ping_thread
        # ping_thread = PingThread("ping google.com -t", output_text)
        ping_thread = PingThread("uvicorn pytorch_solver:app --host 192.168.0.130 --port 8001", output_text)
        ping_thread.start()
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

    def stop_ping_thread():
        global ping_thread
        if ping_thread:
            ping_thread.stop()
            print(f'ping_thread stopped. ')
            ping_thread.join()
            print(f'ping_thread joined. ')
        start_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        
    # Create the main window
    root = tk.Tk()
    root.title("Bumblebeee")

    # Create a Notebook widget
    notebook = ttk.Notebook(root)

    # Create tabs (frames) to be added to the Notebook
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    # Add tabs to the Notebook
    notebook.add(tab1, text="Tab 1")
    notebook.add(tab2, text="Tab 2")
    notebook.add(tab3, text="Tab 3")

    # Bind the tab change event
    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    # Pack the Notebook widget
    notebook.pack(expand=1, fill="both")

    # Add content to each tab
    label1 = tk.Label(tab1, text="Runesolver")
    label1.pack(padx=10, pady=10)

    label2 = tk.Label(tab2, text="Tab 2 Function .. work in progress ..")
    label2.pack(padx=10, pady=10)

    label3 = tk.Label(tab3, text="Tab 3 Function .. work in progress ..")
    label3.pack(padx=10, pady=10)
    
    # button = tk.Button(tab1, text="Start Runesolver", command=start_runesolver, width=20, height=5, bg='lime', font=('Helvetica', 16))
    # button.pack(pady=(10,20))

    start_button = tk.Button(tab1, text="Start Runesolver", command=start_ping_thread, width=20, height=5, bg='lime', font=('Helvetica', 16))
    start_button.pack(pady=(10,20))
    stop_button = tk.Button(tab1, text="Stop Runesolver", command=stop_ping_thread, width=20, height=5, bg='tomato', font=('Helvetica', 16))
    stop_button.pack(pady=(10,20))
    
    output_text = tk.Text(tab1, height=10, width=60, state=tk.DISABLED)
    output_text.pack(pady=10)
    
    # Start the Tkinter event loop
    root.mainloop()


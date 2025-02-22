import tkinter as tk
from tkinter import ttk
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class ResponseViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Claude Response Viewer")
        self.geometry("800x600")

        # Create main container
        self.main_container = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Create sidebar frame
        self.sidebar = ttk.Frame(self.main_container)
        self.main_container.add(self.sidebar)

        # Create response list
        self.response_list = tk.Listbox(self.sidebar, width=30)
        self.response_list.pack(fill=tk.BOTH, expand=True)
        self.response_list.bind('<<ListboxSelect>>', self.on_select)

        # Create main content frame
        self.content_frame = ttk.Frame(self.main_container)
        self.main_container.add(self.content_frame)

        # Create text widget for displaying responses
        self.text_widget = tk.Text(self.content_frame, wrap=tk.WORD, padx=10, pady=10)
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        # Initialize file handler and observer
        self.setup_file_watcher()
        
        # Load existing responses
        self.load_responses()

    def setup_file_watcher(self):
        class ResponseHandler(FileSystemEventHandler):
            def __init__(self, callback):
                self.callback = callback

            def on_created(self, event):
                if not event.is_directory and event.src_path.endswith('.txt'):
                    self.callback()

        self.observer = Observer()
        self.observer.schedule(
            ResponseHandler(self.load_responses),
            path="response",
            recursive=False
        )
        self.observer.start()

    def load_responses(self):
        # Clear current list
        self.response_list.delete(0, tk.END)
        
        # Get all response files
        try:
            files = [f for f in os.listdir("response") if f.endswith('.txt')]
            files.sort()  # Sort files alphabetically
            
            # Add to listbox
            for file in files:
                self.response_list.insert(tk.END, file)
                
            # Select the last item if it exists
            if files:
                self.response_list.select_set(tk.END)
                self.response_list.event_generate('<<ListboxSelect>>')
        except Exception as e:
            print(f"Error loading responses: {e}")

    def on_select(self, event):
        # Get selected filename
        selection = self.response_list.curselection()
        if not selection:
            return
            
        filename = self.response_list.get(selection[0])
        
        # Clear current text
        self.text_widget.delete(1.0, tk.END)
        
        # Load and display selected response
        try:
            with open(os.path.join("response", filename), 'r', encoding='utf-8') as f:
                content = f.read()
                self.text_widget.insert(tk.END, content)
        except Exception as e:
            self.text_widget.insert(tk.END, f"Error loading response: {e}")

    def on_closing(self):
        self.observer.stop()
        self.observer.join()
        self.destroy()

def main():
    app = ResponseViewer()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()

import customtkinter as ctk
import threading
import time
import queue

# Set a consistent theme for the app
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, command_queue, status_queue, on_close):
        super().__init__()

        self.command_queue = command_queue
        self.status_queue = status_queue
        self.on_close = on_close
        self.speaking_words = 0

        # --- Configure window ---
        self.title("Personal Assistant")
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Create main frame for chat history ---
        self.main_frame = ctk.CTkScrollableFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Add a text box to show conversation history
        self.chat_history_textbox = ctk.CTkTextbox(self.main_frame, width=500, height=450, state="disabled")
        self.chat_history_textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # --- Create input frame ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.user_input = ctk.CTkEntry(self.input_frame, placeholder_text="Type your command...")
        self.user_input.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
        self.user_input.bind("<Return>", self.send_command)

        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_command)
        self.send_button.grid(row=0, column=1, padx=(0, 10), pady=10)

        # --- Create status bar frame ---
        self.status_frame = ctk.CTkFrame(self)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        self.status_frame.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready.")
        self.status_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Update the UI from a separate thread
        self.update_ui_thread = threading.Thread(target=self.check_queue_and_update_ui)
        self.update_ui_thread.daemon = True
        self.update_ui_thread.start()

    def send_command(self, event=None):
        command = self.user_input.get()
        if command:
            self.add_message_to_history(f"You: {command}")
            self.command_queue.put(command)
            self.user_input.delete(0, "end")
            self.status_label.configure(text="Processing command...")

    def add_message_to_history(self, message):
        self.chat_history_textbox.configure(state="normal")
        self.chat_history_textbox.insert("end", f"{message}\n\n")
        self.chat_history_textbox.configure(state="disabled")
        self.chat_history_textbox.see("end")

    def check_queue_and_update_ui(self):
        while True:
            try:
                # Check for updates from the main program
                words_speaking = self.status_queue.get_nowait()
                if words_speaking > 0:
                    self.status_label.configure(text=f"Speaking... ({words_speaking} words)")
                elif words_speaking == 0:
                    self.status_label.configure(text="Ready.")

                # Check for new messages to display
                while not self.command_queue.empty():
                    message = self.command_queue.get_nowait()
                    self.add_message_to_history(f"Assistant: {message}")
            except queue.Empty:
                pass
            time.sleep(0.1) # Prevents the thread from using 100% CPU

    def on_closing(self):
        self.on_close()
        self.destroy()

def run_interface(command_queue, status_queue, on_close):
    app = App(command_queue, status_queue, on_close)
    app.mainloop()
# --- client.py ---
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox, ttk
from datetime import datetime
import re

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Colors
        self.bg_color = "#2C3E50"
        self.text_color = "#ECF0F1"
        self.input_bg = "#34495E"
        self.accent_color = "#3498DB"
        self.system_msg_color = "#95A5A6"
        self.user_msg_color = "#E74C3C"
        self.others_msg_color = "#2ECC71"
        
        # Setup GUI
        self.root = tk.Tk()
        self.root.title("ChatWave")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.configure(bg=self.bg_color)
        
        # Load custom font
        self.root.option_add("*Font", "Helvetica 10")
        
        # Create custom styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", 
                             background=self.accent_color, 
                             foreground=self.text_color, 
                             padding=6, 
                             relief="flat")
        self.style.map("TButton", 
                       background=[("active", "#2980B9"), ("pressed", "#1F618D")])
        
        # Create main container
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # App header
        self.header_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.logo_label = tk.Label(self.header_frame, text="ChatWave", 
                                  font=("Helvetica", 18, "bold"), 
                                  bg=self.bg_color, fg=self.accent_color)
        self.logo_label.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(self.header_frame, text="Disconnected", 
                                    bg=self.bg_color, fg=self.system_msg_color,
                                    font=("Helvetica", 10))
        self.status_label.pack(side=tk.RIGHT, padx=5)
        
        # Chat area
        self.chat_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.chat_area = scrolledtext.ScrolledText(self.chat_frame, 
                                                  wrap=tk.WORD, 
                                                  bg=self.input_bg, 
                                                  fg=self.text_color, 
                                                  insertbackground=self.text_color,
                                                  font=("Helvetica", 11),
                                                  padx=10, pady=10)
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Configure tags for different message types
        self.chat_area.tag_configure("system", foreground=self.system_msg_color, font=("Helvetica", 10, "italic"))
        self.chat_area.tag_configure("user", foreground=self.user_msg_color, font=("Helvetica", 11, "bold"))
        self.chat_area.tag_configure("others", foreground=self.others_msg_color, font=("Helvetica", 11))
        self.chat_area.tag_configure("timestamp", foreground="#7F8C8D", font=("Helvetica", 9))
        
        # Input area
        self.input_frame = tk.Frame(self.main_container, bg=self.bg_color)
        self.input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.message_input = tk.Entry(self.input_frame, 
                                     bg=self.input_bg, 
                                     fg=self.text_color, 
                                     insertbackground=self.text_color,
                                     relief=tk.FLAT,
                                     font=("Helvetica", 11))
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.message_input.bind("<Return>", self.send_message)
        
        self.send_button = ttk.Button(self.input_frame, 
                                     text="Send", 
                                     command=self.send_message,
                                     style="TButton")
        self.send_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Users online (sidebar)
        self.sidebar_frame = tk.Frame(self.root, bg=self.bg_color, width=200)
        
        # Online users
        self.online_users = []
        
        # Close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Connect to server
        self.nickname = None
        
    def start(self):
        self.get_nickname()
        
        try:
            self.client_socket.connect((self.host, self.port))
            self.status_label.config(text=f"Connected as {self.nickname}")
            
            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.root.mainloop()
            
        except Exception as e:
            self.update_chat(f"Error connecting to server: {e}", "system")
            self.status_label.config(text="Connection failed")
    
    def get_nickname(self):
        # Create a custom dialog for nickname entry
        dialog = tk.Toplevel(self.root)
        dialog.title("Welcome to ChatWave")
        dialog.geometry("400x200")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Center the dialog
        self.root.eval(f'tk::PlaceWindow {str(dialog)} center')
        
        # Logo
        logo_label = tk.Label(dialog, text="ChatWave", 
                             font=("Helvetica", 24, "bold"), 
                             bg=self.bg_color, fg=self.accent_color)
        logo_label.pack(pady=(20, 15))
        
        # Nickname frame
        nickname_frame = tk.Frame(dialog, bg=self.bg_color)
        nickname_frame.pack(fill=tk.X, padx=30, pady=10)
        
        nickname_label = tk.Label(nickname_frame, text="Enter your nickname:", 
                                 bg=self.bg_color, fg=self.text_color,
                                 font=("Helvetica", 11))
        nickname_label.pack(anchor=tk.W, pady=(0, 5))
        
        nickname_entry = tk.Entry(nickname_frame, 
                                 bg=self.input_bg, 
                                 fg=self.text_color, 
                                 insertbackground=self.text_color,
                                 relief=tk.FLAT,
                                 font=("Helvetica", 11))
        nickname_entry.pack(fill=tk.X, ipady=8)
        nickname_entry.focus_set()
        
        # Button frame
        button_frame = tk.Frame(dialog, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=30, pady=(5, 20))
        
        join_button = ttk.Button(button_frame, 
                                text="Join Chat", 
                                style="TButton",
                                command=lambda: self.set_nickname(nickname_entry.get(), dialog))
        join_button.pack(fill=tk.X)
        
        # Bind Enter key
        dialog.bind("<Return>", lambda event: self.set_nickname(nickname_entry.get(), dialog))
        
        # Wait for the dialog to close
        self.root.wait_window(dialog)
    
    def set_nickname(self, nickname, dialog):
        if nickname and nickname.strip():
            self.nickname = nickname.strip()
            dialog.destroy()
        else:
            messagebox.showerror("Error", "Nickname cannot be empty!", parent=dialog)
    
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                
                if message == "NICK":
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    # Check for system messages
                    if "has joined the chat" in message or "has left the chat" in message:
                        self.update_chat(message, "system")
                    else:
                        # Check if it's the user's own message
                        if message.startswith(f"{self.nickname}: "):
                            self.update_chat(message, "user")
                        else:
                            self.update_chat(message, "others")
            except Exception as e:
                self.update_chat(f"Error receiving message: {e}", "system")
                self.client_socket.close()
                break
    
    def send_message(self, event=None):
        message = self.message_input.get().strip()
        if message:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.message_input.delete(0, tk.END)
            except Exception as e:
                self.update_chat(f"Error sending message: {e}", "system")
    
    def update_chat(self, message, msg_type="others"):
        self.chat_area.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_area.insert(tk.END, f"[{timestamp}] ", "timestamp")
        
        # Add message with appropriate tag
        self.chat_area.insert(tk.END, f"{message}\n", msg_type)
        
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            try:
                self.client_socket.close()
            except:
                pass
            self.root.destroy()

if __name__ == "__main__":
    client = ChatClient()
    client.start()

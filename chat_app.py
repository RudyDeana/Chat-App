import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# chat_app.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import socket
import threading
import json
import random
import os

class ChatApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chat App")
        self.window.geometry("800x600")
        
        # Using more compatible colors
        self.colors = {
            'bg_dark': '#ffffff',  # Changed to white
            'bg_light': '#f5f5f5',  # Very light gray
            'accent': '#007acc',
            'text': '#000000',     # Black text
            'input_bg': '#ffffff',  # White input
            'input_fg': '#000000'   # Black input text
        }
        
        self.window.configure(bg=self.colors['bg_dark'])
        
        # Style configuration for ttk
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Chat.TScrollbar",
            background=self.colors['accent'],
            troughcolor='#e0e0e0',
            borderwidth=0,
            arrowcolor=self.colors['text'])
        style.layout("Chat.TScrollbar", [
            ('Scrollbar.trough', {'children':
                [('Scrollbar.thumb', {'expand': '1'})],
                'sticky': 'nswe'})
        ])
        
        # Connection configuration
        self.server = '101.56.214.224'  # or '127.0.0.1'
        self.port = 5555
        self.buffer_size = 4096
        
        self.setup_gui()

    def setup_gui(self):
        # Main frame
        main_frame = tk.Frame(self.window, bg=self.colors['bg_dark'], padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Centered Logo/Icon
        logo_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        logo_frame.pack(fill='x')
        
        tk.Label(
            logo_frame,
            text="💬",
            font=('Arial', 48),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(expand=True, pady=10)
        
        # Centered title
        title_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        title_frame.pack(fill='x')
        
        tk.Label(
            title_frame,
            text="Chat App",
            font=('Arial', 24, 'bold'),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(expand=True, pady=10)
        
        # Centered input frame
        input_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        input_frame.pack(fill='x', pady=20)
        
        label_frame = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        label_frame.pack(fill='x')
        
        tk.Label(
            label_frame,
            text="👤 Your Name:",
            font=('Arial', 12),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(expand=True)
        
        entry_frame = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        entry_frame.pack(fill='x', pady=5)
        
        self.username_entry = tk.Entry(
            entry_frame, 
            font=('Arial', 12), 
            width=30,
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg'],
            insertbackground=self.colors['input_fg'],
            justify='center'
        )
        self.username_entry.pack(expand=True)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        buttons_frame.pack(pady=20)
        
        tk.Button(
            buttons_frame,
            text="🔵 Create New Room",
            font=('Arial', 12),
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg'],
            command=self.create_room,
            padx=20,
            pady=10,
            cursor='hand2',
            relief='flat'
        ).pack(pady=10)
        
        separator = tk.Frame(buttons_frame, height=2, bg=self.colors['accent'])
        separator.pack(fill='x', pady=15)
        
        tk.Label(
            buttons_frame,
            text="🔑 Room Code:",
            font=('Arial', 12),
            bg=self.colors['bg_dark'],
            fg=self.colors['input_fg']
        ).pack(pady=5)
        
        self.room_code_entry = tk.Entry(
            buttons_frame,
            font=('Arial', 12),
            width=20,
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg']
        )
        self.room_code_entry.pack()
        
        tk.Button(
            buttons_frame,
            text="➡️ Join Room",
            font=('Arial', 12),
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg'],
            command=self.join_room,
            padx=20,
            pady=10,
            cursor='hand2',
            relief='flat'
        ).pack(pady=10)

    def show_chat_room(self, room_code):
        chat_window = tk.Toplevel(self.window)
        chat_window.title(f"Chat - Room {room_code}")
        chat_window.geometry("1000x600")
        chat_window.configure(bg=self.colors['bg_dark'])
        
        # Main frame
        chat_frame = tk.Frame(chat_window, bg=self.colors['bg_dark'], padx=20, pady=20)
        chat_frame.pack(expand=True, fill='both')
        
        # Header
        header = tk.Frame(chat_frame, bg=self.colors['bg_dark'])
        header.pack(fill='x', pady=(0,10))
        
        tk.Label(
            header,
            text=f"💬 Room #{room_code}",
            font=('Arial', 16, 'bold'),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(expand=True)
        
        # Main area
        main_area = tk.Frame(chat_frame, bg=self.colors['bg_light'])
        main_area.pack(expand=True, fill='both')
        
        # Users list
        users_frame = tk.Frame(main_area, bg=self.colors['bg_dark'], width=200)
        users_frame.pack(side='left', fill='y', padx=(0,10))
        users_frame.pack_propagate(False)
        
        tk.Label(
            users_frame,
            text="👥 Online Users",
            font=('Arial', 12, 'bold'),
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        self.users_list = tk.Text(
            users_frame,
            font=('Arial', 11),
            bg=self.colors['bg_dark'],
            fg=self.colors['text'],
            relief='flat',
            state='disabled',
            width=20
        )
        self.users_list.pack(expand=True, fill='both', padx=10)
        
        # Messages area with file preview
        messages_frame = tk.Frame(main_area, bg=self.colors['bg_light'])
        messages_frame.pack(side='right', expand=True, fill='both')
        
        # File preview area
        preview_frame = tk.Frame(messages_frame, bg=self.colors['bg_light'])
        preview_frame.pack(fill='x', padx=10, pady=5)
        
        preview_content = tk.Frame(preview_frame, bg=self.colors['bg_light'])
        preview_content.pack(expand=True)
        
        self.preview_label = tk.Label(
            preview_content,
            text="",
            font=('Arial', 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            wraplength=400
        )
        self.preview_label.pack(side='left', pady=5)
        
        self.preview_button = tk.Button(
            preview_content,
            text="⬇️",
            font=('Arial', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg'],
            command=self.download_preview_file,
            padx=10,
            cursor='hand2',
            relief='flat',
            state='disabled'
        )
        self.preview_button.pack(side='left', padx=5)
        
        # Messages area
        self.messages = tk.Text(
            messages_frame,
            font=('Arial', 11),
            bg=self.colors['bg_light'],
            fg=self.colors['text'],
            relief='flat',
            state='disabled',
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        scrollbar = ttk.Scrollbar(
            messages_frame, 
            orient='vertical', 
            command=self.messages.yview,
            style="Chat.TScrollbar"
        )
        self.messages.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.messages.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Centered input area
        input_frame = tk.Frame(chat_frame, bg=self.colors['bg_dark'], pady=10)
        input_frame.pack(fill='x')
        
        input_content = tk.Frame(input_frame, bg=self.colors['bg_dark'])
        input_content.pack(expand=True)
        
        self.message_entry = tk.Entry(
            input_content,
            font=('Arial', 12),
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg'],
            insertbackground=self.colors['input_fg'],
            width=50,
            justify='center'
        )
        self.message_entry.pack(side='left', padx=5)
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        file_button = tk.Button(
            input_content,
            text="📎",
            font=('Arial', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg'],
            command=self.send_file,
            padx=10,
            cursor='hand2',
            relief='flat'
        )
        file_button.pack(side='left', padx=5)
        
        send_button = tk.Button(
            input_content,
            text="➤",
            font=('Arial', 14),
            bg=self.colors['input_bg'],
            fg=self.colors['input_fg'],
            command=self.send_message,
            padx=10,
            cursor='hand2',
            relief='flat'
        )
        send_button.pack(side='left')

        self.active_room = {
            'window': chat_window,
            'messages': self.messages,
            'users_list': self.users_list,
            'preview_label': self.preview_label,
            'preview_button': self.preview_button
        }

    def create_room(self):
        username = self.username_entry.get().strip()
        if not username:
            messagebox.showerror("Error", "Please enter your name!")
            return
            
        room_code = str(random.randint(1000, 9999))
        self.connect_to_chat(username, room_code, True)

    def join_room(self):
        username = self.username_entry.get().strip()
        room_code = self.room_code_entry.get().strip()
        
        if not username or not room_code:
            messagebox.showerror("Error", "Please enter your name and room code!")
            return
            
        self.connect_to_chat(username, room_code, False)

    def connect_to_chat(self, username, room_code, is_host):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.server, self.port))
            
            # Send connection data
            self.client.send(json.dumps({
                'username': username,
                'room': room_code,
                'is_host': is_host
            }).encode())
            
            # Receive response
            response = json.loads(self.client.recv(1024).decode())
            if response['type'] == 'error':
                messagebox.showerror("Error", response['content'])
                self.client.close()
                return
                
            # Show chat
            self.show_chat_room(room_code)
            
            # Start receiving messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Unable to connect to server: {str(e)}")

    def send_message(self):
        message = self.message_entry.get().strip()
        if message:
            try:
                self.client.send(json.dumps({
                    'type': 'message',
                    'content': message
                }).encode())
                self.message_entry.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Unable to send message")

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                file_size = os.path.getsize(file_path)
                file_name = os.path.basename(file_path)
                
                # Check maximum size (e.g. 100MB)
                max_size = 100 * 1024 * 1024  # 100MB in bytes
                if file_size > max_size:
                    messagebox.showerror("Error", "File is too large (max 100MB)")
                    return
                
                # Show progress
                progress_window = tk.Toplevel(self.window)
                progress_window.title("Sending file...")
                progress_window.geometry("300x150")
                progress_window.transient(self.window)
                progress_window.grab_set()
                
                tk.Label(
                    progress_window,
                    text=f"Sending {file_name}...",
                    pady=10
                ).pack()
                
                progress_var = tk.DoubleVar()
                progress_bar = ttk.Progressbar(
                    progress_window,
                    variable=progress_var,
                    maximum=100
                )
                progress_bar.pack(pady=10, padx=20, fill='x')
                
                # Set longer timeout for file sending
                self.client.settimeout(30)  # 30 seconds timeout
                
                try:
                    # Send file information
                    self.client.send(json.dumps({
                        'type': 'file_info',
                        'file_name': file_name,
                        'file_size': file_size
                    }).encode())
                    
                    # Send file
                    sent_bytes = 0
                    with open(file_path, 'rb') as f:
                        while sent_bytes < file_size:
                            chunk = f.read(min(self.buffer_size, file_size - sent_bytes))
                            if not chunk:
                                break
                            
                            # Send chunk with error handling
                            total_sent = 0
                            while total_sent < len(chunk):
                                try:
                                    bytes_sent = self.client.send(chunk[total_sent:])
                                    if bytes_sent == 0:
                                        raise ConnectionError("Connection lost")
                                    total_sent += bytes_sent
                                except socket.timeout:
                                    continue
                            
                            sent_bytes += total_sent
                            
                            # Update progress
                            progress = (sent_bytes / file_size) * 100
                            progress_var.set(progress)
                            progress_window.update()
                    
                    messagebox.showinfo("Success", "File sent successfully!")
                    
                finally:
                    # Restore normal timeout
                    self.client.settimeout(None)
                    progress_window.destroy()
                
            except ConnectionError:
                messagebox.showerror("Error", "Connection lost while sending file")
            except socket.timeout:
                messagebox.showerror("Error", "Timeout while sending file")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to send file: {str(e)}")

    def show_file_preview(self, file_name, file_data):
        # Show file preview
        self.current_preview_file = {'name': file_name, 'data': file_data}
        self.preview_label.config(text=f"📄 {file_name}")
        self.preview_button.config(state='normal')

    def download_preview_file(self):
        if hasattr(self, 'current_preview_file'):
            file_name = self.current_preview_file['name']
            file_data = self.current_preview_file['data']
            
            save_path = filedialog.asksaveasfilename(
                defaultextension=os.path.splitext(file_name)[1],
                initialfile=file_name
            )
            
            if save_path:
                try:
                    with open(save_path, 'wb') as f:
                        f.write(file_data)
                    messagebox.showinfo("Success", "File downloaded successfully!")
                    self.preview_label.config(text="")
                    self.preview_button.config(state='disabled')
                except Exception as e:
                    messagebox.showerror("Error", f"Error while saving: {str(e)}")

    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(self.buffer_size).decode()
                msg = json.loads(data)
                
                if msg['type'] == 'users':
                    self.users_list.config(state='normal')
                    self.users_list.delete('1.0', tk.END)
                    for user in msg['users']:
                        self.users_list.insert(tk.END, f"• {user}\n")
                    self.users_list.config(state='disabled')
                    
                elif msg['type'] == 'message':
                    self.messages.config(state='normal')
                    self.messages.insert(tk.END, f"{msg['sender']}: {msg['content']}\n")
                    self.messages.see(tk.END)
                    self.messages.config(state='disabled')
                    
                elif msg['type'] == 'file':
                    sender = msg['sender']
                    file_name = msg['file_name']
                    file_size = msg['file_size']
                    
                    # Show download progress
                    progress_window = tk.Toplevel(self.window)
                    progress_window.title("Downloading file...")
                    progress_window.geometry("300x150")
                    
                    tk.Label(
                        progress_window,
                        text=f"Downloading {file_name}...",
                        pady=10
                    ).pack()
                    
                    progress_var = tk.DoubleVar()
                    progress_bar = ttk.Progressbar(
                        progress_window,
                        variable=progress_var,
                        maximum=100
                    )
                    progress_bar.pack(pady=10, padx=20, fill='x')
                    
                    try:
                        received_data = b''
                        while len(received_data) < file_size:
                            chunk = self.client.recv(min(self.buffer_size, file_size - len(received_data)))
                            if not chunk:
                                raise ConnectionError("Connection interrupted")
                            received_data += chunk
                            
                            progress = (len(received_data) / file_size) * 100
                            progress_var.set(progress)
                            progress_window.update()
                        
                        # Show preview instead of saving to list
                        self.show_file_preview(file_name, received_data)
                        
                        self.messages.config(state='normal')
                        self.messages.insert(tk.END, f"📎 {sender} shared file: {file_name}\n")
                        self.messages.see(tk.END)
                        self.messages.config(state='disabled')
                        
                    except Exception as e:
                        messagebox.showerror("Error", f"Error during download: {str(e)}")
                    finally:
                        progress_window.destroy()
                    
            except ConnectionError:
                messagebox.showerror("Error", "Lost connection to server")
                break
            except Exception as e:
                print(f"Error in receiving: {str(e)}")
                break

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ChatApp()
    app.run()

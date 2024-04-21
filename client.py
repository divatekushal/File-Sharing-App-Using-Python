import tkinter as tk
from tkinter import filedialog, messagebox
import os
import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Define global variables
host = '127.0.0.1'
port = 8080
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
key = get_random_bytes(16)  # AES key

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username == "1" and password == "1":
        frame_login.pack_forget()
        frame.pack(padx=20,pady=20) 
    # Authentication logic can be added here

def upload():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as f:
            data = f.read()
            sock.sendall(b"upload_file")  # Sending a message to indicate file upload
            sock.sendall(file_name.encode())
            sock.sendall(b":::-:::")  # Sending the filename separator
            sock.sendall(data)  # Sending the file content
        print("File uploaded successfully.")
        # Notify the user of successful upload
        messagebox.showinfo("Upload", "File uploaded successfully.")

def exit():
    # Ask for confirmation before exiting
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        sock.sendall(b"exit")
        root.destroy()

def download():
    # Send download request to server
    sock.sendall(b"download_file")

    # Receive file data from server
    file_data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        file_data += chunk

    if file_data.startswith(b"File not found"):
        # Notify the user if the file is not found on the server
        messagebox.showerror("Download Error", "File not found on the server.")
    else:
        # Ask user to choose save location and filename
        file_name = filedialog.asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt", filetypes=[("All Files", "*.*")])
        if file_name:
            try:
                with open(file_name, "wb") as f:
                    f.write(file_data)
                print("File downloaded successfully.")
                # Notify the user of successful download
                messagebox.showinfo("Download", "File downloaded successfully.")
            except Exception as e:
                # Notify the user if an error occurs during file saving
                messagebox.showerror("Download Error", f"An error occurred: {str(e)}")


def file_browsing():
    # Send a request to the server to get the list of files
    sock.sendall(b"list_files")

    # Receive the list of files from the server
    files_data = sock.recv(1024).decode()
    file_list = files_data.split(":::")  # Assuming ":::" is not part of any filename

    # Create a new window to display the file list
    browse_window = tk.Toplevel(root)
    browse_window.title("File Browser")

    # Create a listbox to display the files
    file_listbox = tk.Listbox(browse_window, width=50)
    file_listbox.pack(padx=10, pady=10)

    # Insert each file into the listbox
    for file_name in file_list:
        file_listbox.insert(tk.END, file_name)

    # Function to handle downloading the selected file
    def download_selected():
        selected_index = file_listbox.curselection()
        if selected_index:
            selected_file = file_listbox.get(selected_index)
            sock.sendall(b"download_file")
            sock.sendall(selected_file.encode())
            # Receive file data from server and save it locally (implement this part)

    # Button to download the selected file
    download_button = tk.Button(browse_window, text="Download Selected", command=download_selected)
    download_button.pack(pady=5)

    return        

root = tk.Tk()
root.title("File Sharing App")

frame_login = tk.Frame(root)
frame_login.pack(padx=20, pady=20)

username_label = tk.Label(frame_login, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
username_entry = tk.Entry(frame_login)
username_entry.grid(row=0, column=1, padx=5, pady=5)

password_label = tk.Label(frame_login, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
password_entry = tk.Entry(frame_login)
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tk.Button(frame_login, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=3)

error_label = tk.Label(frame_login, text="", fg="red")
error_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Sharing window
frame = tk.Frame(root)

upload_button = tk.Button(frame, text="Upload", command=upload)
upload_button.pack(fill=tk.X, padx=10, pady=5)

download_button = tk.Button(frame, text="Download", command=download)
download_button.pack(fill=tk.X, padx=10, pady=5)

auth_button = tk.Button(frame, text="File Browsing", command=file_browsing)
auth_button.pack(fill=tk.X, padx=10, pady=5)

exit_button = tk.Button(frame, text="Exit", command=exit)
exit_button.pack(fill=tk.X, padx=10, pady=5)

root.mainloop()

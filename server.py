import socket
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Define global variables
directory = "server"
if not os.path.exists(directory):
    os.makedirs(directory)
key = get_random_bytes(16)  # AES key

def receive_file(conn, client_addr):
    # Receive message indicating file upload, file browsing request, or file download request
    msg = conn.recv(1024).decode()
    
    if msg == "upload_file":
        # Receive filename from client
        filename = conn.recv(1024).decode()
        filename_corrected = filename.split(":::-:::")
        data = "".join(filename_corrected[1:])
        # Receive file data and save with sanitized filename
        with open(os.path.join(directory, filename_corrected[0]), 'wb') as fo:  # Open in binary mode for writing
            fo.write(data.encode())
        print(f"File '{filename_corrected[0]}' received successfully from client {client_addr}.")
        # Notify the client of successful upload
        conn.sendall(b"File uploaded successfully.")
    elif msg == "list_files":
        # Send the list of files in the server directory to the client
        file_list = os.listdir(directory)
        files_data = ":::".join(file_list)
        conn.sendall(files_data.encode())
        print("File list sent to the client.")
    elif msg == "download_file":
        # Receive the requested filename from the client
        requested_file = conn.recv(1024).decode()
        file_path = os.path.join(directory, requested_file)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                file_data = file.read()
                conn.sendall(file_data)  # Send the file content to the client
                print(f"File '{requested_file}' sent to client {client_addr}.")
        else:
            conn.sendall(b"File not found")  # Send a message if the file is not found
            print(f"File '{requested_file}' not found.")

    elif msg == "download_file":
        # Receive the requested filename from the client
        requested_file = conn.recv(1024).decode()
        file_path = os.path.join(directory, requested_file)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                file_data = file.read()
                conn.sendall(file_data)  # Send the file content to the client
                print(f"File '{requested_file}' sent to client {client_addr}.")
        else:
            conn.sendall(b"File not found")  # Send a message if the file is not found
            print(f"File '{requested_file}' not found.")

    else:
        print(f"Unexpected message received from client {client_addr}: {msg}")

def main():
    host = '127.0.0.1'
    port = 8080

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen()  # Limiting to one client

    print('Server is listening for clients...')
    conn, addr = sock.accept()
    print('Connected with client', addr)
    
    while True:
        # Handle the connection
        receive_file(conn, addr)

        # Check if the client sent an exit command
        exit_command = conn.recv(1024).decode()
        if exit_command == "exit":
            print('Exit command received. Closing connection with client', addr)
            conn.close()
            break  # Exit the loop and stop the server

    sock.close()

if __name__ == '__main__':
    main()

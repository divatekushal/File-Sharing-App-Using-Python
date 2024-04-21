# File Sharing App Using Python

File Sharing App is a Python application with a graphical user interface (GUI) that allows users to upload, download, and manage files securely.

## Features

- **Upload:** Upload files to the server. (Implemented using tkinter)
- **Download:** Download files from the server. (Implemented using tkinter)
- **File Browsing:** View the list of files available on the server. (Implemented using tkinter)
- **Authentication:** Authenticate users with a username and password. (Implemented using tkinter)
- **Encryption:** Encrypt file data during transmission for security. (Implemented using Crypto)
- **File Management:** Delete files from the server. (Implemented using tkinter)

## Usage

1. **Installation:**
   - Clone the repository to your local machine.

2. **Dependencies:**
   - Ensure you have Python installed, along with the required libraries .

3. **Running the Server:**
   - Open a terminal window.
   - Navigate to the project directory.
   - Run the following command to start the server:
     ```
     python server.py
     ```
   - The server will start listening on a specified IP address and port (default is 127.0.0.1:8080).

4. **Running the Client:**
   - Open another terminal window.
   - Navigate to the project directory.
   - Run the following command to start the client application:
     ```
     python client.py
     ```
   - The client will attempt to connect to the server's IP address and port.

5. **Login:**
   - Enter your username and password to log in to the application.

6. **Uploading:**
   - Click on the "Upload" button to select a file from your local machine and upload it to the server.

7. **Downloading:**
   - Click on the "Download" button to download a file from the server.

8. **Browsing:**
   - Click on the "File Browsing" button to view the list of files available on the server.

9. **Exiting:**
   - Click on the "Exit" button to exit the application.

## IP Address and Port Usage

- The IP address (default: 127.0.0.1) and port (default: 8080) are used for communication between the client and server.
- The server listens for incoming connections on the specified IP address and port.
- The client attempts to connect to the server using the specified IP address and port.

## Output
![Output Screenshot](output_screenshot.png)

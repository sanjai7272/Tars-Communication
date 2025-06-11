import socket

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define the IP address and port for the server
    host = '192.168.1.2'  # IP address of Laptop 1
    port = 12345          # Port to bind to

    # Bind the socket to the address and port
    server_socket.bind((host, port))

    # Start listening for incoming connections (queue up to 5 connections)
    server_socket.listen(5)
    
    print(f"Server listening on {host}:{port}")

    # Accept a connection
    client_socket, addr = server_socket.accept()
    print(f"Got connection from {addr}")

    # Receive data from the client (1024 bytes max)
    data = client_socket.recv(1024).decode()
    print(f"Received from client: {data}")

    # Send a response to the client
    client_socket.send("Hello from the server!".encode())

    # Close the connection
    client_socket.close()

if __name__ == "_main_":
    start_server()
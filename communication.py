import socket
import re

PORT = 65432
BYTE_SIZE = 4096
TIMEOUT = 30
ALL_IP = ""
END_MESSAGE = "#<<END>>#"


def validate_ip(ip):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'

    # use regex to validate ip
    if ip is "localhost":
        return True
    return re.match(pattern, ip) is not None

def clean_input(ip):
    return ip.replace(" ", "").strip()

def send_message():
    message = input("Enter a message (max 4096 characters): ")[0:4096]

    ip = input("Enter the recipient's IP address: ")
    # clean whitespace
    ip = clean_input(ip)

    while not validate_ip(ip):
        ip = input("Invalid IP address. Please enter a valid IP address: ")
        ip = clean_input(ip)

    connection_socket = None
    try:
        # Create the socket
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Establish the timeout of 30-seconds
        connection_socket.settimeout(TIMEOUT)

        # Connect to server
        connection_socket.connect((ip, PORT))

        # Send data
        print("Sending message...")
        connection_socket.sendall(message.encode('utf-8'))
        received = connection_socket.recv(BYTE_SIZE)

        if received.decode('utf-8') == END_MESSAGE:
            print("Message sent successfully!")
        else:
            print("Message sending error. Message not sent.")
    except socket.timeout:
        print("Timeout: Connection to the recipient timed out.")
    except (socket.error, Exception) as e:
        print(f"Error: {e}")
    finally:
        if connection_socket:
            connection_socket.close()


def receive_message():
    # Creating the server socket
    connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    connection_socket.bind((ALL_IP, PORT))

    # Let user know that the server is going to listen on the port
    print("Waiting for message on port " + str(PORT) + "...")

    # Listen for incoming connections
    connection_socket.listen()

    # Accepting a connection for the user
    connect_socket, address = connection_socket.accept()
    print(f"Connected by {address}")

    # Receive the message and print it, b"" because we need to read bytes in
    message = b""
    try:
        exit_switch = False
        while not exit_switch:
            data = connect_socket.recv(BYTE_SIZE)
            if not data:
                exit_switch = True
            else:
                message += data

        # Print the message ensuring we convert back to text from bytes
        print("Message:")
        print(message.decode('utf-8'))
        print("End of message.")

        # Send back acknowledgement
        connect_socket.sendall(b"#<<END>>#")
    except socket.error as e:
        print(f"Error: {e}")
    finally:
        # Close the socket
        connect_socket.close()


def exit_program():
    print("\nGoodbye!")
    exit(0)


def menu():
    while True:
        print("=== The Python Communicator ===")
        print("1) Send message")
        print("2) Receive message")
        print("0) Exit")

        option = input("Enter option: ")

        if option == "1":
            send_message()
        elif option == "2":
            receive_message()
        elif option == "0":
            exit_program()
        else:
            print("Error, invalid input")

    pass


def main():
    menu()
    pass


if __name__ == "__main__":
    main()

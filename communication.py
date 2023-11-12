import socket
import re

# Constants
PORT = 65432
BYTE_SIZE = 4096
MAX_IPV4_LENGTH = 15
TIMEOUT = 30
ALL_IP = ""
END_MESSAGE = b"#<<END>>#"


def validate_ip(ip):
    pattern = (r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]['
               r'0-9]?)$')

    if ip.lower() == "localhost":
        return True
    return re.match(pattern, ip) is not None


def clean_input(ip):
    return ip.replace(" ", "").strip()


def get_user_input(prompt, max_length):
    user_input = input(prompt)[:max_length]
    return user_input


def send_message():
    message = get_user_input("Enter a message (max 4096 characters): ", BYTE_SIZE)

    ip = clean_input(get_user_input("Enter the recipient's IP address: ", MAX_IPV4_LENGTH))

    while not validate_ip(ip):
        ip = clean_input(get_user_input("Invalid IP address. Please enter a valid IP "
                                        "address : ", MAX_IPV4_LENGTH))

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
        connection_socket.settimeout(None)
        connection_socket.sendall(message.encode('utf-8'))
        received = connection_socket.recv(BYTE_SIZE)

        if received == END_MESSAGE:
            print("Message sent successfully!")
        else:
            print("Message sending error. Message not sent.")
    except socket.timeout:
        print("Timeout: Connection to the recipient timed out.")
    except socket.error as e:
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

    with connect_socket:
        print(f"Connected by {address}")
        exit_switch = False
        while not exit_switch:
            received = connect_socket.recv(BYTE_SIZE)

            if not received:
                exit_switch = True
            else:
                print(f"Message received: {received.decode('utf-8')}")
            connect_socket.sendall(END_MESSAGE)


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


def main():
    menu()


if __name__ == "__main__":
    main()

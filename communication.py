"""
File: communication.py
Author: Kaushal Patel
Author: Daniel Aoulou
Date: 11/12/2023
Description: This Python script implements a simple client-server communication system using
sockets. The program allows users to send and receive messages over a network using IPv4
addresses. The user can choose to send a message to a specified IP address always using the
default port or receive messages on the default port. The communication protocol involves
establishing a connection, sending messages, and acknowledging successful message reception. The
program includes functions for input validation, cleaning user input, and
displaying a user-friendly menu for interaction.
"""


import socket   # Socket library
import re   # Regular expression library

# Constants
PORT = 65432    # The port to use for the socket
BYTE_SIZE = 4096    # The maximum size of the message in bytes
MAX_IPV4_LENGTH = 15    # The maximum length of an IPv4 address
TIMEOUT = 30    # The timeout in seconds
ALL_IP = ""   # The IP address to listen on all interfaces
END_MESSAGE = b"#<<END>>#"  # The end message to send to the client


def validate_ip(ip: str) -> bool:
    """
    Function that validates an IP address using a regular expression
    :param ip: The IP address to validate
    :return: True if the IP address is valid, False otherwise
    """

    # Regular expression pattern for an IPv4 address
    pattern = (r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9]['
               r'0-9]?)$')

    # If the IP address is localhost, then it is valid
    if ip.lower() == "localhost":
        return True

    # Otherwise, check the IP address against the regular expression pattern
    return re.match(pattern, ip) is not None


def clean_input(ip: str) -> str:
    """
    Function that cleans the user input
    :param ip: The user input
    :return: The cleaned user input
    """

    # Remove all spaces and strip the input
    return ip.replace(" ", "").strip()


def get_user_input(prompt: str, max_length: int) -> str:
    """
    Function that gets user input
    :param prompt: The prompt to display to the user
    :param max_length: The maximum length of the user input
    :return: The user input as a string
    """

    # Get the user input and limit it to the maximum length
    user_input = input(prompt)[:max_length]
    return user_input


def send_message() -> None:
    """
    Function that sends a message to a server
    :return: None
    """

    # Get the message from the user
    message = get_user_input("Enter a message (max 4096 characters): ", BYTE_SIZE)

    # Get the IP address from the user
    ip = clean_input(get_user_input("Enter the recipient's IP address: ", MAX_IPV4_LENGTH))

    # Validate the IP address. If it is not valid, then ask the user to enter a valid IP address
    while not validate_ip(ip):
        ip = clean_input(get_user_input("Invalid IP address. Please enter a valid IP "
                                        "address : ", MAX_IPV4_LENGTH))

    # Declare the connection socket
    connection_socket = None
    try:
        # Create the socket
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Establish the timeout of 30-seconds
        connection_socket.settimeout(TIMEOUT)

        # Connect to server
        connection_socket.connect((ip, PORT))

        try:
            # Let the user know that the message is being sent to the server
            print("Sending message...")

            # Set the timeout to None so that the socket will block until the message is sent
            connection_socket.settimeout(None)

            # Send the message to the server and encode it to utf-8
            connection_socket.sendall(message.encode('utf-8'))

            # Receive data from the server
            received = connection_socket.recv(BYTE_SIZE)

            # If the message received is the end message, then the message was sent successfully
            if received == END_MESSAGE:
                print("Message sent successfully!")
            # Otherwise, the message was not sent successfully
            else:
                print("Message sending error. Message not sent.")
        except socket.timeout:
            # If the message times out, then the message was not sent successfully
            print("Timeout: Connection to the recipient timed out.")
        except socket.error as e:
            # If an error occurs while sending the message, then print the error
            print(f"Data sending error: {e}")
    except (socket.timeout, socket.error, ConnectionRefusedError) as e:
        # If an error occurs while connecting to the server, or other errors occur, then print
        # the error
        print(f"Connection error: {e}")
    finally:
        # In all cases, close the socket if it was created during the function call
        if connection_socket:
            connection_socket.close()


def receive_message() -> None:
    """
    Function that receives a message from a client and prints it to the console
    :return: None
    """
    try:
        # Creating the server socket
        connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        # If an error occurs, print it and exit the program
        print(f"Socket creation error: {e}")
        return  # TODO - Should this be return or exit?

    try:
        # Bind the socket to a specific address and port
        connection_socket.bind((ALL_IP, PORT))
    except socket.error as e:
        # If an error occurs, print it, close the socket, and return from the function
        print(f"Socket binding error: {e}")
        connection_socket.close()
        return  # TODO - Should this be return or exit?

    # Let user know that the server is going to listen on the port
    print("Waiting for message on port " + str(PORT) + "...")

    try:
        # Listen for incoming connections
        connection_socket.listen()
    except socket.error as e:
        # If an error occurs, print it, close the socket, and return from the function
        print(f"Socket listening error: {e}")
        connection_socket.close()
        return  # TODO - Should this be return or exit?

    try:
        # Accepting a connection for the user
        connect_socket, address = connection_socket.accept()
    except socket.error as e:
        # If an error occurs, print it, close the socket, and return from the function
        print(f"Socket accepting error: {e}")
        connection_socket.close()
        return  # TODO - Should this be return or exit?

    # With the connection established, receive the message
    with connect_socket:
        # Let the user know that a connection has been established
        print(f"Connected by {address}")
        exit_switch = False

        # Loop until the message is received
        while not exit_switch:
            try:
                # Receive the message
                received = connect_socket.recv(BYTE_SIZE)

                # If the message is empty, then we have received the message
                if not received:
                    # Set the exit switch to true to exit the incoming socket loop
                    exit_switch = True
                else:
                    # Otherwise, print the message
                    print(f"Message received: {received.decode('utf-8')}")

                # Send the end message to the client to indicate an acknowledgement of the message
                connect_socket.sendall(END_MESSAGE)
            except socket.error as e:
                # If an error occurs, print it and exit the incoming socket loop
                print(f"Socket receiving error: {e}")
                exit_switch = True


def exit_program() -> None:
    """
    Function that exits the program
    :return: None
    """
    print("\nGoodbye!")

    # Exit the program with exit code 0
    exit(0)


def display_menu() -> str:
    """
    Function that displays the menu
    :return: The menu as a string
    """
    return "=== The Python Communicator ===\n" \
           "1) Send message\n" \
           "2) Receive message\n" \
           "0) Exit"


def menu() -> None:
    """
    Menu function that displays the menu and handles the user input
    :return: None
    """

    # Loop until the user exits. The user exits by entering 0
    while True:

        # Display the menu
        print(display_menu())

        # Get the user's input
        option = get_user_input("Enter your option: ", 1)

        # Handle the user's input
        if option == "1":
            send_message()
        elif option == "2":
            receive_message()
        elif option == "0":
            exit_program()
        else:
            print("Error, invalid input")


def main() -> None:
    """
    Main function of the program that calls the menu function to start the program loop
    :return: None
    """

    # Call the menu function
    menu()


if __name__ == "__main__":
    """
    This is executed when run from the command line
    """

    # Call the main function
    main()

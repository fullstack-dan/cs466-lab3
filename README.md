# Unsecured Network Communication Practice

This simple project is a lab completed for Western Carolina University's
CS 466 - Information Security course. The purpose of this lab is to practice
creating a simple client and server that communicate over an unsecured network
using TCP.

## Description

This project is a simple client and server that communicate over an unsecured
network using TCP. The client and server are written in Python 3. The client
sends a message to the server, and the server responds with an end message to
signal the acknowledgement of the message. The communication is then terminated.
The communication is not encrypted or secured in any way. This was done deliberately
to be able to analyze the communication using Wireshark. Attached are traces completed
using Wireshark to analyze the communication between the client and server. One point to
make is that the program can allow the user to act as either the client or server.


## Getting Started

### Dependencies

* Python 3
* Wireshark
* Any OS that can run Python 3 and Wireshark
* A port that is not in use by another program

### Installing

* Download the files from the repository
* Ensure that Python 3 is installed ```python --version```
* Ensure that Wireshark is installed
* Ensure that the port you want to use is not in use by another program
  * Edit the 
```communication.py``` file and change the constant ```PORT``` to the port you want to use
  * Make sure that the port is open on your firewall if you are using this program to communicate
  between two computers on a network [Link for Windows](https://www.tomshardware.com/news/how-to-open-firewall-ports-in-windows-10,36451.html)

### Executing program

* How to run the program:
1) Navigate to the directory where the files are located (The cs466-lab3 folder)
2) Run the file:
```python3 communication.py``` or ```python communication.py ```
3) If you are wanting to act as the server, press 2 and then enter.
4) If you are wanting to act as the client, press 1 and then enter.

## Authors

Kaushal Patel
[Kbpatel3](https://github.com/Kbpatel3)

Daniel Aoulou
[fullstack-dan](https://github.com/fullstack-dan)

## Version History

* 1.0
    * Initial Submission

## License

This project is not licensed.
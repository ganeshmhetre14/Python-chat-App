# ChatWave - Real-Time Chat Application

## Overview

ChatWave is a real-time chat application built using Python's `socket` and `tkinter` modules. It allows multiple users to connect to a central server and chat with each other.

## Features

- Real-time messaging between multiple clients.
- User-friendly graphical interface using `tkinter`.
- Server handles multiple client connections using threading.
- System messages for user join and leave events.
- Supports private and public chat rooms.

## Project Structure

```
ChatWave/
│── server.py          # Chat server script
│── client.py          # Chat client with GUI
│── requirements.txt   # Dependencies (only standard libraries used)
│── README.md          # Documentation
```

## Requirements

- Python 3.x
- Tkinter (built into Python on Windows/macOS; install separately on Linux using `sudo apt-get install python3-tk`)

## How to Run

### Start the Server

1. Open a terminal or command prompt.
2. Navigate to the project folder.
3. Run the following command:
   ```sh
   python server.py
   ```
   The server will start and listen for client connections.

### Start a Client

1. Open a **new** terminal or command prompt.
2. Navigate to the project folder.
3. Run:
   ```sh
   python client.py
   ```
4. Enter a nickname when prompted.
5. Start chatting!

### Connect Multiple Clients

- Open multiple instances of `client.py` to chat from different users.
- Run the client on different devices by changing the server's IP in `client.py`.

## Troubleshooting

### "ModuleNotFoundError: No module named 'tkinter'"

- If using Linux, install tkinter using:
  ```sh
  sudo apt-get install python3-tk
  ```

### "Connection Refused"

- Ensure that the server is running before starting the client.
- If running on different devices, check firewall settings and allow connections on port `5555`.

### "Address Already in Use"

- Change the port number in `server.py` and `client.py` to a different one (e.g., `port=5556`).

## Future Enhancements

- Implement user authentication.
- Add emoji and file sharing features.
- Create a web-based version using Flask or Django.

---

Happy chatting! 🎉

